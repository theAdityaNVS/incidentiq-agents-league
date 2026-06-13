# IncidentIQ — 2-Minute Demo Video Script & Shotlist

**Goal:** show visible multi-step reasoning + Foundry IQ grounding, polished and clear, in ≤2:00.
Record at 1080p. No third-party trademarks/music. Upload to YouTube/Vimeo (public) and put the
link in the Innovation Studio project description.

**Setup before recording:** server running (`uvicorn incidentiq.api:app --app-dir src`), browser at
`http://localhost:8000`, zoom ~110%, hide bookmarks bar.

| Time | On screen | Voiceover (read aloud) |
|------|-----------|------------------------|
| 0:00–0:12 | Dashboard loaded; incident card visible | "When checkout latency spikes 5x, on-call engineers burn hours correlating logs, metrics, and recent deploys under pressure. IncidentIQ does that reasoning in seconds." |
| 0:12–0:20 | Hover the incident card (INC-4471) | "Here's the alert: checkout-api p95 jumped from 240ms to 1.3 seconds." |
| 0:20–0:30 | Click **Run Agent Diagnosis** | "I hand it to the agent." |
| 0:30–0:55 | Reasoning console streams: 3 hypotheses, then tool calls | "It forms three hypotheses, then pulls evidence with tools — deploy history, metrics, logs — exactly like an SRE would." |
| 0:55–1:15 | Hypothesis cards resolve: 1 KEPT (green), 2 ELIMINATED (red) with reasoning | "It eliminates the upstream-dependency and CPU theories with evidence — the gateway is flat, CPU isn't saturated — and keeps the deploy regression." |
| 1:15–1:30 | Root Cause panel; point at the cited **[RB-12] / [PM-INC-3990]** evidence lines | "The root cause is pinpointed — a new Redis-backed token cache with an undersized pool — and it's **grounded in our runbooks via Foundry IQ**, with citations, so it's not hallucinated." |
| 1:30–1:42 | Mitigation + Durable Fix cards; click **View Post-Mortem** | "It drafts the mitigation, the durable fix, and a full post-mortem — including the grounded sources." |
| 1:42–1:52 | Cut to `docs/architecture.svg` | "Foundry agent, Foundry IQ knowledge base, tools, cited output." |
| 1:52–2:00 | Back to dashboard / title card | "Hours to seconds — grounded, cited, and safe: fixes are suggested, never auto-executed. That's IncidentIQ." |

## Rubric coverage (say/show at least one cue for each)
- **Reasoning & multi-step (20%)** — the streaming hypothesis→tool→eliminate→conclude (0:30–1:15).
- **Accuracy & relevance (20%)** — cited Foundry IQ grounding (1:15–1:30).
- **Reliability & safety (20%)** — "suggested, never auto-executed" + offline fallback (1:52–2:00).
- **UX & presentation (15%)** — the polished dashboard throughout.
- **Creativity (15%)** — incident RCA as visible, cited agent reasoning.

## Recording tips
- Pre-run once so model/animation is warm; keep one clean take of the diagnosis stream.
- If demoing Foundry mode live is risky on stage, record with local mode (identical UX) — it always runs.
- Keep cursor movements deliberate; pause ~1s on the cited evidence and the root-cause panel.
