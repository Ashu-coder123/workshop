# csv-export Specification

## Purpose
TBD - created by archiving change add-csv-export. Update Purpose after archive.
## Requirements
### Requirement: CSV Export Backend Endpoint
The system SHALL expose a GET endpoint at `/reports/export` that accepts the following query parameters: `status`, `date_from`, `date_to`, `sort`, `descending`, `offset`, and `limit`. The endpoint SHALL return a streamed response with a `text/csv` media type containing the filtered and sorted report data. The CSV data columns MUST be `id`, `title`, `status`, `owner`, `amount`, and `created_at`. Internal details such as `internal_id` and `owner_email` SHALL be omitted from the exported data.

#### Scenario: Successful CSV Download with Filters
- **WHEN** a GET request is sent to `/reports/export` with a status filter of "approved"
- **THEN** the system returns a 200 response with `Content-Disposition` set to attachment filename `reports.csv` containing only reports with "approved" status.

### Requirement: CSV Export Dashboard UI Button
The frontend dashboard user interface SHALL display an "Export CSV" button in the page header. Clicking this button SHALL trigger a download of the CSV data by executing a client-side request to `/reports/export` incorporating the active UI filters and sorting criteria.

#### Scenario: Clicking Export CSV Button
- **WHEN** the user clicks the "Export CSV" button on the dashboard
- **THEN** the browser triggers a download of the `reports.csv` file containing the data currently filtered and sorted on the UI table.

