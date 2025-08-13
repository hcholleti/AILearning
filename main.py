from fetcher.job_fetcher import JobFetcher
from filter.job_filter import JobFilter
from emailer.email_sender import EmailSender

def main():
    job_fetcher = JobFetcher()

    def job_process():
        # 1. Fetch jobs
        jobs = job_fetcher.fetch_jobs(keywords="DevOps Engineer", location="USA", posted_within_days=1)
        if not jobs:
            print("No jobs found.")
            return

        # 2. Filter jobs
        job_filter = JobFilter(jobs)
        filtered = job_filter.filter_jobs(title_keywords=["DevOps"], location="USA")

        # 3. Deduplicate jobs (pass seen_job_ids as needed, here using empty list for demo)
        unique = job_filter.deduplicate_jobs(seen_job_ids=[])

        # 4. Export to Excel
        filename = job_fetcher.export_to_excel(unique)
        print(f"Exported jobs to {filename}")

        # 5. Send email with attachment
        email_sender = EmailSender()
        email_sender.send_email(
            to_address="learnaitools01@gmail.com",  # Change to your email
            subject="Daily DevOps Engineer Job Listings",
            body="Please find attached the latest DevOps Engineer jobs.",
            attachment_path=filename
        )

    # Run the job process once (remove scheduling for now)
    job_process()

if __name__ == "__main__":
    main()

