"""Seed data for the Reports app.

In a real system this would come from a database. For workshop purposes a deterministic
in-memory list keeps everything reproducible.
"""

from __future__ import annotations

import random
from datetime import datetime, timedelta, timezone

from app.models import Report, ReportStatus

_OWNERS: list[tuple[str, str]] = [
    ("Aanya Sharma", "aanya.sharma@example.com"),
    ("Ben Carter", "ben.carter@example.com"),
    ("Chen Wei", "chen.wei@example.com"),
    ("Dara O'Connor", "dara.oconnor@example.com"),
    ("Eli Müller", "eli.mueller@example.com"),
    ("Farah Habib", "farah.habib@example.com"),
    ("Gabriel Rossi", "gabriel.rossi@example.com"),
    ("Hana Tanaka", "hana.tanaka@example.com"),
]

_TITLES: list[str] = [
    "Q1 revenue summary",
    "Marketing spend, Feb",
    "Support cost rollup",
    'CSV with commas, "quotes" and newlines\nin the title',  # edge case for RFC 4180
    "AWS invoice review",
    "Engineering headcount plan",
    "Customer NPS analysis",
    "Partner referral commissions",
    "Refund pipeline weekly",
    "EU compliance audit notes",
]

_STATUSES: list[ReportStatus] = ["pending", "approved", "rejected", "archived"]


def _generate_reports() -> list[Report]:
    rng = random.Random(20260523)  # deterministic seed
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    rows: list[Report] = []
    for i in range(1, 121):  # 120 rows
        owner, email = rng.choice(_OWNERS)
        rows.append(
            Report(
                id=i,
                internal_id=f"INT-{i:06d}-{rng.randrange(10_000, 100_000)}",
                title=rng.choice(_TITLES),
                status=rng.choice(_STATUSES),
                owner=owner,
                owner_email=email,
                amount=round(rng.uniform(100, 50_000), 2),
                created_at=start + timedelta(hours=rng.randrange(0, 24 * 140)),
            )
        )
    return rows


REPORTS: list[Report] = _generate_reports()


def all_reports() -> list[Report]:
    """Return the full seed dataset (do not mutate the returned list)."""

    return list(REPORTS)
