# IncidentIQ — Submission Tracker & Requirements Audit

Source of truth: Agents League About page + Microsoft's submission email. Deadline **June 14, 2026**.

## Mandatory submission requirements

| # | Requirement | Status | Notes |
|---|-------------|--------|-------|
| 1 | **Integrate ≥1 Microsoft IQ layer** (Foundry IQ / Work IQ / Fabric IQ) | 🟡 **Code built — awaiting Azure** | Foundry IQ grounding implemented: `knowledge/` runbooks + `search_runbooks` tool + cited evidence in the trace/post-mortem; `run_foundry` wired to the Foundry model + Foundry IQ. Goes fully live once the (free) Azure account + creds are added (FOUNDRY_PLAN.md). |
| 2 | Working project built with the track's tool (Reasoning Agents → Microsoft Foundry) | 🟡 Partial | Local mode fully working incl. grounding; Foundry mode ready, needs creds. |
| 3 | Project description (problem, features, tech, AI value) | ✅ Done | On Innovation Studio project + README. |
| 4 | Demo video ≤2 min, public YouTube/Vimeo, no 3rd-party trademarks | 🟡 Script ready | Full script + shotlist in `VIDEO_SCRIPT.md`; still to record + upload. |
| 5 | Public GitHub repo with README | ✅ Done | github.com/theAdityaNVS/incidentiq-agents-league (README present, no secrets). |
| 6 | Architecture diagram (Foundry / Agent Framework / Azure MCP / Copilot / Azure) | ✅ Done | `docs/architecture.svg` (image) with the Foundry IQ box; ASCII version also in `docs/architecture.md`. |
| 7 | All teammates registered + activated + added to project (≤5) | ✅ (solo) | Only add teammates if any join; each must self-register + be accepted. |
| 8 | Read Disclaimer + Code of Conduct; no confidential info | ⬜ User action | Quick read on the About page. |
| 9 | Project created **and submitted** on Innovation Studio | 🟡 Created | Submit step still to be done before deadline. |

## Judging rubric (how we score) — and our plan to maximize each

| Weight | Criterion | Our strength / action |
|-------:|-----------|----------------------|
| 20% | Accuracy & Relevance | Reasoning-agent track fit is strong. **Foundry IQ grounding** (cited runbook evidence) raises accuracy. |
| 20% | Reasoning & Multi-step Thinking | Core strength: hypothesis → tool call → eliminate → conclude, all visible in the console + post-mortem. |
| 15% | Creativity & Originality | Incident root-cause as visible agent reasoning; Foundry IQ grounding of each hypothesis is a differentiator. |
| 15% | UX & Presentation | Polished dark dashboard; tight 2-min video needed (item 4). |
| 20% | Reliability & Safety | Local fallback always runs; no auto-destructive actions (rollback/PR are human-approved); no secrets in repo. Call this out in the video + README. |
| 10% | Community vote | Share on the Agents League Discord (https://aka.ms/agentsleague/discord). |

## 2-minute demo video outline
1. **0:00–0:15 Problem** — "Checkout latency spiked 5x; on-call burns hours correlating logs/metrics/deploys."
2. **0:15–1:20 Live run** — open dashboard → Run Agent Diagnosis → reasoning console streams hypotheses → KEPT/ELIMINATED with evidence → root cause pinpointed → **show Foundry IQ cited sources** → post-mortem.
3. **1:20–1:40 Architecture** — Foundry agent + Foundry IQ retrieval + tools + output.
4. **1:40–2:00 Impact & safety** — hours→seconds MTTR; human-approved fixes; grounded/cited to reduce hallucination.

## Open items before submit (priority order)
1. ❗ Build the **Foundry IQ integration** (mandatory) — FOUNDRY_PLAN.md.
2. Architecture diagram image (add Foundry IQ box).
3. Record + upload the 2-min demo video; put the link in the project description.
4. Final review (Disclaimer/CoC) → **Submit** on Innovation Studio before June 14.
