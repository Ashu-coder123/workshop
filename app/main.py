"""FastAPI HTTP layer for the Reports app."""

from __future__ import annotations

import csv
import io
import os
from datetime import datetime

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from app.models import ReportListResponse, ReportPublic, ReportStatus
from app.reports import query

app = FastAPI(title="SDD Workshop — Reports API", version="0.1.0")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Create static directory if it does not exist
os.makedirs(STATIC_DIR, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def read_root() -> FileResponse:
    """Serve the Reports Dashboard SPA."""
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/reports", response_model=ReportListResponse)
def list_reports(
    status: ReportStatus | None = Query(None, description="Filter by status"),
    date_from: datetime | None = Query(None, description="Lower bound on created_at (inclusive)"),
    date_to: datetime | None = Query(None, description="Upper bound on created_at (inclusive)"),
    sort: str = Query("created_at", description="Sort field"),
    descending: bool = Query(True, description="Sort descending"),
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
) -> ReportListResponse:
    """Return a paginated list of reports.

    Public fields only — `internal_id` and `owner_email` are stripped via
    `ReportPublic.from_internal`.
    """

    try:
        rows = query(
            status=status,
            date_from=date_from,
            date_to=date_to,
            sort=sort,
            descending=descending,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    page = rows[offset : offset + limit]
    return ReportListResponse(
        items=[ReportPublic.from_internal(r) for r in page],
        total=len(rows),
        offset=offset,
        limit=limit,
    )


@app.get("/reports/export")
def export_reports(
    status: ReportStatus | None = Query(None, description="Filter by status"),
    date_from: datetime | None = Query(None, description="Lower bound on created_at (inclusive)"),
    date_to: datetime | None = Query(None, description="Upper bound on created_at (inclusive)"),
    sort: str = Query("created_at", description="Sort field"),
    descending: bool = Query(True, description="Sort descending"),
    offset: int | None = Query(None, ge=0, description="Optional offset for export range"),
    limit: int | None = Query(None, ge=1, le=200, description="Optional limit for export range"),
) -> StreamingResponse:
    """Export filtered and sorted reports as a CSV file.

    Honors public-only field distinction by stripping internal_id and owner_email.
    """
    try:
        rows = query(
            status=status,
            date_from=date_from,
            date_to=date_to,
            sort=sort,
            descending=descending,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    # Apply pagination only if offset or limit are explicitly passed
    if offset is not None or limit is not None:
        start = offset or 0
        end = (start + limit) if limit is not None else len(rows)
        page = rows[start:end]
    else:
        page = rows

    public_reports = [ReportPublic.from_internal(r) for r in page]

    def csv_generator():
        output = io.StringIO()
        writer = csv.writer(output, lineterminator="\n")
        # Write header
        writer.writerow(["id", "title", "status", "owner", "amount", "created_at"])
        yield output.getvalue()
        output.seek(0)
        output.truncate(0)

        for r in public_reports:
            writer.writerow([
                r.id,
                r.title,
                r.status,
                r.owner,
                f"{r.amount:.2f}",
                r.created_at.isoformat(),
            ])
            yield output.getvalue()
            output.seek(0)
            output.truncate(0)

    headers = {"Content-Disposition": 'attachment; filename="reports.csv"'}
    return StreamingResponse(csv_generator(), media_type="text/csv", headers=headers)
