from jobtracker.emailer.send_email import send_email

jobs = [
    {"title": "DevOps Engineer", "company": "Acme Corp", "match_score": 92.5, "matched_skills": ["AWS", "Terraform"], "apply_url": "http://example.com/job1"},
    {"title": "Software Engineer", "company": "Beta Inc", "match_score": 80.0, "matched_skills": ["Python"], "apply_url": "http://example.com/job2"},
]

if __name__ == "__main__":
    # This will actually send an email! Use with caution and set EMAIL_ADDRESS in your .env
    send_email(jobs, to_address="your@email.com", subject="Test Jobs", attachment_path=None)
    print("Test email sent (if credentials are correct)")
