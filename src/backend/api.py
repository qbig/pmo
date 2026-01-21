"""FastAPI routes for PMO Assistant."""

from typing import List, Optional, Dict
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .indexer import Indexer
from .ai.engine import AIEngine
from .config import Config

router = APIRouter()

# Global instances (set in main.py)
indexer: Optional[Indexer] = None
ai_engine: Optional[AIEngine] = None
semantic_search = None  # Optional semantic search instance


def set_indexer(idx: Indexer):
    """Set the global indexer instance."""
    global indexer
    indexer = idx


def set_ai_engine(engine: AIEngine):
    """Set the global AI engine instance."""
    global ai_engine
    ai_engine = engine


def set_semantic_search(search_instance):
    """Set the global semantic search instance."""
    global semantic_search
    semantic_search = search_instance


class FileResponse(BaseModel):
    """File response model."""
    id: str
    path: str
    file_type: str
    title: str
    owner: Optional[str]
    status: Optional[str]
    content: Optional[str] = None
    frontmatter: Optional[dict] = None
    updated_at: Optional[str] = None


class FileListResponse(BaseModel):
    """File list response model."""
    files: List[FileResponse]


@router.get("/api/files", response_model=FileListResponse)
async def list_files(file_type: Optional[str] = None):
    """List all indexed files."""
    if not indexer:
        raise HTTPException(status_code=503, detail="Indexer not initialized")
    
    files = indexer.list_files(file_type=file_type)
    return FileListResponse(files=files)


@router.get("/api/files/{file_id}", response_model=FileResponse)
async def get_file(file_id: str):
    """Get a specific file by ID."""
    if not indexer:
        raise HTTPException(status_code=503, detail="Indexer not initialized")
    
    file_data = indexer.get_file(file_id)
    if not file_data:
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(**file_data)


@router.get("/api/projects")
async def list_projects():
    """List all projects."""
    if not indexer:
        raise HTTPException(status_code=503, detail="Indexer not initialized")
    
    files = indexer.list_files(file_type="project")
    return {"projects": files}


@router.get("/api/risks")
async def list_risks():
    """List all risks."""
    if not indexer:
        raise HTTPException(status_code=503, detail="Indexer not initialized")
    
    files = indexer.list_files(file_type="risk")
    return {"risks": files}


@router.get("/api/decisions")
async def list_decisions():
    """List all decisions."""
    if not indexer:
        raise HTTPException(status_code=503, detail="Indexer not initialized")
    
    files = indexer.list_files(file_type="decision")
    return {"decisions": files}


@router.get("/api/ai/summary/{project_id}")
async def get_project_summary(project_id: str):
    """Generate AI summary for a project."""
    if not ai_engine:
        raise HTTPException(status_code=503, detail="AI engine not initialized")
    
    try:
        summary = await ai_engine.generate_project_summary(project_id)
        return {"summary": summary}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/api/ai/drift/{project_id}")
async def detect_project_drift(project_id: str):
    """Detect drift and issues in a project."""
    if not ai_engine:
        raise HTTPException(status_code=503, detail="AI engine not initialized")
    
    try:
        issues = await ai_engine.detect_drift(project_id)
        return issues
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/api/ai/forecast/{project_id}")
async def forecast_project_blockers(project_id: str):
    """Forecast blockers and delays for a project."""
    if not ai_engine:
        raise HTTPException(status_code=503, detail="AI engine not initialized")
    
    try:
        forecast = await ai_engine.forecast_blockers(project_id)
        return forecast
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


class MeetingIngestRequest(BaseModel):
    """Request model for meeting ingestion."""
    notes: str
    project_id: Optional[str] = None


@router.post("/api/ai/ingest-meeting")
async def ingest_meeting_notes(request: MeetingIngestRequest):
    """Extract structured information from meeting notes."""
    if not ai_engine:
        raise HTTPException(status_code=503, detail="AI engine not initialized")
    
    result = await ai_engine.ingest_meeting_notes(
        request.notes,
        request.project_id
    )
    return result


class FileEditRequest(BaseModel):
    """Request model for file editing."""
    request: str


@router.post("/api/ai/edit/{file_id}")
async def edit_file(file_id: str, edit_request: FileEditRequest):
    """Generate updated file content based on user request."""
    if not ai_engine:
        raise HTTPException(status_code=503, detail="AI engine not initialized")
    
    try:
        updated_content = await ai_engine.edit_file(file_id, edit_request.request)
        return {"content": updated_content}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/api/diff/generate")
async def generate_diff(request: Dict[str, str]):
    """Generate diff between original and updated content."""
    from .diff import DiffGenerator, DiffSummary
    
    original = request.get("original", "")
    updated = request.get("updated", "")
    filename = request.get("filename", "file.md")
    
    if not original or not updated:
        raise HTTPException(status_code=400, detail="original and updated content required")
    
    unified_diff = DiffGenerator.generate_unified_diff(original, updated, filename)
    hunks = DiffGenerator.generate_hunk_list(original, updated)
    side_by_side = DiffGenerator.generate_side_by_side_diff(original, updated)
    summary = DiffSummary(original, updated)
    
    return {
        "unified_diff": unified_diff,
        "hunks": hunks,
        "side_by_side": side_by_side,
        "summary": summary.to_dict()
    }


@router.post("/api/diff/apply/{file_id}")
async def apply_diff(file_id: str, request: Dict[str, str]):
    """Apply diff to a file."""
    from .diff import PatchApplier
    from pathlib import Path
    
    if not indexer:
        raise HTTPException(status_code=503, detail="Indexer not initialized")
    
    file_data = indexer.get_file(file_id)
    if not file_data:
        raise HTTPException(status_code=404, detail="File not found")
    
    updated_content = request.get("content")
    if not updated_content:
        raise HTTPException(status_code=400, detail="content required")
    
    file_path = Path(file_data["path"])
    backup = request.get("backup", True)
    
    success = PatchApplier.apply_patch(file_path, updated_content, backup=backup)
    
    if success:
        # Re-index the file
        await indexer.index_file(file_path)
        return {"status": "success", "path": str(file_path)}
    else:
        raise HTTPException(status_code=500, detail="Failed to apply patch")


@router.post("/api/diff/preview/{file_id}")
async def preview_diff(file_id: str, request: Dict[str, str]):
    """Preview diff without applying."""
    from .diff import DiffGenerator, DiffSummary
    
    if not indexer:
        raise HTTPException(status_code=503, detail="Indexer not initialized")
    
    file_data = indexer.get_file(file_id)
    if not file_data:
        raise HTTPException(status_code=404, detail="File not found")
    
    updated_content = request.get("content")
    if not updated_content:
        raise HTTPException(status_code=400, detail="content required")
    
    original = file_data["content"]
    filename = Path(file_data["path"]).name
    
    unified_diff = DiffGenerator.generate_unified_diff(original, updated_content, filename)
    hunks = DiffGenerator.generate_hunk_list(original, updated_content)
    side_by_side = DiffGenerator.generate_side_by_side_diff(original, updated_content)
    summary = DiffSummary(original, updated_content)
    
    return {
        "unified_diff": unified_diff,
        "hunks": hunks,
        "side_by_side": side_by_side,
        "summary": summary.to_dict()
    }


class SearchRequest(BaseModel):
    """Request model for semantic search."""
    query: str
    top_k: int = 5


@router.post("/api/search")
async def semantic_search_endpoint(request: SearchRequest):
    """Semantic search over indexed files."""
    if not indexer:
        raise HTTPException(status_code=503, detail="Indexer not initialized")
    
    if not semantic_search:
        raise HTTPException(status_code=503, detail="Semantic search not available. Install sentence-transformers.")
    
    # Get all file embeddings
    all_files = indexer.list_files()
    file_embeddings = {}
    
    for file_info in all_files:
        file_data = indexer.get_file(file_info["id"])
        if file_data and file_info["id"] in semantic_search.embeddings_cache:
            file_embeddings[file_info["id"]] = semantic_search.embeddings_cache[file_info["id"]]
    
    # Search
    results = semantic_search.search(request.query, file_embeddings, top_k=request.top_k)
    
    # Format results
    formatted_results = []
    for file_id, similarity in results:
        file_data = indexer.get_file(file_id)
        if file_data:
            formatted_results.append({
                "file_id": file_id,
                "title": file_data["title"],
                "file_type": file_data["file_type"],
                "similarity": float(similarity),
                "path": file_data["path"]
            })
    
    return {
        "query": request.query,
        "results": formatted_results
    }
