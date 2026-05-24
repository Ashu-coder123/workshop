import csv
import io
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    """Verify health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_serve_dashboard():
    """Verify that root URL serves the SPA HTML dashboard page."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "<title>Reports Dashboard</title>" in response.text

def test_csv_export_basic():
    """Verify basic CSV export returns correct status, headers, and media type."""
    response = client.get("/reports/export")
    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]
    assert 'attachment; filename="reports.csv"' in response.headers["content-disposition"]
    
    # Parse CSV contents
    content = response.text
    reader = csv.reader(io.StringIO(content))
    rows = list(reader)
    
    # Check headers (must contain public fields, and NOT contain internal ones)
    assert len(rows) > 0
    headers = rows[0]
    assert headers == ["id", "title", "status", "owner", "amount", "created_at"]
    
    # Check that we got all 120 reports
    assert len(rows) == 121  # 1 header + 120 rows

def test_csv_export_filtering_status():
    """Verify status filtering works for CSV export."""
    # Filter by approved
    response = client.get("/reports/export?status=approved")
    assert response.status_code == 200
    
    reader = csv.reader(io.StringIO(response.text))
    rows = list(reader)
    
    # All rows (except header) should have "approved" status
    for row in rows[1:]:
        assert row[2] == "approved"

    # Filter by pending
    response2 = client.get("/reports/export?status=pending")
    assert response2.status_code == 200
    reader2 = csv.reader(io.StringIO(response2.text))
    rows2 = list(reader2)
    for row in rows2[1:]:
        assert row[2] == "pending"

def test_csv_export_filtering_date():
    """Verify date filtering works for CSV export."""
    # Date window: let's fetch reports from 2026-02-01T00:00:00Z to 2026-02-15T23:59:59Z
    response = client.get("/reports/export?date_from=2026-02-01T00:00:00Z&date_to=2026-02-15T23:59:59Z")
    assert response.status_code == 200
    
    reader = csv.reader(io.StringIO(response.text))
    rows = list(reader)
    
    for row in rows[1:]:
        created_at_str = row[5]
        # It should be within the range
        assert created_at_str >= "2026-02-01T00:00:00"
        assert created_at_str <= "2026-02-15T23:59:59"

def test_csv_export_sorting():
    """Verify sorting behaves as expected in the CSV."""
    # Sort by amount ascending
    response = client.get("/reports/export?sort=amount&descending=false")
    assert response.status_code == 200
    
    reader = csv.reader(io.StringIO(response.text))
    rows = list(reader)
    
    amounts = [float(row[4]) for row in rows[1:]]
    assert len(amounts) > 0
    # Amounts should be sorted ascending
    assert amounts == sorted(amounts)

    # Sort by amount descending
    response2 = client.get("/reports/export?sort=amount&descending=true")
    assert response2.status_code == 200
    reader2 = csv.reader(io.StringIO(response2.text))
    rows2 = list(reader2)
    amounts2 = [float(row[4]) for row in rows2[1:]]
    assert amounts2 == sorted(amounts2, reverse=True)

def test_csv_export_pagination():
    """Verify limit and offset pagination work on CSV export."""
    # Fetch first page of 5 items
    response = client.get("/reports/export?limit=5&offset=0&sort=id&descending=false")
    assert response.status_code == 200
    reader = csv.reader(io.StringIO(response.text))
    rows = list(reader)[1:]  # strip header
    assert len(rows) == 5
    first_page_ids = [int(row[0]) for row in rows]
    
    # Fetch second page of 5 items
    response2 = client.get("/reports/export?limit=5&offset=5&sort=id&descending=false")
    assert response2.status_code == 200
    reader2 = csv.reader(io.StringIO(response2.text))
    rows2 = list(reader2)[1:]
    assert len(rows2) == 5
    second_page_ids = [int(row[0]) for row in rows2]
    
    # Check that they don't overlap and represent sequential paging
    assert first_page_ids == [1, 2, 3, 4, 5]
    assert second_page_ids == [6, 7, 8, 9, 10]

def test_csv_export_escaping_edge_cases():
    """Verify that title with commas, quotes, and newlines is exported correctly without breaking CSV structure."""
    response = client.get("/reports/export")
    assert response.status_code == 200
    
    content = response.text
    # Parse with standard csv.reader
    reader = csv.reader(io.StringIO(content))
    rows = list(reader)
    
    # Find the row containing our complex title
    target_row = None
    for row in rows:
        if 'CSV with commas, "quotes" and newlines' in row[1]:
            target_row = row
            break
            
    assert target_row is not None, "Edge case title not found in CSV"
    
    # The title should match the expected string with its newline
    assert target_row[1] == 'CSV with commas, "quotes" and newlines\nin the title'
    # Ensure columns count matches header (6 fields)
    assert len(target_row) == 6
