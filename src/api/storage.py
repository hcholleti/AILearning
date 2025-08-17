"""
Azure Blob Storage integration for Job Tracker
Handles resume uploads, search results storage, and file management
"""
import os
import json
import csv
import io
from datetime import datetime
from typing import Dict, List, Optional
import tempfile

try:
    from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
    from azure.core.exceptions import ResourceNotFoundError
    AZURE_AVAILABLE = True
except ImportError:
    AZURE_AVAILABLE = False
    print("Azure Storage SDK not installed. Using local file storage as fallback.")

class AzureBlobStorage:
    """Azure Blob Storage client for job tracker data"""
    
    def __init__(self):
        if AZURE_AVAILABLE:
            self.connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
            self.container_name = os.getenv("AZURE_STORAGE_CONTAINER", "jobtracker")
            
            if self.connection_string:
                self.blob_service_client = BlobServiceClient.from_connection_string(
                    self.connection_string
                )
                self._ensure_container_exists()
            else:
                print("Azure Storage connection string not found. Using local storage.")
                self.blob_service_client = None
        else:
            self.blob_service_client = None
        
        # Fallback to local storage
        self.local_storage_path = os.path.join(os.path.dirname(__file__), "../storage")
        os.makedirs(self.local_storage_path, exist_ok=True)
    
    def _ensure_container_exists(self):
        """Create container if it doesn't exist"""
        try:
            self.blob_service_client.create_container(self.container_name)
        except Exception:
            pass  # Container might already exist
    
    async def upload_resume(self, session_id: str, filename: str, content: bytes) -> str:
        """Upload resume file to blob storage"""
        blob_name = f"resumes/{session_id}/{filename}"
        
        if self.blob_service_client:
            try:
                blob_client = self.blob_service_client.get_blob_client(
                    container=self.container_name,
                    blob=blob_name
                )
                blob_client.upload_blob(content, overwrite=True)
                return blob_client.url
            except Exception as e:
                print(f"Azure upload failed: {e}. Using local storage.")
        
        # Fallback to local storage
        local_path = os.path.join(self.local_storage_path, "resumes", session_id)
        os.makedirs(local_path, exist_ok=True)
        file_path = os.path.join(local_path, filename)
        
        with open(file_path, "wb") as f:
            f.write(content)
        
        return f"file://{file_path}"
    
    async def save_resume_profile(self, session_id: str, resume_profile: Dict) -> str:
        """Save parsed resume profile as JSON"""
        blob_name = f"profiles/{session_id}/profile.json"
        content = json.dumps(resume_profile, indent=2).encode('utf-8')
        
        if self.blob_service_client:
            try:
                blob_client = self.blob_service_client.get_blob_client(
                    container=self.container_name,
                    blob=blob_name
                )
                blob_client.upload_blob(content, overwrite=True)
                return blob_client.url
            except Exception as e:
                print(f"Azure upload failed: {e}. Using local storage.")
        
        # Fallback to local storage
        local_path = os.path.join(self.local_storage_path, "profiles", session_id)
        os.makedirs(local_path, exist_ok=True)
        file_path = os.path.join(local_path, "profile.json")
        
        with open(file_path, "w") as f:
            json.dump(resume_profile, f, indent=2)
        
        return f"file://{file_path}"
    
    async def get_resume_profile(self, session_id: str) -> Optional[Dict]:
        """Retrieve resume profile by session ID"""
        blob_name = f"profiles/{session_id}/profile.json"
        
        if self.blob_service_client:
            try:
                blob_client = self.blob_service_client.get_blob_client(
                    container=self.container_name,
                    blob=blob_name
                )
                content = blob_client.download_blob().readall()
                return json.loads(content.decode('utf-8'))
            except ResourceNotFoundError:
                pass
            except Exception as e:
                print(f"Azure download failed: {e}. Trying local storage.")
        
        # Fallback to local storage
        file_path = os.path.join(self.local_storage_path, "profiles", session_id, "profile.json")
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                return json.load(f)
        
        return None
    
    async def save_search_results(self, session_id: str, results: Dict) -> str:
        """Save search results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        blob_name = f"results/{session_id}/search_{timestamp}.json"
        content = json.dumps(results, indent=2, default=str).encode('utf-8')
        
        if self.blob_service_client:
            try:
                blob_client = self.blob_service_client.get_blob_client(
                    container=self.container_name,
                    blob=blob_name
                )
                blob_client.upload_blob(content, overwrite=True)
                
                # Also save as "latest" for easy retrieval
                latest_blob_name = f"results/{session_id}/latest.json"
                latest_blob_client = self.blob_service_client.get_blob_client(
                    container=self.container_name,
                    blob=latest_blob_name
                )
                latest_blob_client.upload_blob(content, overwrite=True)
                
                return blob_client.url
            except Exception as e:
                print(f"Azure upload failed: {e}. Using local storage.")
        
        # Fallback to local storage
        local_path = os.path.join(self.local_storage_path, "results", session_id)
        os.makedirs(local_path, exist_ok=True)
        
        file_path = os.path.join(local_path, f"search_{timestamp}.json")
        with open(file_path, "w") as f:
            json.dump(results, f, indent=2, default=str)
        
        # Save as latest
        latest_path = os.path.join(local_path, "latest.json")
        with open(latest_path, "w") as f:
            json.dump(results, f, indent=2, default=str)
        
        return f"file://{file_path}"
    
    async def get_search_results(self, session_id: str) -> Optional[Dict]:
        """Get latest search results for session"""
        blob_name = f"results/{session_id}/latest.json"
        
        if self.blob_service_client:
            try:
                blob_client = self.blob_service_client.get_blob_client(
                    container=self.container_name,
                    blob=blob_name
                )
                content = blob_client.download_blob().readall()
                return json.loads(content.decode('utf-8'))
            except ResourceNotFoundError:
                pass
            except Exception as e:
                print(f"Azure download failed: {e}. Trying local storage.")
        
        # Fallback to local storage
        file_path = os.path.join(self.local_storage_path, "results", session_id, "latest.json")
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                return json.load(f)
        
        return None
    
    async def export_to_csv(self, results: Dict) -> str:
        """Export search results to CSV file"""
        jobs = results.get("jobs", [])
        
        # Create temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            writer = csv.writer(f)
            
            # Write header
            headers = [
                "Title", "Company", "Location", "Match Score", "Semantic Score",
                "Skill Match Score", "Filter Score", "Matched Skills", "Posted Date",
                "Apply URL", "Source"
            ]
            writer.writerow(headers)
            
            # Write job data
            for job in jobs:
                row = [
                    job.get("title", ""),
                    job.get("company", ""),
                    f"{job.get('city', '')}, {job.get('state', '')}",
                    job.get("match_score", ""),
                    job.get("semantic_score", ""),
                    job.get("skill_match_score", ""),
                    job.get("filter_score", ""),
                    ", ".join(job.get("matched_skills", [])),
                    job.get("posted_at", ""),
                    job.get("apply_url", ""),
                    job.get("source", "")
                ]
                writer.writerow(row)
        
        return f.name
    
    async def delete_session(self, session_id: str):
        """Delete all data for a session"""
        if self.blob_service_client:
            try:
                # List and delete all blobs for this session
                blob_list = self.blob_service_client.get_container_client(
                    self.container_name
                ).list_blobs(name_starts_with=f"resumes/{session_id}/")
                
                for blob in blob_list:
                    self.blob_service_client.delete_blob(
                        container=self.container_name,
                        blob=blob.name
                    )
                
                # Delete profiles and results
                for prefix in [f"profiles/{session_id}/", f"results/{session_id}/"]:
                    blob_list = self.blob_service_client.get_container_client(
                        self.container_name
                    ).list_blobs(name_starts_with=prefix)
                    
                    for blob in blob_list:
                        self.blob_service_client.delete_blob(
                            container=self.container_name,
                            blob=blob.name
                        )
            except Exception as e:
                print(f"Azure deletion failed: {e}. Trying local storage.")
        
        # Fallback: delete local storage
        import shutil
        for folder in ["resumes", "profiles", "results"]:
            folder_path = os.path.join(self.local_storage_path, folder, session_id)
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
    
    async def list_sessions(self) -> List[str]:
        """List all session IDs"""
        sessions = set()
        
        if self.blob_service_client:
            try:
                blob_list = self.blob_service_client.get_container_client(
                    self.container_name
                ).list_blobs(name_starts_with="profiles/")
                
                for blob in blob_list:
                    session_id = blob.name.split('/')[1]
                    sessions.add(session_id)
                    
                return list(sessions)
            except Exception as e:
                print(f"Azure listing failed: {e}. Using local storage.")
        
        # Fallback: list local sessions
        profiles_path = os.path.join(self.local_storage_path, "profiles")
        if os.path.exists(profiles_path):
            return [d for d in os.listdir(profiles_path) if os.path.isdir(os.path.join(profiles_path, d))]
        
        return []

# Test/utility functions
async def test_storage():
    """Test storage functionality"""
    storage = AzureBlobStorage()
    
    print("Testing Azure Blob Storage integration...")
    
    # Test session
    test_session_id = "test-session-123"
    
    # Test resume profile
    test_profile = {
        "text": "Test resume content",
        "skills": ["python", "aws", "docker"],
        "experience_years": 5
    }
    
    await storage.save_resume_profile(test_session_id, test_profile)
    retrieved_profile = await storage.get_resume_profile(test_session_id)
    
    print(f"Profile saved and retrieved: {retrieved_profile is not None}")
    
    # Test search results
    test_results = {
        "jobs": [{"title": "Test Job", "company": "Test Corp", "match_score": 85}],
        "total_jobs": 1
    }
    
    await storage.save_search_results(test_session_id, test_results)
    retrieved_results = await storage.get_search_results(test_session_id)
    
    print(f"Results saved and retrieved: {retrieved_results is not None}")
    
    # List sessions
    sessions = await storage.list_sessions()
    print(f"Sessions found: {sessions}")
    
    # Cleanup
    await storage.delete_session(test_session_id)
    print("Test cleanup completed")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_storage())
