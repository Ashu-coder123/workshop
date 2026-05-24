## 1. Backend CSV Streaming Implementation

- [x] 1.1 Implement GET endpoint `/reports/export` in `app/main.py`
- [x] 1.2 Use FastAPI's StreamingResponse and csv.writer to stream CSV lines
- [x] 1.3 Parse and apply status, date, sort, and pagination parameters to query results

## 2. Frontend Button and Integration

- [x] 2.1 Add an "Export CSV" button in the dashboard page header within `app/static/index.html`
- [x] 2.2 Style the button using premium glassmorphic/vibrant colors in `index.html`'s `<style>` block
- [x] 2.3 Implement the JavaScript click listener to redirect browser to `/reports/export` with active filter and sort queries

## 3. Testing and Validation

- [x] 3.1 Write integration tests in `tests/test_export.py` to assert CSV headers, records count, status filters, sorting, pagination, and CSV escaping edge cases
- [x] 3.2 Run pytest to verify all automated checks pass successfully
