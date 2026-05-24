## Why

Users of the Reports Dashboard need to export expense and operational summaries to a CSV file for offline analysis, spreadsheet manipulation, or reporting purposes.

## What Changes

- Add a backend REST endpoint (`/reports/export`) to query, filter, sort, and stream report data as a CSV file.
- Add an "Export CSV" button to the front-end dashboard UI that downloads the CSV file with the active filters and sort criteria applied.

## Capabilities

### New Capabilities
- `csv-export`: Enables the retrieval and download of reports dataset as a CSV file, supporting the same query filters and sorting fields as the paginated list view.

### Modified Capabilities
<!-- Leave empty as no existing spec-level behaviors are changing -->

## Impact

- **Backend**: FastAPI app (`app/main.py`) to expose the `/reports/export` endpoint using a streaming CSV generator response.
- **Frontend**: The static dashboard (`app/static/index.html`) to include the "Export CSV" button, associated styling, and client-side integration to download the CSV.
