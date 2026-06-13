# Microsoft Agents League — Game Plan
**Deadline: Jun 14, 11:59 PM PT (= Mon Jun 15, 12:29 PM IST) — ~2 days**

## Step 0 (BLOCKING, do first)
Activate your Innovation Studios profile via the email from `InnoStudio-noreply@microsoft.com` (check junk). No active profile = no submission. Then create the Project inside Innovation Studios early — don't leave platform mechanics to the last hour.

## Recommended track: Reasoning Agents (Microsoft Foundry)
Best fit for your multi-agent experience (BobBridge, agent hackathons), and judges see fewer deep-reasoning entries than Copilot apps.

## Winning idea (primary): **IncidentIQ — Root-Cause Reasoning Agent for Production Incidents**
An agent that takes an incident alert (e.g., "checkout latency spiked 5x") and autonomously: pulls logs/metrics/deploy history (mock or real via Azure MCP tools), forms hypotheses, tests each via multi-step reasoning, ranks root causes with evidence, and drafts the post-mortem + fix PR suggestion.
- Why it wins: clear AI value (saves on-call hours), visibly demonstrates *multi-step reasoning* (hypothesis → tool call → eliminate → conclude), easy 2-min demo with a dramatic before/after.
- Stack: Microsoft Foundry (agent + reasoning loop), Azure MCP (tool access), GitHub Copilot (build assist — mention in submission), optional Agent Framework for orchestration.

### Backup ideas (if Foundry setup stalls)
1. **PolicyPilot** (Enterprise Agents track): M365 Copilot agent that answers "can I do X?" against company policy docs with cited reasoning and escalation to HR.
2. **CopilotKata** (Creative Apps track): GitHub Copilot-assisted app — interactive code-review trainer that generates flawed code and coaches users through finding bugs.

## 2-day build plan
- **Day 1 (today):** Profile activated → Foundry project up → core reasoning loop working with 2–3 mock tools (logs, metrics, deploys) → end-to-end happy path.
- **Day 2 (Jun 14):** Polish one demo scenario; record 2-min video (problem 15s → live run 75s → architecture 20s → impact 10s); draw architecture diagram (Foundry ↔ Agent Framework ↔ Azure MCP tools ↔ output); README; push public GitHub repo; **submit by night IST — don't wait for the PT deadline.**

## Submission checklist (from Microsoft's email)
- [ ] Working project on required MS tools
- [ ] Project description: problem, features, technologies, AI value
- [ ] Demo video ≤2 min, public YouTube/Vimeo link, no third-party trademarks
- [ ] Public GitHub repo in the Code Repository Link field
- [ ] Architecture diagram (Foundry / Agent Framework / Azure MCP / Copilot / Azure)
- [ ] All teammates (≤5) registered + profiles activated + added to project
