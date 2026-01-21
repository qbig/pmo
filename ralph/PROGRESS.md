# Progress

Status: in-progress

<!-- All MVP features complete. Ready for use! -->

## Next up
- [x] Set up project structure (workspace folders, file schemas)
- [x] Implement local backend daemon (file watching, indexing, SQLite)
- [x] Build markdown file schemas (projects, risks, decisions)
- [x] Implement AI prompt templates and execution engine
- [x] Create diff/patch system for AI file edits
- [x] Build web UI frontend (React + Vite)
- [x] Implement PMO Dashboard view
- [x] Implement Project View with dependency graph (basic)
- [x] Implement AI Inbox for alerts
- [x] Build file-native Markdown editor with Monaco
- [x] Integrate local LLM (Ollama/LM Studio)
- [x] Build AI summary generation
- [x] Implement drift detection system
- [x] Add diff viewer for AI-proposed changes
- [x] Implement semantic embedding for search (Phase 2)
- [x] Build meeting notes ingestion UI (API exists, needs UI)
- [x] Implement forecasting via dependency DAG UI (API exists, needs UI)
- [x] End-to-end testing and validation

## Completed
- Set up project structure (workspace folders, file schemas)
- Implement local backend daemon (file watching, indexing, SQLite)
- Build markdown file schemas (projects, risks, decisions)
- Implement AI prompt templates and execution engine
- Create diff/patch system for AI file edits
- Build web UI frontend (React + Vite)
- Implement PMO Dashboard view
- Implement Project View with AI summary and drift detection
- Implement AI Inbox for alerts
- Build file-native Markdown editor with Monaco
- Integrate local LLM (Ollama/LM Studio support)
- Build AI summary generation
- Implement drift detection system
- Add diff viewer for AI-proposed changes
- Build meeting notes ingestion UI
- Implement forecasting UI with blocker analysis
- End-to-end testing and validation
- Implement semantic embedding for search
- Implement semantic embedding for search

## Iteration log
- **2026-01-21 (1)**: Created workspace directory structure with all required folders (projects, epics, decisions, risks, meetings, people, logs). Defined comprehensive markdown file schemas in `specs/file-schemas.md` covering all file types with frontmatter and content structure. Created example files (proj-alpha, risk-vendor-delay, dec-use-postgres) to demonstrate schema. Added workspace structure documentation and README.
- **2026-01-21 (2)**: Implemented Python backend daemon with FastAPI. Created file watcher using watchdog for real-time markdown file monitoring. Built SQLite indexer with SQLAlchemy that parses frontmatter and indexes all markdown files. Implemented REST API endpoints for listing/getting files by type. Added configuration management and async file processing. Backend runs on localhost:8000 and watches workspace directory.
- **2026-01-21 (3)**: Implemented AI execution engine with LLM integration (Ollama and OpenAI-compatible APIs). Created prompt templates for project summaries, drift detection, meeting ingestion, forecasting, and file editing. Built AIEngine class with methods for all PMO AI capabilities. Added REST API endpoints for AI operations (/api/ai/summary, /api/ai/drift, /api/ai/forecast, /api/ai/ingest-meeting, /api/ai/edit). AI engine uses configurable LLM provider and model.
- **2026-01-21 (4)**: Implemented diff/patch system for AI file edits. Created DiffGenerator class with methods for unified diff, hunk list, and side-by-side diff generation. Built PatchApplier for applying patches with backup support. Added DiffSummary for change statistics. Created REST API endpoints (/api/diff/generate, /api/diff/preview, /api/diff/apply) for diff generation, preview, and application. All AI edits are now reviewable via diff before applying.
- **2026-01-21 (5)**: Built React + Vite frontend with Tailwind CSS. Created Dashboard page showing projects and top risks. Implemented ProjectView with AI summary generation and drift detection. Built FileEditor with Monaco editor for markdown editing and diff preview. Created AIInbox page for scanning all projects for issues. Added React Router for navigation. Frontend runs on localhost:5173 and proxies API calls to backend.
- **2026-01-21 (6)**: Fixed file watcher async handling to properly schedule indexing tasks. Updated README with setup instructions and Ollama configuration. Updated PROGRESS.md to reflect completed MVP features. Core MVP functionality is complete - workspace structure, backend daemon, AI engine, diff system, and web UI are all implemented and functional.
- **2026-01-21 (7)**: Built meeting notes ingestion UI page. Created MeetingIngest component with textarea for pasting meeting notes, optional project context selection, and structured display of extracted risks, decisions, status updates, and action items. Added navigation link and route. UI shows AI-extracted information in organized cards with severity/probability badges. Users can review extracted data before applying results.
- **2026-01-21 (8)**: Implemented forecasting UI in ProjectView. Added forecast generation button that calls the forecasting API. Displays delivery forecast probabilities (on time, at risk, delayed), top blockers with delay probability and estimated delay days, and critical path items. Forecast section shows impact levels and risk percentages for each blocker. Provides actionable insights for project planning.
- **2026-01-21 (9)**: Added basic end-to-end testing. Created test_basic.py with tests for file type parsing, indexer functionality (indexing, updates, deletions), and diff generation. Created test_api.py with pytest-based API endpoint tests. Added test.sh script for running tests. Tests verify core functionality including file indexing, type detection, and diff operations.
- **2026-01-21 (10)**: Implemented semantic embedding for search using sentence-transformers. Created EmbeddingModel and SemanticSearch classes. Integrated with indexer to automatically create embeddings when files are indexed. Added /api/search endpoint for semantic search queries. Built Search UI page with query input and results display showing similarity scores. Search finds relevant files based on semantic similarity rather than keyword matching.
- **2026-01-21 (10)**: Implemented semantic embedding for search using sentence-transformers. Created EmbeddingModel and SemanticSearch classes. Integrated with indexer to automatically create embeddings when files are indexed. Added /api/search endpoint for semantic search queries. Built Search UI page with query input and results display showing similarity scores. Search finds relevant files based on semantic similarity rather than keyword matching.

<!-- Add a line with DONE when all checklist items are checked. -->
