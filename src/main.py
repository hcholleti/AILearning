# Entry point for the Job Tracker Agent prototype.
# (Moved from project root to src/main.py)

import os
from jobtracker.fetcher.fetcher import JobFetcher
from jobtracker.filter.filter import JobFilter
from jobtracker.resume.parser import resume_parser
from jobtracker.matcher.matcher import job_matcher
from jobtracker.filter.llm_filter import filter_jobs
from jobtracker.emailer.send_email import send_email
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# Always load .env from project root
load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env")))

def load_seen_ids(path: str):
    if not os.path.exists(path):
        return set()
    return set([l.strip() for l in open(path, "r") if l.strip()])

def save_seen_ids(path: str, ids):
    with open(path, "w") as f:
        for i in ids:
            f.write(f"{i}\n")


def main():
    # --- User config ---
    resume_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../resumes/SathwikaSriramResumeDevOps.docx"))  # Update to your resume
    user_prompt = "filter for DevOps jobs requiring Terraform"  # Example prompt
    job_keywords = "Software Engineer"
    job_location = "USA"
    posted_within_days = 20

    rapidapi_key = os.getenv("RAPIDAPI_KEY")
    fetcher = JobFetcher(rapidapi_key)
    jobs = fetcher.fetch_jsearch(keywords=job_keywords, location=job_location, posted_within_days=posted_within_days)

    seen_path = os.path.join(os.path.dirname(__file__), "../outputs", "seen_jobs.csv")
    os.makedirs(os.path.dirname(seen_path), exist_ok=True)
    seen_ids = load_seen_ids(seen_path)
    jobs = JobFilter(jobs).deduplicate(seen_ids)

    # --- Resume parsing ---
    print(f"Parsing resume: {resume_path}")
    resume_profile = resume_parser(resume_path)

    # --- Job matching ---
    print("Matching jobs to resume...")
    matched_jobs = job_matcher(jobs, resume_profile)

    # --- LLM/prompt filtering ---
    print(f"Filtering jobs with prompt: {user_prompt}")
    filtered_jobs = filter_jobs(matched_jobs, user_prompt)

    if not filtered_jobs:
        print("No new jobs to report.")
        return

    # save excel
    df = pd.DataFrame([
        {"Title": j["title"], "Company": j["company"], "Location": f"{j.get('city')}, {j.get('state')}", "Posted": j.get("posted_at"), "URL": j.get("apply_url"), "Source": j.get("source"), "Match Score": j.get("match_score"), "Matched Skills": ", ".join(j.get("matched_skills", []))}
        for j in filtered_jobs
    ])
    out_path = os.path.join(os.path.dirname(__file__), "../outputs", f"jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
    df.to_excel(out_path, index=False)

    # update seen ids
    all_ids = set(list(seen_ids) + [j["id"] for j in filtered_jobs if j.get("id")])
    save_seen_ids(seen_path, all_ids)

    # send email
    send_email(filtered_jobs, to_address=os.getenv("EMAIL_ADDRESS"), subject="Daily Jobs", attachment_path=out_path)
    print("Done")

if __name__ == "__main__":
    main()
