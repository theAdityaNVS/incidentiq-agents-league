# IncidentIQ — Full Demo Recording Script

This script includes an **Intro**, **Outro**, clear **Actions & Clicks**, and highlights when to show the **Azure Dashboard** and **GitHub Codebase** to maximize your evaluation marks.

---

### **Phonetic Pronunciation Guide**
*   **IncidentIQ** $\rightarrow$ *"Incident I-Q"*
*   **INC-4471** $\rightarrow$ *"I-N-C forty-four seventy-one"*
*   **checkout-api** $\rightarrow$ *"checkout A-P-I"*
*   **p95** $\rightarrow$ *"P ninety-five"*
*   **14:05 UTC** $\rightarrow$ *"fourteen-oh-five U-T-C"*
*   **H1 / H2 / H3** $\rightarrow$ *"H-one, H-two, and H-three"*
*   **Foundry IQ** $\rightarrow$ *"Foundry I-Q"*

---

## **Recording Walkthrough**

### **1. Introduction & Azure Dashboard (0:00–0:15)**
*   **[ACTION]** Start the video on your **Azure Monitor Dashboard** (or Vercel dashboard) showing the latency chart spiking. Point your cursor at the peak of the spike.
*   **[SPEECH]** 
    > "Hi, I'm Aditya. Today I'm excited to show you **IncidentIQ**, a telemetry-aware reasoning agent designed to resolve complex cloud incidents in seconds instead of hours. Let's look at a live incident where checkout latency on our system has spiked five-x."

### **2. Transition to IncidentIQ Alert (0:15–0:25)**
*   **[ACTION]** Switch tabs to the **IncidentIQ Dashboard**. Move your cursor to hover over the alert details on the incident card **INC-4471**, pointing to the **checkout-api** tag and **14:05 UTC** timestamp.
*   **[SPEECH]**
    > "Here is the alert on our dashboard: **checkout-api** p-ninety-five latency has jumped from two-hundred and forty milliseconds to one point three seconds, starting fourteen-oh-five U-T-C."

### **3. Triggering the Diagnosis (0:25–0:32)**
*   **[ACTION]** Move your cursor to the **Run Agent Diagnosis** button and click it. The status badge will change to **Agent Diagnosing**.
*   **[SPEECH]**
    > "Let’s trigger the reasoning agent and watch it run."

### **4. Streaming Console & GitHub Codebase (0:32–0:55)**
*   **[ACTION]** Let the streaming console print its initial hypotheses ($H_1$, $H_2$, $H_3$). While it streams, switch tabs to your **GitHub repository** showing `agent.py` or the tool schemas, scroll down for 2 seconds, then switch back to the streaming console.
*   **[SPEECH]**
    > "As the agent starts, it forms three hypotheses: a bad deploy, an upstream dependency, or resource exhaustion. Under the hood, the agent leverages tools—defined in our GitHub repository here—to fetch recent deploys, telemetry metrics, and logs, exactly like a human SRE."

### **5. Hypothesis Evaluation (0:55–1:12)**
*   **[ACTION]** Scroll down to the **Hypothesis Evaluation** section. Point your cursor at the green/red cards showing the gateway and CPU theories being eliminated.
*   **[SPEECH]**
    > "It automatically correlates the telemetry and rules out upstream gateway and C-P-U theories with evidence—the gateway is flat and C-P-U is under forty percent—pointing us directly to a deploy regression."

### **6. Root Cause & Grounded Citations (1:12–1:32)**
*   **[ACTION]** Scroll to the **Identified Root Cause** block. Hover your cursor over the **Grounded in Foundry IQ** badge and pause on the citation chips: **RB-12** and **PM-INC-3990**.
*   **[SPEECH]**
    > "The agent pinpoints the regression: version two point forty-one changed the token cache to Redis with an undersized connection pool. Crucially, the analysis is grounded in our runbooks via **Foundry I-Q**, citing exact documents to eliminate hallucinations."

### **7. Action Items & Outro (1:32–2:00)**
*   **[ACTION]** Scroll to the action section. Click **View Full Post-Mortem Report** to open the markdown modal, scroll down once, and close it. Hover your cursor over the **Execute Rollback** and **Draft PR Fix** buttons.
*   **[SPEECH]**
    > "It synthesizes immediate fixes, drafts a complete post-mortem report, and provides safe, human-in-the-loop actions like rolling back the deployment. Hours of triage, resolved safely in seconds. That's **IncidentIQ**. Thanks for watching!"
