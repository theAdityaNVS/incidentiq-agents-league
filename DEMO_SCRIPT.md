# IncidentIQ — Demo Recording Script (Narrated MP4, ≤ 2:00)

**Deliverable:** public YouTube/Vimeo video for the Agents League submission.
**Recorded against:** the live deployment — `https://agents-league-microsoft.vercel.app/`
**Verified:** flow, labels, and timings below were confirmed against a live run on 2026-06-15.

This script is exact to the current UI. Read the **Narration** column aloud while performing
the **On screen** actions. Total target: **1:55–2:00**. Narration is ~250 words ≈ 2 min at a
calm pace with the built-in pauses.

---

## Pre-flight (do this before you hit record)

1. **Browser:** Chrome at `https://agents-league-microsoft.vercel.app/`, zoom **110%**, hide the
   bookmarks bar (Ctrl+Shift+B). Full-screen the window (F11). Close other tabs.
2. **Warm it up:** run one full diagnosis once, then **reload** the page so the next run is fast
   and the animation is smooth. Leave it on the standby screen.
3. **OBS:** Display Capture (or a cropped Window Capture of Chrome), canvas **1920×1080 / 30 fps**.
   Mic source added, levels checked, ~−12 dB. Do a 5-second test take first.
4. **Mouse:** move deliberately; pause ~1s on anything you want the viewer to read (citations,
   root cause). Don't click the browser's address bar on camera.
5. **No third-party trademarks** in frame (the app's own UI and "Foundry IQ" wording are fine).

---

## Shotlist & narration

| Time | On screen (do this) | Narration (say this) |
|------|---------------------|----------------------|
| **0:00–0:12** | Standby dashboard. Cursor rests near the **INC-4471** incident card. | "When checkout latency spikes five-x, on-call engineers burn hours under pressure, manually correlating logs, metrics, and recent deploys. IncidentIQ does that reasoning in seconds." |
| **0:12–0:22** | Slowly hover across the incident card — the title **"Checkout latency spiked ~5x"**, the **checkout-api** chip, and **"Incident Started 14:05 UTC."** | "Here's the alert: checkout-api p95 latency jumped from two-forty milliseconds to one-point-three seconds, starting 14:05 UTC." |
| **0:22–0:30** | Click **Run Agent Diagnosis**. The status badge flips to **Agent Diagnosing**. | "I hand it to the agent and watch it think." |
| **0:30–0:52** | The **reasoning console** streams: it forms **H1 / H2 / H3**, dispatches tools, then logs `get_recent_deploys`, `get_metrics`, `get_logs`. Let it stream — don't scroll yet. | "It forms three hypotheses — a bad deploy, an upstream dependency, or resource exhaustion — then pulls evidence with tools: deploy history, metrics, and logs, exactly like an SRE would." |
| **0:52–1:08** | Console resolves: **H1 KEPT**, **H2 ELIMINATED**, **H3 ELIMINATED**. Slowly scroll to the **Hypothesis Evaluation** cards (one green *kept*, two red *eliminated*). | "It eliminates the upstream-dependency and CPU theories with evidence — the gateway is flat, CPU's under forty percent — and keeps the deploy regression." |
| **1:08–1:25** | Scroll to **Identified Root Cause** → pause on the **"Grounded in Foundry IQ"** block and the citation chips **RB-12 · PM-INC-3990 · RB-07**. | "The root cause is pinpointed — a new Redis-backed token cache with an undersized connection pool, queuing requests about four-eighty milliseconds. And it's grounded in our runbooks through Foundry IQ, with citations — so it's evidence, not a hallucination." |
| **1:25–1:40** | Scroll to **Resolution & Action Items**: hover **Execute Rollback** and **Draft PR Fix**, then click **View Full Post-Mortem Report**; the post-mortem modal opens. | "It drafts the immediate mitigation, the durable fix, and a full post-mortem report — ready to share." |
| **1:40–1:48** | Close the modal. (Optional) cut to `docs/architecture.svg` for ~2s. | "Under the hood: a Foundry reasoning agent, a Foundry IQ knowledge base, telemetry tools, and cited output." |
| **1:48–2:00** | Back on the results. Rest cursor on the **Execute Rollback** / **Draft PR Fix** buttons. | "Hours to seconds — grounded, cited, and safe: fixes are suggested for a human to approve, never auto-executed. That's IncidentIQ." |

---

## Rubric coverage (say or show at least one cue for each)

- **Reasoning & multi-step (20%)** — the streaming hypothesis → tool-call → eliminate → conclude (0:30–1:08).
- **Accuracy & relevance (20%)** — the cited **Foundry IQ** grounding block (1:08–1:25).
- **Reliability & safety (20%)** — "suggested for a human to approve, never auto-executed" (1:48–2:00).
- **UX & presentation (15%)** — the polished dark dashboard throughout.
- **Creativity & originality (15%)** — incident root-cause as *visible, cited* agent reasoning.

---

## Exact on-screen text to expect (for syncing narration)

- **Status badge:** `Agent Standby` → `Agent Diagnosing` → reverts to `Agent Standby` when done.
- **Console sequence:** `[SYSTEM] Initializing…` → `[AGENT] Target Incident: INC-4471` →
  `[ENGINE] Formulating diagnostics hypotheses…` → `[HYPOTHESIS] H1/H2/H3` →
  `[TOOL_DISPATCH]` → `[TOOL_CALL] get_recent_deploys → retrieved 3 events ✓` (+ `get_metrics`, `get_logs`) →
  `[ENGINE] Running causal evidence analyzer…` → `[ANALYSIS] H1: KEPT / H2: ELIMINATED / H3: ELIMINATED` →
  `[SYSTEM] Root cause identified. Resolution plans synthesized.`
- **Evidence Collection Timeline cards:** `get_recent_deploys`, `get_metrics`, `get_logs`, `search_runbooks`.
- **Citations:** `RB-12` (checkout-redis-cache), `PM-INC-3990` (redis-pool), `RB-07` (latency-triage).
- **Root cause line:** "checkout-api v2.41.0 switched the payment-token cache from an in-process LRU
  to a Redis lookup. The Redis connection pool (max=10) is undersized… p95 from 240ms to ~1310ms."
- **Action buttons:** `Execute Rollback`, `Draft PR Fix`, `View Full Post-Mortem Report`, `Copy Markdown`.

## Recording tips

- Keep one clean take of the diagnosis stream — the console only needs to play through once.
- If a take runs long, the easiest cut is the architecture beat (1:40–1:48); the rest is core.
- Pause ~1 second on the **Grounded in Foundry IQ** citations and the **Root Cause** panel — those
  two shots win the Accuracy and Reasoning marks.
- After exporting, upload **public/unlisted** to YouTube and paste the link into the Innovation
  Studio project description (TRACKER.md item 4).
