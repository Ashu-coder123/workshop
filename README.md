# Reports API

A small FastAPI service that exposes a paginated `/reports` endpoint backed by a deterministic in-memory dataset.

## Layout

```
app/
├── __init__.py
├── data.py        # Seed dataset (120 rows, deterministic)
├── models.py      # Pydantic models — internal vs public
├── reports.py     # Filter / sort / pagination query layer
└── main.py        # FastAPI HTTP layer
```

## Requirements

- Python 3.10+
- pip

## Setup

```bash
git clone https://github.com/IITMBSMLOps/SpecDrivenDevelopmentBase.git
cd SpecDrivenDevelopmentBase

python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -e .
```

## Run the API

```bash
uvicorn app.main:app --reload --port 8000
```

Then hit it from another terminal:

```bash
curl "http://localhost:8000/health"
curl "http://localhost:8000/reports?limit=3" | python -m json.tool
```

## Endpoints

| Method | Path       | Description                                            |
| ------ | ---------- | ------------------------------------------------------ |
| GET    | `/health`  | Liveness probe — returns `{"status": "ok"}`.           |
| GET    | `/reports` | Paginated list of reports with filtering and sorting.  |

### `GET /reports` query parameters

| Param        | Type            | Default      | Notes                                            |
| ------------ | --------------- | ------------ | ------------------------------------------------ |
| `status`     | enum            | —            | One of `pending`, `approved`, `rejected`, `archived`. |
| `date_from`  | datetime (ISO)  | —            | Lower bound on `created_at` (inclusive).         |
| `date_to`    | datetime (ISO)  | —            | Upper bound on `created_at` (inclusive).         |
| `sort`       | string          | `created_at` | One of `id`, `title`, `status`, `owner`, `amount`, `created_at`. |
| `descending` | bool            | `true`       | Sort direction.                                  |
| `offset`     | int (>=0)       | `0`          | Pagination offset.                               |
| `limit`      | int (1..200)    | `20`         | Page size.                                       |

