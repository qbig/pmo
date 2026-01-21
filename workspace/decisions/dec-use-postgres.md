---
id: dec:use-postgres
date: 2026-01-18
owner: eng-lead
status: accepted
---

# Use Postgres for Core Storage

## Context
Need transactional guarantees.

## Decision
Adopt Postgres over DynamoDB.

## Consequences
- Strong consistency
- Higher ops overhead
