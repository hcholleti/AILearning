import os
from jobtracker.emailer.email_sender import EmailSender
from typing import List, Dict

def send_email(jobs: List[Dict], to_address: str, subject: str, attachment_path: str = None):
    """Enhanced email composition with better formatting and insights"""
    
    if not jobs:
        body = "No matching jobs found for your criteria."
    else:
        # Sort jobs by match score for better presentation
        sorted_jobs = sorted(jobs, key=lambda x: x.get('match_score', 0), reverse=True)
        
        # Email header with summary
        avg_score = sum(job.get('match_score', 0) for job in jobs) / len(jobs)
        header = f"""
Job Search Results Summary:
==========================
Total Jobs Found: {len(jobs)}
Average Match Score: {avg_score:.1f}%
Best Match: {sorted_jobs[0].get('match_score', 0):.1f}%

Top Job Matches:
================
"""
        
        # Format each job
        job_lines = []
        for i, job in enumerate(sorted_jobs[:10], 1):  # Show top 10 jobs
            match_score = job.get('match_score', 0)
            semantic_score = job.get('semantic_score', 'N/A')
            skill_score = job.get('skill_match_score', 'N/A')
            filter_score = job.get('filter_score', 'N/A')
            
            job_info = f"""
{i}. {job.get('title', 'N/A')} at {job.get('company', 'N/A')}
   📍 Location: {job.get('city', '')}, {job.get('state', '')}
   📊 Overall Match: {match_score}% (Semantic: {semantic_score}%, Skills: {skill_score}%)
   🎯 Filter Score: {filter_score}%
   💼 Posted: {job.get('posted_at', 'N/A')}
   🔗 Apply: {job.get('apply_url', 'N/A')}
   🛠️  Matched Skills: {', '.join(job.get('matched_skills', [])[:5])}{'...' if len(job.get('matched_skills', [])) > 5 else ''}
"""
            job_lines.append(job_info)
        
        # Additional insights
        all_skills = []
        for job in jobs:
            all_skills.extend(job.get('matched_skills', []))
        
        from collections import Counter
        top_skills = Counter(all_skills).most_common(5)
        
        insights = f"""

Key Insights:
=============
📈 Most In-Demand Skills from Your Profile:
{chr(10).join([f"   • {skill}: {count} jobs" for skill, count in top_skills])}

💡 Recommendation: Focus on jobs with match scores above {avg_score:.0f}% for better alignment.
"""
        
        body = header + "\n".join(job_lines) + insights
    
    emailer = EmailSender()
    emailer.send(to_address=to_address, subject=subject, body=body, attachment_path=attachment_path)
