from jobtracker.filter.llm_filter import filter_jobs

jobs = [
    {"title": "DevOps Engineer", "raw": {"job_description": "Looking for a DevOps Engineer with AWS and Terraform experience."}},
    {"title": "Devops Engineer", "raw": {"job_description": "Devops Engineer with Python and cloud experience."}},
]

if __name__ == "__main__":
    prompt = "filter for DevOps jobs requiring DevOps skills"
    filtered = filter_jobs(jobs, prompt)
    for job in filtered:
        print(f"{job['title']}: {job['raw']['job_description']}")
