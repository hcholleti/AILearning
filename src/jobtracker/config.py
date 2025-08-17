# Configuration settings for the Job Tracker
import os
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class JobTrackerConfig:
    """Configuration class for job tracker settings"""
    
    # Resume settings
    resume_path: str = ""
    
    # Job search parameters
    job_keywords: str = "Software Engineer"
    job_location: str = "USA"
    posted_within_days: int = 7
    
    # Filtering settings
    user_prompt: str = "filter for relevant jobs"
    use_llm_filtering: bool = False
    match_score_threshold: float = 50.0  # Minimum match score percentage
    
    # Email settings
    email_subject: str = "Daily Job Matches"
    max_jobs_in_email: int = 10
    
    # Model settings
    sentence_transformer_model: str = "all-MiniLM-L6-v2"
    
    # Scoring weights
    semantic_weight: float = 0.7
    skill_weight: float = 0.3
    
    @classmethod
    def from_env(cls) -> 'JobTrackerConfig':
        """Create config from environment variables"""
        return cls(
            resume_path=os.getenv("RESUME_PATH", ""),
            job_keywords=os.getenv("JOB_KEYWORDS", "Software Engineer"),
            job_location=os.getenv("JOB_LOCATION", "USA"),
            posted_within_days=int(os.getenv("POSTED_WITHIN_DAYS", "7")),
            user_prompt=os.getenv("USER_PROMPT", "filter for relevant jobs"),
            use_llm_filtering=os.getenv("USE_LLM_FILTERING", "false").lower() == "true",
            match_score_threshold=float(os.getenv("MATCH_SCORE_THRESHOLD", "50.0")),
            email_subject=os.getenv("EMAIL_SUBJECT", "Daily Job Matches"),
            max_jobs_in_email=int(os.getenv("MAX_JOBS_IN_EMAIL", "10")),
        )

# Predefined skill categories for better matching
TECH_SKILLS = {
    'programming_languages': [
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust', 
        'php', 'ruby', 'swift', 'kotlin', 'scala', 'r'
    ],
    'web_frameworks': [
        'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 
        'spring', 'laravel', 'rails'
    ],
    'cloud_platforms': [
        'aws', 'azure', 'gcp', 'google cloud', 'amazon web services', 
        'microsoft azure', 'digital ocean', 'heroku'
    ],
    'devops_tools': [
        'docker', 'kubernetes', 'terraform', 'ansible', 'jenkins', 'gitlab ci',
        'github actions', 'circleci', 'travis ci', 'helm'
    ],
    'databases': [
        'sql', 'postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch',
        'cassandra', 'dynamodb', 'oracle', 'sqlite'
    ],
    'data_science': [
        'machine learning', 'deep learning', 'ai', 'data science', 'pandas', 
        'numpy', 'tensorflow', 'pytorch', 'scikit-learn', 'spark', 'hadoop'
    ],
    'monitoring': [
        'prometheus', 'grafana', 'datadog', 'new relic', 'splunk', 'elk stack',
        'kibana', 'logstash'
    ]
}

# Flatten all skills for easy lookup
ALL_TECH_SKILLS = set()
for category, skills in TECH_SKILLS.items():
    ALL_TECH_SKILLS.update(skills)
