# ROADMAP: Memory-Enabled Agent Chatbot

## Phases

### Phase 1 (MVP): Core Chat Loop
**ACs covered**: AC-1, AC-2, AC-3, AC-4, AC-5, AC-6, AC-7
**Effort**: ~8 hours
**Deliverables**: Working CLI chatbot with memory, tools, retry, and error recovery

Tasks:
- T1.1–T1.4: Data models + persistence (AC-4)
- T1.5–T1.6: Session management (AC-1)
- T1.7–T1.9: LLM provider + retry (AC-2, AC-5)
- T1.10–T1.13: Tool framework + built-in tools (AC-3, AC-6, AC-7)
- T1.14–T1.15: Orchestrator + CLI (AC-2, AC-7)
- T1.16: Verification

### Phase 2 (Future): Advanced Features
- Streaming responses
- Multiple simultaneous sessions
- Plugin system for dynamic tool loading
- Vector-based memory retrieval
- Web UI

## Dependencies

Phase 2 depends on Phase 1 completion. No external dependencies on other phases.

## Milestones

| Milestone | Phase | Criteria |
|-----------|-------|----------|
| M1: Models + Persistence | P1 | All 4 data models + JSON persistence with append/get |
| M2: Session Management | P1 | create/list/resume/delete sessions, active session tracking |
| M3: LLM Integration | P1 | Provider abstraction + retry handler + basic chat |
| M4: Tool Framework | P1 | Tool protocol + registry + calculator + current_time |
| M5: Full Orchestration | P1 | Message loop with tool calling + error recovery |
| M6: CLI + Verification | P1 | Working REPL, all ACs verified |
