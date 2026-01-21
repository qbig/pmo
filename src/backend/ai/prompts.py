"""Prompt templates for PMO AI capabilities."""

PROJECT_SUMMARY_PROMPT = """You are a PMO assistant. Generate a concise executive summary for a project based on the following information.

Project Information:
{project_content}

Related Risks:
{risks_content}

Related Decisions:
{decisions_content}

Generate a 1-page executive summary that includes:
1. Current status (on track / at risk / blocked)
2. Key milestones and progress
3. Top risks and blockers
4. Recent decisions and their impact
5. Next steps

Format as clear, professional markdown."""

DRIFT_DETECTION_PROMPT = """You are a PMO assistant analyzing project health. Review the following project information and identify any drift or issues.

Project Information:
{project_content}

Check for:
1. Goals vs milestones alignment
2. Stale risks (not updated recently)
3. Dependencies without owners
4. Decisions with unresolved consequences
5. Status inconsistencies

Return a JSON object with:
{{
  "issues": [
    {{
      "type": "stale_risk" | "orphaned_dependency" | "goal_misalignment" | "status_inconsistency",
      "severity": "low" | "medium" | "high",
      "description": "Brief description",
      "recommendation": "What should be done"
    }}
  ]
}}"""

MEETING_INGESTION_PROMPT = """You are a PMO assistant. Extract structured information from meeting notes and update project files accordingly.

Meeting Notes:
{meeting_notes}

Project Context:
{project_content}

Extract and structure:
1. New risks (with severity and probability)
2. Decisions made (with context and consequences)
3. Status updates (milestones, blockers, progress)
4. Action items

Return a JSON object:
{{
  "risks": [
    {{
      "id": "risk:name",
      "title": "Risk title",
      "severity": "low" | "medium" | "high" | "critical",
      "probability": "low" | "medium" | "high",
      "description": "Risk description",
      "impact": "Impact description"
    }}
  ],
  "decisions": [
    {{
      "id": "dec:name",
      "title": "Decision title",
      "context": "Why this decision",
      "decision": "What was decided",
      "consequences": ["consequence1", "consequence2"]
    }}
  ],
  "status_updates": {{
    "milestones": ["milestone updates"],
    "blockers": ["blocker descriptions"],
    "progress": "Progress narrative"
  }},
  "action_items": [
    "action item 1",
    "action item 2"
  ]
}}"""

FORECASTING_PROMPT = """You are a PMO assistant. Analyze project dependencies and risks to forecast potential delays.

Project Information:
{project_content}

Dependencies:
{dependencies_content}

Risks:
{risks_content}

Analyze the dependency graph and risk factors to identify:
1. Most likely blockers
2. Critical path items
3. Risk-weighted delay probability

Return a JSON object:
{{
  "blockers": [
    {{
      "id": "dependency or risk ID",
      "type": "dependency" | "risk",
      "description": "What is blocking",
      "delay_probability": 0.0-1.0,
      "estimated_delay_days": number,
      "impact": "high" | "medium" | "low"
    }}
  ],
  "critical_path": ["item1", "item2"],
  "forecast": {{
    "on_time_probability": 0.0-1.0,
    "at_risk_probability": 0.0-1.0,
    "delayed_probability": 0.0-1.0
  }}
}}"""

FILE_EDIT_PROMPT = """You are a PMO assistant. You need to update a markdown file based on the user's request.

Current File Content:
{file_content}

User Request:
{user_request}

Generate the updated file content. Maintain the same frontmatter structure and markdown format. Only change what is necessary based on the request.

Return ONLY the complete updated file content, including frontmatter."""
