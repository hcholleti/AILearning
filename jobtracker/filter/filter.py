"""jobtracker.filter.filter
Filtering and deduplication utilities for job listings.
"""
from datetime import datetime
from typing import List, Dict, Iterable, Set


class JobFilter:
    def __init__(self, jobs: Iterable[Dict]):
        self.jobs = list(jobs)

    def filter_by_keywords(self, keywords: Iterable[str]) -> List[Dict]:
        keys = [k.lower() for k in keywords]
        return [j for j in self.jobs if j.get("title") and any(k in j["title"].lower() for k in keys)]

    def filter_by_location(self, location_substring: str) -> List[Dict]:
        s = location_substring.lower()
        return [j for j in self.jobs if ((j.get("city") or "") + ", " + (j.get("state") or "")).lower().find(s) != -1]

    def filter_by_recent(self, days: int) -> List[Dict]:
        cutoff = datetime.utcnow().timestamp() - days * 86400
        out = []
        for j in self.jobs:
            posted = j.get("posted_at")
            if not posted:
                continue
            try:
                ts = datetime.fromisoformat(posted.replace("Z", "+00:00")).timestamp()
            except Exception:
                continue
            if ts >= cutoff:
                out.append(j)
        return out

    def deduplicate(self, seen_ids: Iterable[str]) -> List[Dict]:
        seen: Set[str] = set(seen_ids)
        out = []
        for j in self.jobs:
            if j.get("id") and j["id"] not in seen:
                out.append(j)
                seen.add(j["id"])
        return out
