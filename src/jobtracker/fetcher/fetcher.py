"""jobtracker.fetcher.fetcher

Simple fetcher implementation for JSearch (RapidAPI).
"""
import os
import requests
from typing import List, Dict, Optional

RAPIDAPI_HOST = "jsearch.p.rapidapi.com"

class JobFetcher:
    """Fetch jobs from public job APIs. Start with JSearch (RapidAPI).

    Usage:
        fetcher = JobFetcher()
        jobs = fetcher.fetch_jsearch("devops engineer", "USA", posted_within_days=1)
    """

    def __init__(self, rapidapi_key: Optional[str] = None):
        self.api_key = rapidapi_key or os.getenv("RAPIDAPI_KEY")
        if not self.api_key:
            raise ValueError("RAPIDAPI_KEY is required (set it in .env or pass to JobFetcher)")
        self.base_url = f"https://{RAPIDAPI_HOST}/search"
        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": RAPIDAPI_HOST,
        }

    def fetch_jsearch(self, keywords: str = "python developer", location: str = "USA", posted_within_days: int = 1, page: int = 1) -> List[Dict]:
        """Fetch jobs from the JSearch API and normalize result records.

        Returns a list of dicts with keys: id, title, company, city, state, posted_at, apply_url, source
        """
        import sys
        # Map posted_within_days to API values
        if posted_within_days <= 1:
            date_posted = "today"
        elif posted_within_days <= 3:
            date_posted = "3days"
        elif posted_within_days <= 7:
            date_posted = "week"
        elif posted_within_days <= 30:
            date_posted = "month"
        else:
            date_posted = "anytime"
        params = {
            "query": keywords,
            "location": location,
            "date_posted": date_posted,
            "page": page,
            "num_pages": 1,
        }
        try:
            resp = requests.get(self.base_url, headers=self.headers, params=params, timeout=30)
            resp.raise_for_status()
            payload = resp.json()
        except Exception as e:
            print(f"[JobFetcher] Error fetching jobs: {e}", file=sys.stderr)
            if hasattr(e, 'response') and e.response is not None:
                print(f"[JobFetcher] Response text: {e.response.text}", file=sys.stderr)
            return []

        if not isinstance(payload, dict) or "data" not in payload:
            print(f"[JobFetcher] Unexpected API response: {payload}", file=sys.stderr)
            return []

        raw = payload.get("data", [])
        jobs = []
        for item in raw:
            job_id = item.get("job_id") or item.get("id") or item.get("job_apply_link")
            jobs.append({
                "id": str(job_id),
                "title": item.get("job_title"),
                "company": item.get("employer_name"),
                "city": item.get("job_city"),
                "state": item.get("job_state"),
                "posted_at": item.get("job_posted_at_datetime_utc") or item.get("job_posted_at") or None,
                "apply_url": item.get("job_apply_link") or item.get("job_link"),
                "source": "jsearch",
                "raw": item,
            })
        if not jobs:
            print(f"[JobFetcher] No jobs found. Raw API data: {raw}", file=sys.stderr)
        return jobs
