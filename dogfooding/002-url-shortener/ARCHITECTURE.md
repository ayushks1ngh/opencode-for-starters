# Architecture: URL Shortener SaaS

## Tech Stack
- Language: Python 3.8+
- HTTP server: `http.server` (stdlib)
- Database: SQLite via `sqlite3` (stdlib)
- Dependencies: None
- Testing: pytest

## System Design

```
HTTP Request
    │
    ▼
Router (parse path + method)
    │
    ├── POST /shorten  →  CreateHandler
    ├── GET /<code>    →  RedirectHandler
    ├── GET /<code>/stats → StatsHandler
    ├── GET /urls      →  ListHandler
    ├── DELETE /<code> →  DeleteHandler
    └── *              →  404 Handler
                              │
                              ▼
                        Database Layer (SQLite)
                              │
                              ├── links table
                              └── clicks table (or counter column)
```

## Data Model

### links table
```sql
CREATE TABLE links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    short_code TEXT UNIQUE NOT NULL,
    target_url TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    clicks INTEGER NOT NULL DEFAULT 0
);
```

No separate clicks table for MVP. Click count is an integer column on links. This avoids JOINs for the MVP while keeping the schema simple.

## API Design

All responses are JSON with `Content-Type: application/json`.

### POST /shorten
Request: `{"url": "https://..."}`
Response 201: `{"short_code": "abc123", "target_url": "https://..."}`
Response 400: `{"error": "Missing or invalid URL"}`

### GET /<short_code>
Response 301: Redirect to target_url
Response 404: `{"error": "Short code not found"}`

### GET /<short_code>/stats
Response 200: `{"short_code": "abc123", "target_url": "https://...", "clicks": 42}`
Response 404: `{"error": "Short code not found"}`

### GET /urls
Response 200: `{"urls": [{"short_code": "abc123", "target_url": "...", "clicks": 42}]}`

### DELETE /<short_code>
Response 200: `{"message": "Deleted abc123"}`
Response 404: `{"error": "Short code not found"}`

## Short Code Generation
- 6 alphanumeric characters (a-z, A-Z, 0-9)
- Randomly generated using `secrets.choice`
- Collision check before insert (retry on collision)
- 62^6 = ~56 billion combinations — collision risk is negligible

## Project Structure

```
url_shortener/
  __init__.py        # package marker, version
  __main__.py        # entry point: python -m url_shortener
  server.py          # HTTP server setup and main loop
  router.py          # URL routing and handler dispatch
  handlers.py        # Request handlers for each endpoint
  storage.py         # SQLite database operations
  models.py          # Data models and validation
  shortcode.py       # Short code generation
tests/
  test_handlers.py
  test_storage.py
  test_shortcode.py
pyproject.toml       # packaging config
```

## Data Flow

```
Client → HTTP Request → server.py (http.server) → router.py (parse path)
    → handlers.py (business logic) → storage.py (SQLite) → JSON response → Client
```

## Error Handling
- Invalid JSON body → 400 `{"error": "Invalid JSON"}`
- Missing URL field → 400 `{"error": "Missing or invalid URL"}`
- Short code not found → 404 `{"error": "Short code not found"}`
- Server error → 500 `{"error": "Internal server error"}`
- Database errors → logged, returned as 500

## Performance Notes (MVP)
- SQLite is single-writer — sufficient for single-server MVP
- No caching layer (add Redis in Phase 2 if needed)
- Redirect is synchronous — acceptable for MVP latency
