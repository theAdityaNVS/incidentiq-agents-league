# Foundry IQ Integration — Plan & Cost (the mandatory requirement)

## The situation (read first)
The Agents League rules state: **"all projects must integrate with at least one of the
Microsoft IQ intelligence layer: Foundry IQ, Work IQ, or Fabric IQ."** This is not optional —
an entry that doesn't integrate an IQ layer **does not qualify**, regardless of how good the
agent is.

All three IQ layers are Azure services. **Foundry IQ** (agentic knowledge retrieval inside
Azure AI Foundry) is the natural fit for IncidentIQ, so "not connecting to Azure at all" and
"qualifying for the hackathon" are mutually exclusive. The good news: the integration we need
can be done for **~$0** using free tiers + the new-account credit. Details below.

## Good news on cost — it's effectively free
| Component | Cost for this hackathon |
|-----------|------------------------|
| New Azure free account | **$200 credit, 30 days** + free services. Card needed for identity check only; **not charged** unless you manually switch to pay-as-you-go. |
| Azure AI Foundry platform + Playground | **Free** to use/explore. |
| Foundry Agent Service (agent instances) | **No charge** for agent instances. |
| Foundry IQ knowledge base (Azure AI Search) | Has a **free tier** + a **free token allocation** for agentic retrieval. A demo-sized KB fits in free. |
| Model inference (use `gpt-4o-mini`) | Billed per token but tiny — a whole demo (small KB + ~dozens of runs) is **well under $1**, covered by the $200 credit. |
| **Realistic total for the hackathon** | **$0** (inside free tier + free credit). Worst case a few dollars. |

So the answer to "how do we make it free or cheap": **create a free Azure account, use the
Azure AI Search free tier for the Foundry IQ knowledge base, the free Foundry Agent Service,
and `gpt-4o-mini` for inference.** Stay inside free credit; never flip to pay-as-you-go.

## How IncidentIQ will use Foundry IQ (minimal, demo-ready, and judge-friendly)
Foundry IQ = grounded, **cited** answers from a knowledge base to reduce hallucination. We add
a small knowledge base of **runbooks + past post-mortems + service docs**, and the agent queries
it during diagnosis so every hypothesis is backed by a cited source.

```
Incident → Foundry agent (run_foundry)
            ├─ tools: get_recent_deploys / get_metrics / get_logs   (telemetry)
            └─ Foundry IQ knowledge base (agentic retrieval)         (grounding)
                 e.g. "Runbook RB-12: checkout-api Redis pool default = 10"
          → ReasoningTrace now carries citations → post-mortem cites sources
```
This directly earns rubric points: **Accuracy & Relevance (20%)** and **Reliability & Safety (20%)**
("grounded, cited, reduces hallucination" is literally Foundry IQ's value prop).

## Step-by-step setup (≈30–45 min, $0)
1. Create a **free Azure account** → get $200 credit. (Student? Azure for Students gives credit with no card.)
2. In **Azure AI Foundry**, create a project; deploy **`gpt-4o-mini`**.
3. Create an **Azure AI Search** resource on the **Free tier**; create a **Foundry IQ knowledge base** over a new repo folder `knowledge/` (drop in 3–6 markdown runbooks/post-mortems).
4. Fill the **`run_foundry` stub** in `src/incidentiq/agent.py`:
   - create/connect the Foundry agent with `tools.TOOL_SPECS` **plus** a Foundry IQ retrieval tool,
   - run the same hypothesis→tool→eliminate→conclude loop,
   - attach retrieved citations to each `Hypothesis.evidence` and into the post-mortem.
5. Config via `.env` (already git-ignored): `PROJECT_ENDPOINT`, `MODEL_DEPLOYMENT_NAME`, search endpoint/key. **Never commit `.env`.**
6. Test: `python -m incidentiq.main --foundry` and the web app's diagnose path; keep **local mode as the live-demo fallback** in case of network/quota hiccups on stage.

## Cost-control rules
- Use `gpt-4o-mini` (not a frontier model) for all calls.
- Keep the knowledge base small (a handful of docs) → stays in Search free tier.
- Cap demo runs; don't loop the agent unattended.
- **Do not enable pay-as-you-go.** Monitor the credit balance in the Azure portal.

## Fallback if you truly cannot use Azure
**GitHub Models** offers free model inference and pairs with the GitHub Copilot CLI the
hackathon promotes — useful for the LLM. **But GitHub Models is *not* a Microsoft IQ layer**,
so it does **not** satisfy requirement #1 and the entry would not qualify on the mandatory
criterion. Recommendation: do the free Azure Foundry IQ path above; it's the only route that
both qualifies and stays free.

## Sources
- [Foundry IQ FAQ — Microsoft Learn](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/foundry-iq-faq)
- [Foundry IQ product page](https://azure.microsoft.com/en-us/products/ai-foundry/iq/)
- [Agentic Retrieval overview — Azure AI Search](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview)
- [Azure AI Search pricing (Foundry IQ)](https://azure.microsoft.com/en-us/pricing/details/search/)
- [Foundry Agent Service pricing](https://azure.microsoft.com/en-us/pricing/details/foundry-agent-service/)
- [Microsoft Foundry pricing](https://azure.microsoft.com/en-us/pricing/details/ai-foundry/)
- [Create an Azure free account ($200 credit)](https://azure.microsoft.com/en-us/pricing/purchase-options/azure-account)
- [Azure for Students](https://azure.microsoft.com/en-us/free/students)
