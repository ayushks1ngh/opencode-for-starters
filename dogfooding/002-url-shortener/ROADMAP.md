# Roadmap: URL Shortener SaaS

## Phase 1: MVP (AC-1 through AC-7)
Fundamental URL shortener with redirect, click tracking, and CRUD management.
- [ ] Project skeleton (pyproject.toml, __init__, __main__)
- [ ] Database schema and storage layer
- [ ] Short code generation
- [ ] Server and routing framework
- [ ] Create short URL handler (AC-1)
- [ ] Redirect handler (AC-2, AC-7)
- [ ] Click stats handler (AC-3)
- [ ] List URLs handler (AC-4)
- [ ] Delete URL handler (AC-5)
- [ ] Error handling and 404s
- [ ] Data persistence verification (AC-6)

## Phase 2: Custom Aliases & Expiry
- [ ] Custom alias support (AC from Phase 2 PRD)
- [ ] URL expiry dates
- [ ] Expired URL auto-404

## Phase 3: Analytics & Accounts
- [ ] Click analytics over time (daily breakdown)
- [ ] User authentication and accounts
- [ ] Per-user URL namespacing

## Effort Estimates
- Phase 1: ~3-4 hours implementation
- Phase 2: ~2 hours
- Phase 3: ~4-5 hours
