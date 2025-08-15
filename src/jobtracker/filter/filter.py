# jobtracker.filter.filter

class JobFilter:
    def __init__(self, jobs):
        self.jobs = jobs

    def deduplicate(self, seen_ids):
        return [job for job in self.jobs if job.get("id") not in seen_ids]

    def filter_by_keywords(self, keywords):
        filtered = []
        for job in self.jobs:
            title = (job.get("title") or "").lower()
            if any(kw.lower() in title for kw in keywords):
                filtered.append(job)
        return filtered
