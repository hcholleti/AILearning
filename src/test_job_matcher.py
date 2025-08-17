from jobtracker.matcher.matcher import job_matcher

# Dummy jobs and resume profile for testing
jobs = [
    {"title": "DevOps Engineer", "raw": {"job_description": "Looking for a DevOps Engineer with AWS and Terraform experience."}},
    {"title": "Software Engineer", "raw": {"job_description": "Software Engineer with Python and cloud experience."}},
]
resume_profile = {
    "text": "Experienced DevOps Engineer skilled in AWS, Terraform, and CI/CD.",
    "skills": ["AWS", "Terraform", "CI/CD"],
    "tokens": ["devops", "engineer", "aws", "terraform", "ci", "cd"]
}

if __name__ == "__main__":
    matched = job_matcher(jobs, resume_profile)
    for job in matched:
        print(f"{job['title']}: {job['match_score']}% | Matched Skills: {job['matched_skills']}")
