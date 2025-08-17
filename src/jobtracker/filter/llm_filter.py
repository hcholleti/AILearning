import os
import re
from typing import List, Dict
from sentence_transformers import SentenceTransformer, util

# Initialize model for semantic filtering
model = SentenceTransformer('all-MiniLM-L6-v2')

def filter_jobs(jobs: List[Dict], user_prompt: str, use_llm: bool = False) -> List[Dict]:
    """Enhanced job filtering with semantic similarity and optional LLM integration"""
    print(f"Filtering jobs with prompt: {user_prompt}")
    
    if use_llm:
        return _llm_filter(jobs, user_prompt)
    else:
        return _semantic_filter(jobs, user_prompt)

def _semantic_filter(jobs: List[Dict], user_prompt: str) -> List[Dict]:
    """Semantic filtering using sentence transformers"""
    prompt_embedding = model.encode(user_prompt, convert_to_tensor=True)
    filtered_jobs = []
    
    for job in jobs:
        job_text = f"{job.get('title', '')} {job.get('raw', {}).get('job_description', '')}"
        job_embedding = model.encode(job_text, convert_to_tensor=True)
        
        # Calculate semantic similarity
        similarity = float(util.cos_sim(prompt_embedding, job_embedding)[0][0])
        
        # Also check for direct keyword matches
        keywords = _extract_keywords(user_prompt)
        keyword_matches = sum(1 for keyword in keywords if keyword.lower() in job_text.lower())
        keyword_score = keyword_matches / max(len(keywords), 1) if keywords else 0
        
        # Combined filtering score (60% semantic, 40% keyword)
        combined_score = (similarity * 0.6) + (keyword_score * 0.4)
        
        # Filter threshold
        if combined_score > 0.3:  # Adjust threshold as needed
            job['filter_score'] = round(combined_score * 100, 2)
            filtered_jobs.append(job)
    
    return sorted(filtered_jobs, key=lambda x: x.get('filter_score', 0), reverse=True)

def _extract_keywords(prompt: str) -> List[str]:
    """Extract meaningful keywords from the prompt"""
    # Remove common words and extract important terms
    stop_words = {'filter', 'for', 'jobs', 'requiring', 'with', 'and', 'or', 'the', 'in', 'at', 'to', 'of'}
    words = re.findall(r'\b\w+\b', prompt.lower())
    return [word for word in words if word not in stop_words and len(word) > 2]

def _llm_filter(jobs: List[Dict], user_prompt: str) -> List[Dict]:
    """LLM-based filtering using OpenAI or similar (placeholder for now)"""
    # TODO: Implement actual LLM filtering using OpenAI API or HuggingFace
    # For now, fall back to semantic filtering
    print("LLM filtering not implemented yet, using semantic filtering...")
    return _semantic_filter(jobs, user_prompt)
