# IncidentIQ — Submission Tracker & Requirements Audit

Source of truth: Agents League About page + Microsoft's submission email. Deadline **June 14, 2026**.

## Mandatory submission requirements

| # | Requirement | Status | Notes |
|---|-------------|--------|-------|
| 1 | **Integrate ≥1 Microsoft IQ layer** (Foundry IQ / Work IQ / Fabric IQ) | ✅ **Live** | Azure AI Search `incidentiq-srch` (East US, free tier) indexed with 3 runbooks. `search_runbooks` routes to `_search_azure` when env vars present — confirmed 3 citations returned from live Vercel deployment on 2026-06-15. |
| 2 | Working project built with the track's tool (Reasoning Agents → Microsoft Foundry) | ✅ Done | Local + Foundry IQ modes working. Live at `agents-league-microsoft.vercel.app`. |
| 3 | Project description (problem, features, tech, AI value) | ✅ Done | On Innovation Studio project + README. |
| 4 | Demo video ≤2 min, public YouTube/Vimeo, no 3rd-party trademarks | ⬜ **Record + upload** | Script + shotlist in `VIDEO_SCRIPT.md`. Add link to Innovation Studio project description. |
| 5 | Public GitHub repo with README | ✅ Done | github.com/theAdityaNVS/incidentiq-agents-league — README updated, no secrets in history. |
| 6 | Architecture diagram (Foundry / Agent Framework / Azure MCP / Copilot / Azure) | ✅ Done | `docs/architecture.svg` with Foundry IQ box; ASCII in `docs/architecture.md`. |
| 7 | All teammates registered + activated + added to project (≤5) | ✅ (solo) | Only add teammates if any join. |
| 8 | Read Disclaimer + Code of Conduct; no confidential info | ⬜ User action | Quick read on the About page. |
| 9 | Project created **and submitted** on Innovation Studio | ⬜ **Submit** | Add video link to description, then click Submit. |

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
1. ⬜ Record + upload the 2-min demo video (follow `VIDEO_SCRIPT.md`); add link to Innovation Studio project description.
2. ⬜ Read Disclaimer + Code of Conduct on Innovation Studio About page (2 min).
3. ⬜ Click **Submit** on Innovation Studio.
4. ⬜ Post in Agents League Discord (`https://aka.ms/agentsleague/discord`) — 10% community vote.

## Completed (2026-06-15)
- ✅ Azure AI Search `incidentiq-srch` created (East US, free tier, resource group `incidentiq-rg`)
- ✅ Index `incidentiq-kb` with fields `content`, `source`, `citation` — 3 docs uploaded (RB-12, RB-07, PM-INC-3990)
- ✅ `.env` written locally (gitignored); Vercel env vars set (`AZURE_SEARCH_ENDPOINT`, `AZURE_SEARCH_INDEX`, `AZURE_SEARCH_KEY`)
- ✅ Redeployed to Vercel production — live smoke test confirmed 3 Azure citations from `/api/diagnose`
- ✅ All P1 bugs verified fixed (regex, dispatch TypeError, verdict KeyError, citations panel, glow CSS)
- ✅ No secrets in git history (verified with `git log -S`)
