# LLM-based job filtering (stub, can use OpenAI or HuggingFace)
def filter_jobs(jobs, user_prompt, llm=None):
    print(f"Filtering jobs with prompt: {user_prompt}")
    # For now, simple keyword filter. Replace with LLM call as needed.
    prompt = user_prompt.lower()
    filtered = []
    for job in jobs:
        desc = (job.get('raw', {}).get('job_description') or job.get('title', '')).lower()
        if all(word in desc for word in prompt.split() if word not in {'for', 'jobs', 'requiring'}):
            filtered.append(job)
    return filtered
