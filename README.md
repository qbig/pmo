# PMO Assistant

An AI-supercharged PMO assistant that treats Markdown files as the canonical source of truth.

## Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+ (for frontend)
- Ollama (for local LLM) - [Install Ollama](https://ollama.ai)

### Setup

**Backend:**
```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install backend dependencies
cd src/backend
pip install -r requirements.txt

# Optional: Install sentence-transformers for semantic search
pip install sentence-transformers
```

**Frontend:**
```bash
# Install frontend dependencies
cd src/frontend
npm install
```

### Running

**Terminal 1 - Backend:**
```bash
# Activate virtual environment if using one
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run backend
cd src/backend
python -m src.backend.main
# Backend runs on http://localhost:8000
```

**Terminal 2 - Frontend:**
```bash
cd src/frontend
npm run dev
# Frontend runs on http://localhost:5173
```

Open http://localhost:5173 in your browser.

### Configuration

Set environment variables for LLM configuration:

```bash
export PMO_LLM_PROVIDER=ollama  # or "openai"
export PMO_LLM_MODEL=llama2     # or your preferred model
export PMO_LLM_BASE_URL=http://localhost:11434  # Ollama default
export PMO_PORT=8000            # Backend port
```

### Using Ollama

1. Install Ollama: https://ollama.ai
2. Pull a model: `ollama pull llama2`
3. Start Ollama: `ollama serve` (runs on port 11434 by default)
4. The backend will connect automatically

### Testing

Validate project structure:
```bash
python3 validate.py
```

Run basic tests (requires dependencies installed):
```bash
# Activate virtual environment first
source venv/bin/activate
cd src/backend
PYTHONPATH=../../ python test_basic.py
```

Or use the test script:
```bash
./test.sh
```

## Workspace

The PMO workspace lives in `./workspace/` and contains markdown files organized by type:
- `projects/` - Project files
- `epics/` - Epic files
- `decisions/` - Decision log
- `risks/` - Risk register
- `meetings/` - Meeting notes
- `people/` - People/team files
- `logs/` - Activity logs

See `specs/file-schemas.md` for file format documentation.

## Features

- **Local-first**: All data stored as markdown files in `workspace/`
- **File watching**: Automatic indexing of markdown files
- **AI-powered**: Project summaries, drift detection, forecasting, meeting ingestion
- **Semantic search**: Find files by meaning, not just keywords
- **Diff preview**: Review all AI edits before applying
- **Web UI**: Modern React interface for all operations

## Architecture

- **Backend**: Python daemon (FastAPI, file watching, SQLite indexing, AI execution)
- **Frontend**: React + Vite web UI with Tailwind CSS
- **Storage**: Markdown files + SQLite index (`.pmo.db` in workspace)
- **AI**: Local LLM (Ollama/LM Studio) with optional OpenAI-compatible API fallback
- **Search**: Semantic embeddings using sentence-transformers (optional)

## API Endpoints

- `GET /api/files` - List all files
- `GET /api/files/{id}` - Get file by ID
- `GET /api/projects` - List projects
- `GET /api/risks` - List risks
- `GET /api/ai/summary/{project_id}` - Generate project summary
- `GET /api/ai/drift/{project_id}` - Detect project drift
- `POST /api/ai/forecast/{project_id}` - Forecast blockers
- `POST /api/ai/ingest-meeting` - Extract info from meeting notes
- `POST /api/search` - Semantic search
- `POST /api/diff/preview/{file_id}` - Preview file changes
- `POST /api/diff/apply/{file_id}` - Apply file changes

## Development

See `ralph/PRD.md` for full requirements and `ralph/PROGRESS.md` for current status.

## Troubleshooting

**Backend won't start:**
- Ensure all dependencies are installed: `pip install -r src/backend/requirements.txt`
- Check Python version: `python3 --version` (needs 3.9+)
- Verify workspace directory exists: `ls workspace/`

**Frontend won't start:**
- Ensure Node.js is installed: `node --version` (needs 18+)
- Install dependencies: `cd src/frontend && npm install`
- Check port 5173 is available

**AI features not working:**
- Ensure Ollama is running: `ollama serve`
- Check model is available: `ollama list`
- Verify environment variables are set correctly

**Semantic search not available:**
- Install sentence-transformers: `pip install sentence-transformers`
- Search will work without it, but semantic search requires this package
