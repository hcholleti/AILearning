from datetime import datetime

class JobFilter:
    def __init__(self, job_listings):
        self.job_listings = job_listings

    def filter_jobs(self, title_keywords=None, location=None, posted_date=None):
        filtered_jobs = self.job_listings

        if title_keywords:
            filtered_jobs = [
                job for job in filtered_jobs
                if any(keyword.lower() in job.get('job_title', '').lower() for keyword in title_keywords)
            ]

        if location:
            filtered_jobs = [
                job for job in filtered_jobs
                if location.lower() in (job.get('job_city', '') + ', ' + job.get('job_state', '')).lower()
            ]

        if posted_date:
            filtered_jobs = [
                job for job in filtered_jobs
                if job.get('job_posted_at_datetime_utc') and
                   job['job_posted_at_datetime_utc'] >= posted_date
            ]

        return filtered_jobs

    def deduplicate_jobs(self, seen_job_ids):
        unique_jobs = []
        seen_ids = set(seen_job_ids)

        for job in self.job_listings:
            job_id = job.get('job_id') or job.get('id')
            if job_id and job_id not in seen_ids:
                unique_jobs.append(job)
                seen_ids.add(job_id)

        return unique_jobs
