# PRD: URL Shortener SaaS

## Problem Statement
Sharing long URLs in chat messages, emails, and documents is cumbersome. Existing URL shorteners (bit.ly, TinyURL) work but require third-party trust, have rate limits, and offer no local control. Users need a self-hosted or locally deployable URL shortener with basic analytics.

## Target Audience
- Developers who want a self-hosted URL shortener
- Teams who want internal link management
- Anyone who needs short links with click tracking

## User Stories

### MVP (Phase 1)
1. As a user, I can create a short URL from a long URL so I can share compact links
2. As a user, I can visit a short URL and get redirected to the original URL so links work
3. As a user, I can see how many times a short URL was clicked so I can measure engagement
4. As a user, I can list all my short URLs so I can manage them
5. As a user, I can delete a short URL so I can remove unwanted links

### Phase 2
6. As a user, I can set a custom alias for my short URL so I can brand my links
7. As a user, I can set an expiry date for a short URL so links auto-disable

### Phase 3
8. As a user, I can view a dashboard with click analytics over time so I can see trends
9. As a user, I can create an account so my URLs are private to me

## Acceptance Criteria

### AC-1 (Phase 1): Create short URL
- `POST /shorten` with `{"url": "https://example.com/very/long/path"}` returns `{"short_code": "abc123", "target_url": "..."}`
- Short code is 6 alphanumeric characters, randomly generated
- Duplicate long URLs produce different short codes (each shorten creates a new entry)
- Returns 400 if URL is missing or invalid

### AC-2 (Phase 1): Redirect short URL
- `GET /abc123` returns HTTP 301 redirect to `https://example.com/very/long/path`
- `GET /nonexistent` returns HTTP 404
- Redirect preserves query parameters on target URL (if any)

### AC-3 (Phase 1): View click count
- `GET /abc123/stats` returns `{"short_code": "abc123", "target_url": "...", "clicks": 42}`
- Returns 404 if short code doesn't exist

### AC-4 (Phase 1): List URLs
- `GET /urls` returns `{"urls": [{"short_code": "abc123", "target_url": "...", "clicks": 42}, ...]}`
- Returns empty list if no URLs exist

### AC-5 (Phase 1): Delete URL
- `DELETE /abc123` returns 200 with confirmation
- `DELETE /nonexistent` returns 404
- After deletion, redirect returns 404

### AC-6 (Phase 1): Persistence
- All data persists across server restarts
- Storage is SQLite database in a local file

### AC-7 (Phase 1): Click tracking
- Every redirect increments the click counter for that short code
- Click counter is never decremented
- Click counter persists across restarts

## Non-Requirements (MVP)
- No user authentication or accounts
- No analytics dashboard or charts
- No QR code generation
- No custom aliases
- No rate limiting
- No HTTPS (HTTP only for MVP)
- No clustering or multi-node support
- No API keys

## Technology Constraints
- Zero external dependencies for MVP (stdlib only)
- SQLite for storage
- Python 3.8+
