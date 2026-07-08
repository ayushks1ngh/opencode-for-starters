# Tasks: URL Shortener SaaS

## Phase 1: MVP

### T1.1: Project skeleton — depends_on: none (AC-6)
- [ ] Create directory structure: `url_shortener/`, `tests/`
- [ ] Create `pyproject.toml` with build config
- [ ] Create `url_shortener/__init__.py` with version
- [ ] Create `url_shortener/__main__.py` entry point

### T1.2: Database schema and storage — depends_on: T1.1 (AC-6)
- [ ] Define `links` table schema (id, short_code, target_url, created_at, clicks)
- [ ] Implement `init_db()` — create table on startup
- [ ] Implement `insert_link(short_code, target_url)` — insert, return link
- [ ] Implement `get_link(short_code)` — select by short_code, return link or None
- [ ] Implement `get_all_links()` — select all, return list
- [ ] Implement `delete_link(short_code)` — delete by short_code, return bool
- [ ] Implement `increment_clicks(short_code)` — atomic click increment
- [ ] Handle database errors gracefully

### T1.3: Short code generation — depends_on: T1.1, T1.2 (AC-1)
- [ ] Implement `generate_short_code(length=6)` using secrets.choice
- [ ] Implement `create_unique_code()` — generate and verify uniqueness against DB
- [ ] Retry on collision (up to 5 attempts, then error)

### T1.4: HTTP server and routing — depends_on: T1.1 (AC-1, AC-2, AC-3, AC-4, AC-5)
- [ ] Create `url_shortener/server.py` — http.server.HTTPServer setup
- [ ] Create `url_shortener/router.py` — path/method dispatch to handlers
- [ ] Implement JSON body parsing for POST requests
- [ ] Implement JSON response helper (200, 201, 400, 404, 500)
- [ ] Wire up main loop in `__main__.py` (default port 8080)

### T1.5: Create short URL handler — depends_on: T1.2, T1.3, T1.4 (AC-1)
- [ ] Implement POST /shorten handler
- [ ] Validate URL presence and format
- [ ] Generate short code, store in DB
- [ ] Return 201 with short_code and target_url
- [ ] Return 400 for invalid/missing URL

### T1.6: Redirect handler — depends_on: T1.2, T1.4 (AC-2, AC-7)
- [ ] Implement GET /<short_code> handler
- [ ] Look up short code in DB
- [ ] Increment click counter atomically
- [ ] Return 301 redirect to target_url
- [ ] Return 404 if not found

### T1.7: Click stats handler — depends_on: T1.2, T1.4 (AC-3)
- [ ] Implement GET /<short_code>/stats handler
- [ ] Return short_code, target_url, clicks
- [ ] Return 404 if not found

### T1.8: List URLs handler — depends_on: T1.2, T1.4 (AC-4)
- [ ] Implement GET /urls handler
- [ ] Return list of all URLs with short_code, target_url, clicks
- [ ] Return empty list if none exist

### T1.9: Delete URL handler — depends_on: T1.2, T1.4 (AC-5)
- [ ] Implement DELETE /<short_code> handler
- [ ] Delete from DB
- [ ] Return 200 with confirmation message
- [ ] Return 404 if not found

### T1.10: Error handling and edge cases — depends_on: T1.5, T1.6, T1.7, T1.8, T1.9 (AC-1, AC-2, AC-3, AC-4, AC-5)
- [ ] 404 for unknown routes
- [ ] 400 for invalid JSON body
- [ ] 500 for unhandled exceptions
- [ ] Server start/stop cleanly (Ctrl+C)

## Phase 2: Custom Aliases & Expiry

### T2.1: Custom alias support — depends_on: Phase 1
- [ ] Extend POST /shorten to accept optional `alias` field
- [ ] Validate alias uniqueness
- [ ] Return 409 if alias taken

### T2.2: URL expiry — depends_on: Phase 1
- [ ] Add `expires_at` column to links table
- [ ] Check expiry on redirect, return 410 if expired
- [ ] Extend POST /shorten to accept optional `expires_in_days`

## Phase 3: Analytics & Accounts

### T3.1: Click analytics — depends_on: Phase 1
- [ ] Add clicks_log table (id, short_code, timestamp, referrer, user_agent)
- [ ] Log clicks on redirect
- [ ] Extend stats endpoint with daily breakdown

### T3.2: User accounts — depends_on: T3.1
- [ ] Users table and registration/login
- [ ] Session management
- [ ] Per-user URL scoping
