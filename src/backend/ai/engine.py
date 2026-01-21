"""AI execution engine for PMO capabilities."""

import logging
from typing import Dict, Any, List, Optional
from pathlib import Path

from .llm import LLMClient
from .prompts import (
    PROJECT_SUMMARY_PROMPT,
    DRIFT_DETECTION_PROMPT,
    MEETING_INGESTION_PROMPT,
    FORECASTING_PROMPT,
    FILE_EDIT_PROMPT
)
from ..indexer import Indexer
from ..config import Config

logger = logging.getLogger(__name__)


class AIEngine:
    """AI execution engine for PMO operations."""
    
    def __init__(self, config: Config, indexer: Indexer):
        self.config = config
        self.indexer = indexer
        self.llm = LLMClient(config)
    
    async def generate_project_summary(self, project_id: str) -> str:
        """
        Generate executive summary for a project.
        
        Args:
            project_id: Project file ID
            
        Returns:
            Markdown summary
        """
        # Get project
        project = self.indexer.get_file(project_id)
        if not project or project["file_type"] != "project":
            raise ValueError(f"Project not found: {project_id}")
        
        project_content = project["content"]
        
        # Get related risks
        risks = []
        if project.get("frontmatter", {}).get("risks"):
            risk_ids = project["frontmatter"]["risks"]
            for risk_id in risk_ids:
                risk = self.indexer.get_file(risk_id)
                if risk:
                    risks.append(risk["content"])
        
        risks_content = "\n\n".join(risks) if risks else "No risks identified."
        
        # Get related decisions
        decisions = []
        # Extract decision references from project content
        # (This is simplified - in production, parse markdown links)
        decisions_content = "No decisions referenced."
        
        # Generate summary
        prompt = PROJECT_SUMMARY_PROMPT.format(
            project_content=project_content,
            risks_content=risks_content,
            decisions_content=decisions_content
        )
        
        summary = await self.llm.generate(
            prompt,
            system_prompt="You are an expert PMO assistant. Generate clear, actionable executive summaries.",
            temperature=0.3
        )
        
        return summary
    
    async def detect_drift(self, project_id: str) -> Dict[str, Any]:
        """
        Detect drift and issues in a project.
        
        Args:
            project_id: Project file ID
            
        Returns:
            Dictionary with detected issues
        """
        project = self.indexer.get_file(project_id)
        if not project:
            raise ValueError(f"Project not found: {project_id}")
        
        prompt = DRIFT_DETECTION_PROMPT.format(
            project_content=project["content"]
        )
        
        response = await self.llm.generate(
            prompt,
            system_prompt="You are a PMO assistant. Analyze projects for health issues and drift.",
            temperature=0.2
        )
        
        # Parse JSON response
        import json
        try:
            # Extract JSON from response (might have markdown code blocks)
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                response = response[json_start:json_end].strip()
            elif "```" in response:
                json_start = response.find("```") + 3
                json_end = response.find("```", json_start)
                response = response[json_start:json_end].strip()
            
            return json.loads(response)
        except json.JSONDecodeError:
            logger.error(f"Failed to parse drift detection response: {response}")
            return {"issues": []}
    
    async def ingest_meeting_notes(
        self,
        meeting_notes: str,
        project_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Extract structured information from meeting notes.
        
        Args:
            meeting_notes: Raw meeting notes text
            project_id: Optional project ID for context
            
        Returns:
            Structured data (risks, decisions, status updates, action items)
        """
        project_content = ""
        if project_id:
            project = self.indexer.get_file(project_id)
            if project:
                project_content = project["content"]
        
        prompt = MEETING_INGESTION_PROMPT.format(
            meeting_notes=meeting_notes,
            project_content=project_content or "No project context provided."
        )
        
        response = await self.llm.generate(
            prompt,
            system_prompt="You are a PMO assistant. Extract structured information from meeting notes.",
            temperature=0.3
        )
        
        # Parse JSON response
        import json
        try:
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                response = response[json_start:json_end].strip()
            elif "```" in response:
                json_start = response.find("```") + 3
                json_end = response.find("```", json_start)
                response = response[json_start:json_end].strip()
            
            return json.loads(response)
        except json.JSONDecodeError:
            logger.error(f"Failed to parse meeting ingestion response: {response}")
            return {
                "risks": [],
                "decisions": [],
                "status_updates": {},
                "action_items": []
            }
    
    async def forecast_blockers(self, project_id: str) -> Dict[str, Any]:
        """
        Forecast potential blockers and delays.
        
        Args:
            project_id: Project file ID
            
        Returns:
            Forecast data with blockers and probabilities
        """
        project = self.indexer.get_file(project_id)
        if not project:
            raise ValueError(f"Project not found: {project_id}")
        
        # Get dependencies
        dependencies_content = ""
        if project.get("frontmatter", {}).get("dependencies"):
            deps = project["frontmatter"]["dependencies"]
            dependencies_content = "\n".join(f"- {dep}" for dep in deps)
        
        # Get risks
        risks_content = ""
        if project.get("frontmatter", {}).get("risks"):
            risk_ids = project["frontmatter"]["risks"]
            for risk_id in risk_ids:
                risk = self.indexer.get_file(risk_id)
                if risk:
                    risks_content += f"\n{risk['content']}\n"
        
        prompt = FORECASTING_PROMPT.format(
            project_content=project["content"],
            dependencies_content=dependencies_content or "No dependencies listed.",
            risks_content=risks_content or "No risks identified."
        )
        
        response = await self.llm.generate(
            prompt,
            system_prompt="You are a PMO assistant. Analyze dependencies and risks to forecast project delays.",
            temperature=0.2
        )
        
        # Parse JSON response
        import json
        try:
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                response = response[json_start:json_end].strip()
            elif "```" in response:
                json_start = response.find("```") + 3
                json_end = response.find("```", json_start)
                response = response[json_start:json_end].strip()
            
            return json.loads(response)
        except json.JSONDecodeError:
            logger.error(f"Failed to parse forecasting response: {response}")
            return {
                "blockers": [],
                "critical_path": [],
                "forecast": {
                    "on_time_probability": 0.5,
                    "at_risk_probability": 0.3,
                    "delayed_probability": 0.2
                }
            }
    
    async def edit_file(
        self,
        file_id: str,
        user_request: str
    ) -> str:
        """
        Generate updated file content based on user request.
        
        Args:
            file_id: File ID to edit
            user_request: User's edit request
            
        Returns:
            Updated file content
        """
        file_data = self.indexer.get_file(file_id)
        if not file_data:
            raise ValueError(f"File not found: {file_id}")
        
        prompt = FILE_EDIT_PROMPT.format(
            file_content=file_data["content"],
            user_request=user_request
        )
        
        updated_content = await self.llm.generate(
            prompt,
            system_prompt="You are a PMO assistant. Update markdown files accurately while preserving structure.",
            temperature=0.3
        )
        
        # Clean up response (remove markdown code blocks if present)
        if "```" in updated_content:
            # Extract content from code block
            lines = updated_content.split("\n")
            start_idx = None
            end_idx = None
            for i, line in enumerate(lines):
                if line.strip().startswith("```"):
                    if start_idx is None:
                        start_idx = i + 1
                    else:
                        end_idx = i
                        break
            if start_idx and end_idx:
                updated_content = "\n".join(lines[start_idx:end_idx])
        
        return updated_content
