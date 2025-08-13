import requests
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
# from emailer.email_sender import EmailSender

load_dotenv()


class JobFetcher:
    def __init__(self):
        self.api_url = "https://jsearch.p.rapidapi.com/search"
        api_key = os.getenv("RAPIDAPI_KEY")
        if not api_key:
            raise ValueError("RAPIDAPI_KEY not set in environment variables.")
        self.headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }

    def fetch_jobs(self, keywords="python developer", location="USA", posted_within_days=1):
        params = {
            "query": keywords,
            "location": location,
            "date_posted": "today" if posted_within_days == 1 else f"last_{posted_within_days}_days",
            "page": 1,
            "num_pages": 1
        }
        response = requests.get(self.api_url, headers=self.headers, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get("data", [])
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return []

    def export_to_excel(self, jobs, filename=None):
        """
        Exports a list of job dicts to an Excel file in the 'JobResults' folder.
        """
        if not jobs:
            print("No jobs to export.")
            return None

        # Ensure JobResults directory exists at the project root
        output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'JobResults'))
        os.makedirs(output_dir, exist_ok=True)

        rows = []
        for job in jobs:
            rows.append({
                "Job Title": job.get("job_title"),
                "Company": job.get("employer_name"),
                "Location": f"{job.get('job_city', '')}, {job.get('job_state', '')}",
                "Posted Date": job.get("job_posted_at_datetime_utc"),
                "Job URL": job.get("job_apply_link"),
                "Source": "JSearch"
            })

        if not filename:
            filename = f"jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        filepath = os.path.join(output_dir, filename)
        df = pd.DataFrame(rows)
        df.to_excel(filepath, index=False)
        print(f"✅ Saved {len(rows)} jobs to {filepath}")
        return filepath

    def get_job_sources(self):
        """
        Returns the job sources and search parameters used for fetching jobs.
        """
        return {
            "source": "JSearch API via RapidAPI",
            "search_query": "DevOps Engineer",
            "location": "USA",
            "date_posted": "today"
        }


if __name__ == "__main__":
    fetcher = JobFetcher()
    jobs = fetcher.fetch_jobs(keywords="DevOps Engineer", location="USA", posted_within_days=1)
    if jobs:
        filename = fetcher.export_to_excel(jobs)
        print(f"Exported jobs to {filename}")
    else:
        print("No jobs found.")
