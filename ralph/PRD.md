# PRD

Status: ready

## Overview

An AI-supercharged PMO assistant that treats Markdown files as the canonical source of truth, runs 100% locally, uses a local web app UI as a projection layer, and uses AI to maintain, summarize, forecast, and coordinate work.

**Core thesis:** "Git for project management + AI chief of staff"

## Goals

1. **Local-first, file-native architecture**
   - Everything lives as `.md` files in a workspace
   - Full git compatibility (diff, grep, backup)
   - No vendor lock-in

2. **PMO-centric data model**
   - Focus on goals, dependencies, risks, decisions, progress narratives
   - Tickets are a detail, not the core abstraction

3. **AI as maintainer, not dictator**
   - AI writes to Markdown files directly
   - All changes show diffs before applying
   - Explainable outputs with file references
   - Reversible changes

4. **PMO-grade AI capabilities**
   - Executive summaries from project state
   - Drift detection (goals vs milestones, stale risks, orphaned dependencies)
   - Meeting notes → structured updates (risks, decisions, status)
   - Forecasting and blocker identification via dependency DAG
   - Inline AI suggestions in markdown editor

5. **Web UI as projection layer**
   - Dashboard (portfolio health, top risks, decision deadlines)
   - Project views (narrative, timeline, dependency graph)
   - AI inbox (actionable alerts)
   - File-native editor with diff viewer
   - Every UI element maps to `.md` file locations

## Non-Goals

1. **Not a chatbot** - AI edits files, not just conversational
2. **Not a ticket tracker** - PMO narrative first, tickets secondary
3. **Not a Notion/Jira clone** - Local-first, file-native, no cloud dependency
4. **Not a team collaboration platform (MVP)** - Phase 1 is solo PM/founder focused
5. **No external server required** - Runs entirely on localhost

## Requirements

### Phase 1: MVP (Solo PM / Founder)

#### Workspace Structure
- Markdown workspace with folders: `/projects/`, `/epics/`, `/decisions/`, `/risks/`, `/meetings/`, `/people/`, `/logs/`
- Standardized frontmatter schemas for each file type

#### Data Model (Markdown Conventions)
- **Project files**: id, owner, status, start, target dates; Goal, Current Status, Milestones, Dependencies, Risks, Last Updated
- **Risk files**: id, severity, probability, owner; Description, Impact, Mitigation, Status
- **Decision files**: id, date, owner; Context, Decision, Consequences

#### Local Backend (Daemon)
- File indexing (watchdog/fsnotify)
- Semantic embedding (local model)
- Task graph building from dependencies
- AI execution with prompt templates bound to file schemas
- Diff + patch application (strict input/output contracts)
- Runs on `localhost:PORT`, no external server

#### AI Capabilities
- PMO-grade summaries (reads milestones, risks, meetings → 1-page narrative)
- Drift detection (goals vs milestones, stale risks, orphaned dependencies)
- Meeting → structured updates (extract risks, decisions, status changes)
- Forecasting ("what's blocking us" via dependency DAG)
- AI as editor (show diff, approve → patch applied)

#### Web UI
- PMO Dashboard (portfolio health, R/Y/G projects, top risks, decision deadlines)
- Project View (narrative status, timeline, dependencies graph, linked risks/decisions)
- AI Inbox ("things you should look at" alerts)
- File-native Markdown editor (Monaco) with AI suggestions inline
- Diff viewer for AI-proposed changes
- "Open in folder" always one click away

#### Technical Stack
- Backend: Python or Go
- File watching: watchdog/fsnotify
- Indexing: SQLite
- Embeddings: local model (small transformer)
- LLM: Local (Ollama/LM Studio) with optional cloud fallback
- Frontend: React + Vite, Tailwind, Monaco editor

### Phase 2: Real PMO Power (Future)
- Dependency graph visualization
- Risk scoring algorithms
- Meeting ingestion (transcript parsing)
- Advanced forecasting

### Phase 3: Team Scale (Future)
- Multi-person ownership
- Git-based collaboration
- Review/approval flows

### Phase 4: Org Brain (Future)
- Cross-project insights
- Pattern mining across history
- "Why are we slow?" analysis

## Success Metrics

### MVP Success Criteria
1. **File-native workflow**: User can manage entire PMO via markdown files + git
2. **AI accuracy**: AI-generated summaries accurately reflect project state (manual validation)
3. **Drift detection**: System identifies stale risks/dependencies within 24h of threshold
4. **Meeting ingestion**: AI correctly extracts and structures 80%+ of meeting notes into risks/decisions/status
5. **Forecasting utility**: Dependency DAG correctly identifies top 3 blockers in test scenarios
6. **Performance**: Dashboard loads in <2s, AI summaries generate in <10s
7. **Offline capability**: Full functionality without internet (local LLM)

### User Experience
- User can open workspace in VS Code and understand structure
- Every UI action has clear file location mapping
- AI changes are always reviewable via diff before applying
- No data loss risk (git-backed)

## Open Questions

1. **LLM choice for MVP**: Local-only (Ollama) vs hybrid (local + cloud fallback)? Performance vs capability tradeoff.
2. **Embedding model**: Which local transformer model for semantic search? Size vs accuracy tradeoff.
3. **File schema versioning**: How to handle schema evolution as requirements change?
4. **Conflict resolution**: If user edits file while AI is processing, how to handle?
5. **Workspace initialization**: Default folder structure vs user-configurable?
6. **Port selection**: Fixed port vs auto-detect available port?
7. **Backend language**: Python (easier AI integration) vs Go (performance, single binary)?
8. **UI framework**: React vs Svelte? (Design doc mentions both)
9. **Monaco editor**: Full Monaco vs lighter markdown editor for MVP?
10. **Testing strategy**: How to test AI outputs deterministically?
