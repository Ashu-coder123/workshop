## Context

The Reports Dashboard application currently shows a paginated table of expense reports. While users can filter, sort, and paginate reports in the UI, they cannot download/export the data for external auditing, spreadsheet tasks, or offline storage. 

## Goals / Non-Goals

**Goals:**
- Implement a backend CSV generation route `/reports/export` that mirrors the filter and sort criteria of the main list API.
- Strip sensitive/internal fields (`internal_id`, `owner_email`) from the exported dataset.
- Stream the CSV response to minimize memory usage on the server.
- Add an interactive button in the dashboard UI header to trigger the CSV download seamlessly.

**Non-Goals:**
- Implementing multiple export formats (e.g., PDF, XLSX).
- Asynchronous export processing (e.g., job queues, email notifications).
- Adding custom column selection to the export interface.

## Decisions

### 1. Streamed CSV generation via FastAPI StreamingResponse
- **Decision**: We will generate CSV lines on-the-fly using a generator function that yields rows to a `StreamingResponse` object in chunks.
- **Rationale**: Avoids allocating large string buffers in memory on the server, which keeps resource utilization low and scales better with large datasets.
- **Alternatives Considered**: In-memory CSV generation using `io.StringIO` and returning a standard `Response`. Rejected because it scales poorly for large datasets.

### 2. Standard browser download trigger
- **Decision**: The "Export CSV" button will set `window.location.href` to the `/reports/export` endpoint with matching query parameters.
- **Rationale**: Leverages native browser handling for file downloads (Content-Disposition attachments) with minimal client-side overhead.
- **Alternatives Considered**: Triggering a `fetch` request, converting the response to a Blob, and injecting a virtual link tag to trigger a download. Rejected as it adds unnecessary complexity to the client-side JavaScript.

## Risks / Trade-offs

- **Risk**: Exporting very large datasets could result in slow downloads or timeout errors.
  - **Mitigation**: The backend supports pagination parameters (`limit` and `offset`) for the export endpoint. If a user needs a subset, the UI can pass those. By default, it retrieves the full set without pagination to ensure all filtered rows are exported.
