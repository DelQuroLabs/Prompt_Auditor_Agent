# Specialist spawn triggers

Spawn a specialist only when at least one **signal** matches. Prefer path and explicit human flags over vibes.

## Signal table

| Signal | Specialist |
|---|---|
| Paths/names match `auth`, `session`, `jwt`, `oauth`, `password`, `secret`, `credential`, `permission`, `rbac`, `csrf`, `token`, `crypto` | Security |
| Spec/standards mark a **trust boundary**, PII, payments, multi-tenant isolation | Security |
| Builder `flags` mention secrets, auth, or security risk | Security |
| Paths match `*.tsx`, `*.jsx`, `*.vue`, `*.svelte`, `*.css`, `components/`, `pages/`, `views/`, `screens/` | UX |
| Spec acceptance criteria are user-visible flows (copy, empty states, forms) | UX |
| Spec tags or constraints mention latency, throughput, memory, realtime, batch, N+1 | Perf |
| Hot-path files listed in standards or kickoff | Perf |
| Paths or descriptions identify migrations, `alembic/versions/`, Prisma schemas, Flyway/Liquibase scripts, ORM model definitions with schema changes, backfills, or data transformations | Data |
| Builder `flags` mention migration / schema / breaking data change | Data |
| Paths match `Dockerfile`, `docker-compose`, `.github/`, `deploy/`, `helm/`, `terraform/`, `k8s/` | Release |
| Human requests ship checklist / pre-release review | Release |
| Kickoff lists **unknowns**, unfamiliar vendor API, or Builder sets a research flag / open question needing external fact | Researcher |

## Parallelism

- Run matching specialists **in parallel** on the **same** Builder packet (same `task_id` + `build_revision`).
- Do not chain specialists into each other.
- Cap: usually ≤2 specialists per revision unless ship review needs Release + Security.

## Still skip when…

| Situation | Action |
|---|---|
| Pure internal pure-function change, no trust/UI/data/ops surface | Core pair only |
| Specialist would restate Auditor correctness findings | Skip; let Auditor own it |
| Packet missing the files the specialist needs | Specialist returns scope limitation + open_questions; does not invent |

## Human checklist (30 seconds)

Before pasting into a specialist GPT:

1. Does a row in the signal table match? If no → stop.
2. Is the full Builder response available (not JSON-only)? If no → fix packet first.
3. Will the Auditor see this specialist report on the same revision? If no → do not bother.
