# Entry point for the Job Tracker Agent prototype.
# (Moved from project root to src/main.py)

import os
from jobtracker.fetcher.fetcher import JobFetcher
from jobtracker.filter.filter import JobFilter
from jobtracker.emailer.email_sender import EmailSender
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
    rapidapi_key = os.getenv("RAPIDAPI_KEY")
    fetcher = JobFetcher(rapidapi_key)
    jobs = fetcher.fetch_jsearch(keywords="DevOps Engineer", location="USA", posted_within_days=3)

    seen_path = os.path.join(os.path.dirname(__file__), "../outputs", "seen_jobs.csv")
    os.makedirs(os.path.dirname(seen_path), exist_ok=True)
    seen_ids = load_seen_ids(seen_path)

    jf = JobFilter(jobs)
    new_jobs = jf.deduplicate(seen_ids)
    new_jobs = JobFilter(new_jobs).filter_by_keywords(["devops", "engineer"])

    if not new_jobs:
        print("No new jobs to report.")
        return

    # save excel
    df = pd.DataFrame([{"Title": j["title"], "Company": j["company"], "Location": f"{j.get('city')}, {j.get('state')}", "Posted": j.get("posted_at"), "URL": j.get("apply_url"), "Source": j.get("source")} for j in new_jobs])
    out_path = os.path.join(os.path.dirname(__file__), "../outputs", f"jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
    df.to_excel(out_path, index=False)

    # update seen ids
    all_ids = set(list(seen_ids) + [j["id"] for j in new_jobs if j.get("id")])
    save_seen_ids(seen_path, all_ids)

    # send email
    emailer = EmailSender()
    emailer.send(to_address=os.getenv("EMAIL_ADDRESS"), subject="Daily Jobs", body=f"Found {len(new_jobs)} new jobs.", attachment_path=out_path)
    print("Done")

if __name__ == "__main__":
    main()
