from sentence_transformers import SentenceTransformer, util
from typing import List, Dict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

def job_matcher(jobs: List[Dict], resume_profile: Dict) -> List[Dict]:
    """Enhanced job matcher with semantic similarity and skill matching"""
    resume_text = resume_profile['text']
    resume_skills = set([s.lower() for s in resume_profile.get('tech_skills', [])])
    
    # Pre-compute resume embedding
    resume_emb = model.encode(resume_text, convert_to_tensor=True)
    
    for job in jobs:
        job_desc = job.get('raw', {}).get('job_description') or job.get('title', '')
        job_text = f"{job.get('title', '')} {job_desc}"
        
        # Semantic similarity using sentence transformers
        job_emb = model.encode(job_text, convert_to_tensor=True)
        semantic_score = float(util.cos_sim(resume_emb, job_emb)[0][0])
        
        # Skill matching score
        job_text_lower = job_text.lower()
        matched_skills = [skill for skill in resume_skills if skill in job_text_lower]
        skill_score = len(matched_skills) / max(len(resume_skills), 1) if resume_skills else 0
        
        # Combined score (70% semantic, 30% skill matching)
        combined_score = (semantic_score * 0.7) + (skill_score * 0.3)
        
        # Experience factor (if job mentions years and we have experience data)
        experience_bonus = 0
        if resume_profile.get('experience_years', 0) > 0:
            if any(word in job_text_lower for word in ['senior', 'lead', 'architect']):
                if resume_profile['experience_years'] >= 5:
                    experience_bonus = 0.1
            elif any(word in job_text_lower for word in ['junior', 'entry', 'graduate']):
                if resume_profile['experience_years'] <= 2:
                    experience_bonus = 0.1
        
        final_score = min(combined_score + experience_bonus, 1.0)
        
        job['match_score'] = round(final_score * 100, 2)
        job['matched_skills'] = matched_skills
        job['semantic_score'] = round(semantic_score * 100, 2)
        job['skill_match_score'] = round(skill_score * 100, 2)
    
    return sorted(jobs, key=lambda x: x['match_score'], reverse=True)
