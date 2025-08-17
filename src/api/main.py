"""
FastAPI backend for Job Tracker
Provides REST API endpoints for job search, resume parsing, and result management
"""
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import List, Optional
import tempfile
import os
import json
from datetime import datetime
import uuid

# Import our job tracker modules
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from jobtracker.fetcher.fetcher import JobFetcher
from jobtracker.filter.filter import JobFilter
from jobtracker.resume.parser import resume_parser
from jobtracker.matcher.matcher import job_matcher
from jobtracker.filter.llm_filter import filter_jobs
from jobtracker.config import JobTrackerConfig
from api.storage import AzureBlobStorage

# Initialize FastAPI app
app = FastAPI(
    title="AI Job Tracker API",
    description="AI-powered job matching and filtering system",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Azure Blob Storage
storage = AzureBlobStorage()

# Pydantic models for API
class JobSearchRequest(BaseModel):
    keywords: str
    location: str = "USA"
    posted_within_days: int = 7
    user_prompt: str = "filter for relevant jobs"
    match_score_threshold: float = 50.0
    use_llm_filtering: bool = False

class JobSearchResponse(BaseModel):
    session_id: str
    total_jobs: int
    filtered_jobs: int
    jobs: List[dict]
    resume_profile: dict
    search_params: dict

class ResumeUploadResponse(BaseModel):
    session_id: str
    filename: str
    resume_profile: dict
    blob_url: str

@app.get("/")
async def root():
    return {"message": "AI Job Tracker API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/upload-resume", response_model=ResumeUploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    """Upload and parse resume (PDF/DOCX)"""
    try:
        # Validate file type
        if not file.filename.lower().endswith(('.pdf', '.docx')):
            raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported")
        
        # Generate session ID
        session_id = str(uuid.uuid4())
        
        # Save file temporarily for processing
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        try:
            # Parse resume
            resume_profile = resume_parser(tmp_file_path)
            
            # Upload to Azure Blob Storage
            blob_url = await storage.upload_resume(session_id, file.filename, content)
            
            # Save resume profile metadata
            await storage.save_resume_profile(session_id, resume_profile)
            
            return ResumeUploadResponse(
                session_id=session_id,
                filename=file.filename,
                resume_profile=resume_profile,
                blob_url=blob_url
            )
            
        finally:
            # Clean up temporary file
            os.unlink(tmp_file_path)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Resume processing failed: {str(e)}")

@app.post("/search-jobs", response_model=JobSearchResponse)
async def search_jobs(request: JobSearchRequest, session_id: str):
    """Search and match jobs with uploaded resume"""
    try:
        # Get resume profile from storage
        resume_profile = await storage.get_resume_profile(session_id)
        if not resume_profile:
            raise HTTPException(status_code=404, detail="Resume not found. Please upload a resume first.")
        
        # Fetch jobs
        rapidapi_key = os.getenv("RAPIDAPI_KEY")
        if not rapidapi_key:
            raise HTTPException(status_code=500, detail="RapidAPI key not configured")
        
        fetcher = JobFetcher(rapidapi_key)
        jobs = fetcher.fetch_jsearch(
            keywords=request.keywords,
            location=request.location,
            posted_within_days=request.posted_within_days
        )
        
        # Deduplicate (simplified for API)
        job_filter = JobFilter(jobs)
        jobs = job_filter.deduplicate(set())  # No persistence for API demo
        
        if not jobs:
            return JobSearchResponse(
                session_id=session_id,
                total_jobs=0,
                filtered_jobs=0,
                jobs=[],
                resume_profile=resume_profile,
                search_params=request.dict()
            )
        
        # Match jobs to resume
        matched_jobs = job_matcher(jobs, resume_profile)
        
        # Filter by match score threshold
        high_match_jobs = [
            job for job in matched_jobs 
            if job.get('match_score', 0) >= request.match_score_threshold
        ]
        
        # Apply semantic/LLM filtering
        filtered_jobs = filter_jobs(
            high_match_jobs, 
            request.user_prompt, 
            use_llm=request.use_llm_filtering
        )
        
        # Save search results to storage
        search_results = {
            "search_params": request.dict(),
            "total_jobs": len(jobs),
            "filtered_jobs": len(filtered_jobs),
            "jobs": filtered_jobs[:20],  # Limit for UI performance
            "timestamp": datetime.now().isoformat()
        }
        await storage.save_search_results(session_id, search_results)
        
        return JobSearchResponse(
            session_id=session_id,
            total_jobs=len(jobs),
            filtered_jobs=len(filtered_jobs),
            jobs=filtered_jobs[:20],
            resume_profile=resume_profile,
            search_params=request.dict()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job search failed: {str(e)}")

@app.get("/search-results/{session_id}")
async def get_search_results(session_id: str):
    """Get saved search results"""
    try:
        results = await storage.get_search_results(session_id)
        if not results:
            raise HTTPException(status_code=404, detail="Search results not found")
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve results: {str(e)}")

@app.get("/export-results/{session_id}")
async def export_results(session_id: str, format: str = "csv"):
    """Export search results as CSV or JSON"""
    try:
        results = await storage.get_search_results(session_id)
        if not results:
            raise HTTPException(status_code=404, detail="Search results not found")
        
        if format.lower() == "csv":
            csv_content = await storage.export_to_csv(results)
            return FileResponse(
                csv_content,
                media_type="text/csv",
                filename=f"job_results_{session_id[:8]}.csv"
            )
        elif format.lower() == "json":
            return JSONResponse(results)
        else:
            raise HTTPException(status_code=400, detail="Format must be 'csv' or 'json'")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")

@app.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """Delete session data (resume + search results)"""
    try:
        await storage.delete_session(session_id)
        return {"message": "Session deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Session deletion failed: {str(e)}")

@app.get("/sessions")
async def list_sessions():
    """List all sessions (for admin/debugging)"""
    try:
        sessions = await storage.list_sessions()
        return {"sessions": sessions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list sessions: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
