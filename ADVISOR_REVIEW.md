# ADVISOR_REVIEW.md — IncidentIQ Hackathon Submission Review

**Project:** IncidentIQ · Agents League @ AISF 2026 · Track: Reasoning Agents  
**Review date:** 2026-06-13 (deadline: 2026-06-14)  
**Method:** 5 parallel subagent lenses — Compliance, Backend correctness, Foundry IQ integration, Security, Frontend/UX  

---

## FINAL VERDICT: NOT READY — SUBMIT AFTER FIXING P0s

Two items will cause disqualification or near-zero scores if submitted now:
no demo video and no real Azure/Foundry IQ connection. Both are fixable before
the deadline. Everything else is either solid or a polish improvement.

---

## Gap List

### P0 — Blockers (disqualify or severely damage the score)

**P0-A: No demo video recorded or uploaded**  
Requirement #4 (demo video ≤2 min, public) is unmet. Most hackathon platforms
require the video link before they allow the Submit button to work. Without it:
UX/Presentation (15%) scores near zero, and judges cannot see the multi-step
reasoning that is the project's core strength (20%). VIDEO_SCRIPT.md is ready;
recording is the blocker.  
_Fix: Record the demo today using local mode (always stable). Upload to
YouTube/Vimeo. Add the link to the Innovation Studio project description._

**P0-B: Foundry IQ not connected to any Azure resource**  
The hackathon rules explicitly state entries without an IQ layer do not qualify.
`run_foundry` uses `AIProjectClient` (correct SDK) but the `search_runbooks`
tool always executes as a local Python keyword scan over `knowledge/*.md` in
ALL code paths — there is no branch routing to Azure AI Search. The README,
docstrings, and system prompt all describe it as "Foundry IQ agentic retrieval,"
but no Azure service is called. FOUNDRY_PLAN.md estimates 30–45 min to wire
this up on the Azure free tier.  
_Fix (minimum viable): Create an Azure AI Search free-tier resource, upload the
3 knowledge/ markdown files, add `AZURE_SEARCH_ENDPOINT` env var, and add a
conditional in `tools.search_runbooks` (or a separate `search_runbooks_foundry`)
that calls the Search REST API when Azure creds are present. Then `run_foundry`
automatically uses real agentic retrieval._

**P0-C: Innovation Studio submit not clicked**  
Requirement #9: project is created but not submitted. Must be done before June 14.

---

### P1 — High impact (score damage, not DQ)

**P1-A: `citations` array never rendered on the dashboard**  
The `/api/diagnose` response includes a `citations` array, but `renderDiagnosisResults()`
in `index.html` never reads it. There is no "Foundry IQ Grounded Sources" panel.
The video script at 1:15–1:30 calls for showing citations on screen — they are
only visible as inline text in the evidence list, easy for judges to miss.  
_Fix (no code change): Redirect the video script's citation beat to the
post-mortem modal, where `## Grounded sources (Foundry IQ)` IS rendered clearly.  
Fix (with code): Add a citations section below the hypotheses panel._

**P1-B: 3 critical bugs in agent.py / tools.py that can silently break Foundry mode**

1. **Greedy regex in `_parse_foundry_json`** (`r"\{.*\}"` with DOTALL) will match
   the wrong span if the model output contains any `{...}` before the final JSON
   object (e.g. prose, earlier tool result echoes). Causes `JSONDecodeError` →
   silent fallback to local mode without any judge-visible error.  
   _Fix: Use `r"\{[\s\S]*\}"` non-greedy or strip markdown fences first, then
   `json.loads` directly._

2. **Loop-exhaustion path discards accumulated trace**: When the tool-calling
   loop runs all 8 iterations, `_parse_foundry_json("")` falls back to a fresh
   `run_local()` that discards all Foundry tool-call records from `trace`.  
   _Fix: Return `run_local(incident, verbose=False)` only as a last resort; try
   to reconstruct from the last assistant message first._

3. **`dispatch` does not catch `TypeError`** from unexpected kwargs passed by the
   model. If Foundry model returns an extra argument, `fn(**arguments)` raises
   unhandled `TypeError` → leaves the messages list in an inconsistent state
   (assistant tool_calls turn with no matching tool reply).  
   _Fix: Wrap `fn(**arguments)` in `try/except TypeError` inside `dispatch` and
   return `json.dumps({"error": str(e)})` instead._

**P1-C: Hard dict lookup on `h.verdict` raises KeyError in postmortem.py and `_print_conclusion`**

```python
mark = {"kept": "KEPT", "eliminated": "ELIMINATED", "open": "OPEN"}[h.verdict]
```

If the Foundry model returns `"Kept"`, `"confirmed"`, or `""`, this is an
unhandled `KeyError` → 500 on `/api/postmortem`.  
_Fix: Use `.get(h.verdict, h.verdict.upper())` with a default._

---

### P2 — Polish / robustness (nice to fix, not blocking)

**P2-A: `h_dependency` left "open" when metrics are absent**  
If `pg_lat` is empty dict, the `if pg_lat:` guard is falsy → the dependency
hypothesis is never eliminated, rendering as `[OPEN]` in the post-mortem with
no reasoning. This only affects edge-case incident data, not the current demo.

**P2-B: KB citations appended to `h_deploy` unconditionally**  
The `search_runbooks` call runs after the `if near_deploy:` block. If
`near_deploy` is empty, KB snippets are still appended to the "open" deploy
hypothesis, creating a contradictory post-mortem.  
_Fix: Move the KB search inside `if near_deploy:` or tie it to the kept hypothesis._

**P2-C: `msg.model_dump()` SDK compatibility risk**  
On some azure-ai-projects versions that pin older openai (pydantic v1), `.model_dump()`
doesn't exist → `AttributeError` → silent fallback to local mode. Building the
dict manually avoids the risk:
```python
{"role": "assistant", "content": msg.content,
 "tool_calls": [tc.model_dump() for tc in (msg.tool_calls or [])]}
```

**P2-D: No dedicated "Foundry IQ Sources" panel on dashboard (frontend)**  
Even with the video-script workaround from P1-A, adding a small citations panel
to the main dashboard (styled like the evidence cards) would make the grounding
story compelling during any live demo. Takes ~20 lines of JS + CSS.

**P2-E: `.glow-green` / `.glow-red` CSS classes referenced in JS but not defined**  
The intended extra glow on KEPT/ELIMINATED hypothesis cards doesn't fire.
Low visual impact; quick CSS fix.

**P2-F: Disclaimer + Code of Conduct not yet read (Req #8)**  
Two-minute user action on the Innovation Studio About page.

**P2-G: Discord promotion for community vote (10% of rubric)**  
Share in the Agents League Discord (https://aka.ms/agentsleague/discord).

---

## What Is Already Strong (don't break these)

| Area | Status |
|---|---|
| Reasoning loop correctness (local mode) | Solid. Hypothesis → tool → eliminate → conclude is real and traceable. |
| Knowledge base content | Well-matched to the scenario; RB-12 / PM-INC-3990 cite correctly. |
| FastAPI backend | Clean, correct dataclasses.asdict serialization, correct static-file serving. |
| Post-mortem markdown | Renders citations in a dedicated section; best place to show grounding. |
| No secrets in repo | .env gitignored, DefaultAzureCredential pattern correct, no hardcoded keys. |
| Human-in-the-loop | Structurally enforced — no write tools registered; rollback/PR are strings only. |
| Dashboard loading animation | Streaming simulation + staggered reveal is polished and demo-ready. |
| Architecture diagram | docs/architecture.svg exists with Foundry IQ box. |
| README + Innovation Studio description | Complete and compelling. |
| Fallback chain | Every failure path degrades gracefully to local mode. |

---

## Rubric Score Estimates

| Criterion | Weight | Current (no video, no Azure) | After P0 fixes |
|---|---|---|---|
| Accuracy & Relevance | 20% | 12–14 | 17–18 |
| Reasoning & Multi-step | 20% | 14–16 | 17–19 |
| Creativity & Originality | 15% | 10–12 | 12–14 |
| UX & Presentation | 15% | 3–5 | 12–13 |
| Reliability & Safety | 20% | 13–15 | 16–18 |
| Community vote | 10% | Unknown | Unknown |
| **Estimated total** | | **~52–62%** | **~74–82%** |

---

## Ordered Action Plan (Before June 14)

1. **Record and upload the demo video** (~1–2 hrs). Use local mode — always
   stable, visually identical. Follow VIDEO_SCRIPT.md. For the citation beat
   at 1:20, show the post-mortem modal (`## Grounded sources (Foundry IQ)`
   section is already there). Upload to YouTube unlisted.

2. **Wire search_runbooks to Azure AI Search** (~2–4 hrs). See FOUNDRY_PLAN.md
   step-by-step. Minimum: free-tier Azure AI Search + 3-doc index + env-var
   routing in `search_runbooks`. Then `run_foundry` becomes a real Foundry IQ
   call. Test with `python -m incidentiq.main --foundry`.

3. **Fix the 3 critical code bugs** (P1-B above) (~30 min):
   - Fix `_parse_foundry_json` regex
   - Add `try/except TypeError` in `dispatch`
   - Change verdict dict lookups to `.get()` with fallback

4. **Read Disclaimer + CoC on Innovation Studio** (2 min).

5. **Click Submit on Innovation Studio** (5 min).

6. **Post in Agents League Discord** with the GitHub link and a one-liner about
   the grounded reasoning approach (community vote = 10%).

7. **Optional P2 polish** if time allows: add citations panel to dashboard,
   define `.glow-green`/`.glow-red` CSS, build manual `msg.model_dump()`.
