from sentence_transformers import SentenceTransformer, util
from typing import List, Dict
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def job_matcher(jobs: List[Dict], resume_profile: Dict) -> List[Dict]:
    resume_emb = model.encode(resume_profile['text'], convert_to_tensor=True)
    for job in jobs:
        job_desc = job.get('raw', {}).get('job_description') or job.get('title', '')
        job_emb = model.encode(job_desc, convert_to_tensor=True)
        score = float(util.cos_sim(resume_emb, job_emb)[0][0])
        job['match_score'] = round(score * 100, 2)
        # Highlight matched skills
        job['matched_skills'] = [s for s in resume_profile['skills'] if s.lower() in (job_desc or '').lower()]
    return jobs
