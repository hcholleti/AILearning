# Entry point for the Enhanced Job Tracker Agent
# Features: Resume parsing (PDF/DOCX), AI-powered matching, LLM filtering, smart email reports

import os
from jobtracker.fetcher.fetcher import JobFetcher
from jobtracker.filter.filter import JobFilter
from jobtracker.resume.parser import resume_parser
from jobtracker.matcher.matcher import job_matcher
from jobtracker.filter.llm_filter import filter_jobs
from jobtracker.emailer.send_email import send_email
from jobtracker.config import JobTrackerConfig
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
    # Load configuration
    config = JobTrackerConfig.from_env()
    
    # Override with user-specific settings (you can modify these)
    config.resume_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../resumes/SathwikaSriramResumeDevOps.docx"))
    config.user_prompt = "filter for DevOps jobs requiring Terraform"
    config.job_keywords = "Software Engineer"
    config.job_location = "USA"
    config.posted_within_days = 20
    config.use_llm_filtering = False  # Set to True to use advanced LLM filtering
    config.match_score_threshold = 40.0  # Minimum match score to include jobs

    print(f"🚀 Starting Enhanced Job Tracker...")
    print(f"📄 Resume: {config.resume_path}")
    print(f"🔍 Keywords: {config.job_keywords}")
    print(f"📍 Location: {config.job_location}")
    print(f"🗂️  Filter: {config.user_prompt}")

    # Fetch jobs
    rapidapi_key = os.getenv("RAPIDAPI_KEY")
    if not rapidapi_key:
        print("❌ RAPIDAPI_KEY not found in environment variables")
        return
        
    fetcher = JobFetcher(rapidapi_key)
    print(f"🔎 Fetching jobs...")
    jobs = fetcher.fetch_jsearch(
        keywords=config.job_keywords, 
        location=config.job_location, 
        posted_within_days=config.posted_within_days
    )
    print(f"📊 Found {len(jobs)} initial jobs")

    # Deduplicate
    seen_path = os.path.join(os.path.dirname(__file__), "../outputs", "seen_jobs.csv")
    os.makedirs(os.path.dirname(seen_path), exist_ok=True)
    seen_ids = load_seen_ids(seen_path)
    jobs = JobFilter(jobs).deduplicate(seen_ids)
    print(f"🆕 {len(jobs)} new jobs after deduplication")

    if not jobs:
        print("ℹ️  No new jobs found")
        return

    # Parse resume
    if not os.path.exists(config.resume_path):
        print(f"❌ Resume not found: {config.resume_path}")
        return
        
    print(f"📄 Parsing resume...")
    resume_profile = resume_parser(config.resume_path)
    print(f"✅ Extracted {len(resume_profile['tech_skills'])} tech skills and {resume_profile['experience_years']} years experience")

    # Match jobs to resume
    print("🤖 AI-powered job matching...")
    matched_jobs = job_matcher(jobs, resume_profile)

    # Filter by minimum match score
    high_match_jobs = [job for job in matched_jobs if job.get('match_score', 0) >= config.match_score_threshold]
    print(f"📈 {len(high_match_jobs)} jobs above {config.match_score_threshold}% match threshold")

    # Apply LLM/semantic filtering
    print(f"🎯 Applying smart filtering...")
    filtered_jobs = filter_jobs(high_match_jobs, config.user_prompt, use_llm=config.use_llm_filtering)
    print(f"✨ {len(filtered_jobs)} jobs after filtering")

    if not filtered_jobs:
        print("ℹ️  No jobs match your criteria")
        return

    # Create enhanced Excel output
    df = pd.DataFrame([
        {
            "Title": j["title"], 
            "Company": j["company"], 
            "Location": f"{j.get('city')}, {j.get('state')}", 
            "Posted": j.get("posted_at"), 
            "Match Score": j.get("match_score"), 
            "Semantic Score": j.get("semantic_score"),
            "Skill Match Score": j.get("skill_match_score"),
            "Filter Score": j.get("filter_score"),
            "Matched Skills": ", ".join(j.get("matched_skills", [])),
            "URL": j.get("apply_url"), 
            "Source": j.get("source")
        }
        for j in filtered_jobs[:config.max_jobs_in_email]
    ])
    
    out_path = os.path.join(os.path.dirname(__file__), "../outputs", f"jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
    df.to_excel(out_path, index=False)
    print(f"📊 Saved results to: {out_path}")

    # Update seen jobs
    all_ids = set(list(seen_ids) + [j["id"] for j in filtered_jobs if j.get("id")])
    save_seen_ids(seen_path, all_ids)

    # Send enhanced email
    email_address = os.getenv("EMAIL_ADDRESS")
    if email_address:
        print(f"📧 Sending email to {email_address}...")
        send_email(
            filtered_jobs[:config.max_jobs_in_email], 
            to_address=email_address, 
            subject=f"{config.email_subject} - {len(filtered_jobs)} Matches", 
            attachment_path=out_path
        )
        print("✅ Email sent successfully!")
    else:
        print("⚠️  EMAIL_ADDRESS not configured, skipping email")

    print(f"🎉 Job tracking complete! Found {len(filtered_jobs)} relevant opportunities")

if __name__ == "__main__":
    main()
