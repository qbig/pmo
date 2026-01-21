# Markdown File Schemas

This document defines the standardized frontmatter and content structure for each file type in the PMO workspace.

## Project Files (`/projects/*.md`)

### Frontmatter Schema
```yaml
---
id: proj-<name>
owner: <username>
status: active | completed | cancelled | on-hold
start: YYYY-MM-DD
target: YYYY-MM-DD
---
```

### Content Structure
```markdown
# Project Name

## Goal
[Clear, measurable project goal]

## Current Status
[Status emoji: 🟢 On track | 🟡 At risk | 🔴 Blocked]
[Brief narrative status]

## Milestones
- [x] Milestone 1
- [ ] Milestone 2
- [ ] Milestone 3

## Dependencies
- dep:<dependency-id>
- dep:<another-dependency-id>

## Risks
- risk:<risk-id>
- risk:<another-risk-id>

## Last Updated
YYYY-MM-DD
```

## Risk Files (`/risks/*.md`)

### Frontmatter Schema
```yaml
---
id: risk:<name>
severity: low | medium | high | critical
probability: low | medium | high
owner: <username>
status: open | mitigated | closed
---
```

### Content Structure
```markdown
# Risk Title

## Description
[Detailed description of the risk]

## Impact
[What happens if this risk materializes]

## Mitigation
- [Mitigation strategy 1]
- [Mitigation strategy 2]

## Status
[Current status narrative]
```

## Decision Files (`/decisions/*.md`)

### Frontmatter Schema
```yaml
---
id: dec:<name>
date: YYYY-MM-DD
owner: <username>
status: proposed | accepted | rejected | superseded
---
```

### Content Structure
```markdown
# Decision Title

## Context
[Why this decision is needed]

## Decision
[The decision that was made]

## Consequences
- [Consequence 1]
- [Consequence 2]
- [Consequence 3]
```

## Epic Files (`/epics/*.md`)

### Frontmatter Schema
```yaml
---
id: epic:<name>
owner: <username>
status: planning | active | completed
start: YYYY-MM-DD
target: YYYY-MM-DD
---
```

### Content Structure
```markdown
# Epic Name

## Description
[Epic description]

## Projects
- proj:<project-id>
- proj:<another-project-id>

## Goals
[Epic-level goals]
```

## Meeting Files (`/meetings/*.md`)

### Frontmatter Schema
```yaml
---
id: meeting:<date>-<topic>
date: YYYY-MM-DD
attendees: [username1, username2]
type: standup | planning | retrospective | ad-hoc
---
```

### Content Structure
```markdown
# Meeting Title

## Agenda
- [Agenda item 1]
- [Agenda item 2]

## Notes
[Meeting notes]

## Action Items
- [ ] Action item 1
- [ ] Action item 2

## Decisions
- dec:<decision-id>

## Risks Identified
- risk:<risk-id>
```

## People Files (`/people/*.md`)

### Frontmatter Schema
```yaml
---
id: person:<username>
name: Full Name
role: <role>
team: <team>
---
```

### Content Structure
```markdown
# Person Name

## Role
[Role description]

## Projects
- proj:<project-id>
- proj:<another-project-id>

## Responsibilities
[Key responsibilities]
```

## Log Files (`/logs/*.md`)

### Frontmatter Schema
```yaml
---
id: log:<date>
date: YYYY-MM-DD
type: daily | weekly | monthly
---
```

### Content Structure
```markdown
# Log Title

## Summary
[Brief summary]

## Updates
[Detailed updates]

## Next Steps
- [Next step 1]
- [Next step 2]
```
