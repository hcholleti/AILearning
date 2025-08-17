import os
from jobtracker.emailer.email_sender import EmailSender

def send_email(jobs, to_address, subject, attachment_path=None):
    # Compose email body with job title, company, match score, matched skills
    lines = []
    for job in jobs:
        lines.append(f"Title: {job.get('title')}")
        lines.append(f"Company: {job.get('company')}")
        lines.append(f"Match Score: {job.get('match_score', 'N/A')}%")
        if job.get('matched_skills'):
            lines.append(f"Matched Skills: {', '.join(job['matched_skills'])}")
        lines.append(f"URL: {job.get('apply_url')}")
        lines.append("")
    body = "\n".join(lines)
    emailer = EmailSender()
    emailer.send(to_address=to_address, subject=subject, body=body, attachment_path=attachment_path)
