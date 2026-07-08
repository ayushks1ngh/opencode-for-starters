# Build Brief: Phase 1 — MVP

## Phase Scope
Build a functional URL shortener with HTTP API, SQLite storage, and click tracking. No authentication, no analytics dashboard, no custom aliases.

## Tasks (in dependency order)

1. **T1.1: Project skeleton** — `pyproject.toml`, `__init__.py`, `__main__.py`
2. **T1.2: Database + storage** — SQLite schema, CRUD operations
3. **T1.3: Short code generation** — random code + collision check
4. **T1.4: HTTP server + router** — request dispatch framework
5. **T1.5: Create handler** — POST /shorten
6. **T1.6: Redirect handler** — GET /<code> with click tracking
7. **T1.7: Stats handler** — GET /<code>/stats
8. **T1.8: List handler** — GET /urls
9. **T1.9: Delete handler** — DELETE /<code>
10. **T1.10: Error handling polish**

## Acceptance Criteria to Satisfy
- AC-1: Create short URL (T1.5)
- AC-2: Redirect short URL (T1.6)
- AC-3: View click count (T1.7)
- AC-4: List URLs (T1.8)
- AC-5: Delete URL (T1.9)
- AC-6: Data persistence across restarts (T1.2)
- AC-7: Click tracking (T1.6)

## Architecture Essentials

### Key files
- `url_shortener/server.py` — HTTP server setup on port 8080
- `url_shortener/router.py` — path-based dispatch
- `url_shortener/handlers.py` — business logic per endpoint
- `url_shortener/storage.py` — SQLite wrapper
- `url_shortener/shortcode.py` — secret-based code generation

### Data model
```sql
CREATE TABLE links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    short_code TEXT UNIQUE NOT NULL,
    target_url TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    clicks INTEGER NOT NULL DEFAULT 0
);
```

### API endpoints
| Method | Path | Handler | Response |
|--------|------|---------|----------|
| POST | /shorten | create | 201 + short_code |
| GET | /<code> | redirect | 301 to target |
| GET | /<code>/stats | stats | 200 + click count |
| GET | /urls | list | 200 + all URLs |
| DELETE | /<code> | delete | 200 + confirmation |

### Port
- Default: 8080
- Configurable via environment variable `PORT`

## Known Plan Gaps
- No test specification yet (covered in future phases)
- Server shutdown cleanup (ensure SQLite connection closed)
- Port conflict handling (what if 8080 is in use)
