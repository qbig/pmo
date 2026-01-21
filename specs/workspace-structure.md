# Workspace Structure

The PMO workspace is a directory structure containing markdown files organized by type.

## Directory Layout

```
workspace/
├── projects/      # Project files (proj-*.md)
├── epics/         # Epic files (epic-*.md)
├── decisions/     # Decision log files (dec-*.md)
├── risks/         # Risk register files (risk-*.md)
├── meetings/      # Meeting notes (meeting-*.md)
├── people/        # People/team files (person-*.md)
└── logs/          # Activity logs (log-*.md)
```

## File Naming Conventions

- **Projects**: `proj-<name>.md` (e.g., `proj-alpha.md`)
- **Epics**: `epic-<name>.md` (e.g., `epic-q2-launch.md`)
- **Decisions**: `dec-<name>.md` (e.g., `dec-use-postgres.md`)
- **Risks**: `risk-<name>.md` (e.g., `risk-vendor-delay.md`)
- **Meetings**: `meeting-<date>-<topic>.md` (e.g., `meeting-2026-01-21-standup.md`)
- **People**: `person-<username>.md` (e.g., `person-alice.md`)
- **Logs**: `log-<date>.md` (e.g., `log-2026-01-21.md`)

## Cross-References

Files reference each other using ID prefixes:
- `proj:<id>` - References a project
- `epic:<id>` - References an epic
- `dec:<id>` - References a decision
- `risk:<id>` - References a risk
- `dep:<id>` - References a dependency (can be project, epic, or external)
- `person:<id>` - References a person

## Workspace Root

The workspace root is configurable but defaults to `./workspace` relative to the application root.
