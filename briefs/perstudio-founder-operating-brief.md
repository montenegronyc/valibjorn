# ValiBjorn Founder Operating Brief
## perstudio — "Your Agent's Personal Studio"
Generated: 2026-02-21

---

## VERDICT: GO (Conditional)
**Confidence: 70%**

perstudio solves a real routing problem that nobody else has tackled: agents need production-quality generative media but can't navigate ComfyUI complexity. The founder-market fit is exceptional — a 25-year VFX veteran with deep ComfyUI expertise is one of perhaps a dozen people who could credibly build this. The business model is sound (usage-based, near-zero fixed costs, cash-flow positive from customer #1), and the $10K budget is workable because this is a variable-cost business, not a burn-rate business.

**The condition**: Zero customer conversations have occurred. Every agent flagged this. The entire thesis — that AI agencies will pay 3-5x over raw compute for intent routing — is untested. The 90-day plan starts with 10 discovery calls in Week 1, not code. If those calls reveal the pain isn't acute enough to pay for, this is a PIVOT or KILL. If they confirm it, this is a strong GO.

---

## 1. IDEA SCORECARD

| Dimension | Score (1-10) | Key Finding |
|-----------|:---:|-------------|
| Problem Severity | 7 | Real pain exists but may be 6-12 months from mass urgency. Agencies are hitting this wall on client projects today, but not all of them yet. |
| Market Size | 7 | AI agency market is growing fast. TAM for agent-native media infrastructure is nascent but expanding. Bottoms-up: 5,000+ agencies × $500/mo = $30M addressable. |
| Founder-Market Fit | 9 | 25-year VFX veteran + deep ComfyUI expertise. One of few people who understands both the creative pipeline complexity and the API abstraction needed. |
| Competitive Advantage | 7 | Nobody solves the routing problem today. But the moat is thin — fal.ai or Replicate could add an intent layer with existing infra and customer base. Speed matters. |
| Business Model Viability | 8 | Usage-based with near-zero fixed costs. Margins improve over time (Opus → self-hosted MiniMax). Breakeven at 5-8 customers. Structurally sound. |
| Unit Economics | 7 | Healthy at correct pricing ($1.50-3.00/generation). 55-75% gross margins Phase 1, improving to 78-93% with self-hosted routing. LTV:CAC favorable for PLG. |
| Distribution Feasibility | 7 | PLG + ComfyUI community + AI agent builder communities. All organic, no paid. Viable but unproven — depends on community reception and content quality. |
| Product Buildability | 8 | Solo founder can build MVP in 4-6 weeks. Tier 1 only, 5-8 workflows. The LLM router is the key technical risk — must validate routing accuracy first. |
| Fundraise Readiness | 3 | Not ready today. No traction, no co-founder. Bootstrap first. Raise $500-750K pre-seed only after 3+ paying customers. GPU credit programs are the immediate capital unlock. |
| Legal/Regulatory Risk | 7 | No regulatory blockers. But Flux.1 Dev licensing is a launch blocker (not commercially licensed). CSAM filtering is legally mandatory. Both solvable. |
| Team Readiness | 5 | Solo founder is the biggest structural risk. Manageable to ~$5-8K MRR, then needs first hire (DevRel/Support). Advisory board would help fundraising perception. |
| Timing | 6 | AI agent wave is real but agent-native media generation demand may be 6-12 months from mass adoption. First-mover advantage exists but the window is narrow — incumbents could move. |

**Overall Score: 81/120**

---

## 2. THE BUSINESS IN ONE PAGE

**Problem**: AI agencies building agents that need to generate production-quality images, video, and audio are stuck between limited model APIs (DALL-E, Flux via fal.ai) and impossibly complex ComfyUI pipelines. No existing tool solves the routing problem — mapping what an agent wants to create to the right multi-step workflow.

**Solution**: A three-tier API that gives agents ComfyUI superpowers. Tier 1: POST natural language intent, get production output. Tier 2: Discover what's possible. Tier 3: Direct workflow access for power users. An LLM router handles the hard part — selecting and parameterizing the right ComfyUI workflow.

**Customer**: AI/automation agencies (10-50 people). Buyer is the CTO or lead engineer. Trigger: client project needs generative media, no time to learn ComfyUI.

**Insight**: The routing problem is the gap nobody has filled. ComfyUI deployment tools (ComfyDeploy, ViewComfy) expose ComfyUI's complexity to the caller. Model APIs (fal.ai, Replicate) offer single-model simplicity but limited quality. perstudio sits in the middle: ComfyUI-grade quality with model-API simplicity.

**Model**: Usage-based credits. Clients pay per generation (LLM routing fee + GPU compute). $1.50-3.00 per generation depending on workflow complexity.

**Positioning**: For AI agencies building agents that need generative media, perstudio is the execution API that gives agents ComfyUI-grade output from natural language input. Unlike raw model APIs (limited quality) or ComfyUI deployment tools (still complex), perstudio solves the routing problem — your agent describes what it wants, and perstudio figures out how to make it.

---

## 3. CRITICAL RISKS (Top 5)

### Risk 1: Zero Customer Validation
- **Severity**: CRITICAL
- **Detail**: No Mom Test conversations with actual AI agencies. The core assumption — that agencies will pay 3-5x over raw compute for routing/abstraction — is entirely untested. 11 of 13 agents flagged this.
- **Mitigation**: 10 discovery calls in Week 1-2. Use the Mom Test framework. Don't pitch — ask about their last project that needed generative media. What did they do? What was painful? What would they pay for?
- **Owner**: Founder

### Risk 2: LLM Routing Accuracy
- **Severity**: HIGH
- **Detail**: If the intent router picks the wrong workflow >30% of the time, the core value proposition fails. No amount of marketing or sales compensates for a router that doesn't work. This is untested.
- **Mitigation**: Build the router first. Test with 100 synthetic prompts. If accuracy <70%, rethink the approach before building the full MVP. This is a Week 1-2 technical validation, not a Month 2 problem.
- **Owner**: Founder

### Risk 3: Competitive Response from Incumbents
- **Severity**: HIGH
- **Detail**: fal.ai ($54M raised) or Replicate ($60M+) could add an intent routing layer with existing infrastructure, customer base, and distribution. They have the resources; they just haven't built it yet.
- **Mitigation**: Speed is the moat. Ship first, build community trust, accumulate workflow library depth. The curated workflow library with typed template slots is defensible if built fast enough. Monitor competitor product announcements weekly.
- **Owner**: Founder

### Risk 4: Flux.1 Dev Licensing
- **Severity**: HIGH (Launch Blocker)
- **Detail**: Flux.1 Dev is NOT commercially licensed. Using it in a paid API without a license from Black Forest Labs is infringement. This could block launch or create legal liability.
- **Mitigation**: Either obtain a commercial license from Black Forest Labs OR exclude Flux Dev from the workflow library at launch. Use only commercially-licensed models (SDXL, open Flux variants, etc.).
- **Owner**: Founder

### Risk 5: Solo Founder Single Point of Failure
- **Severity**: MEDIUM
- **Detail**: One person doing engineering, sales, support, ops, content, and GPU management. Context switching degrades everything. 24-hour outages are possible. Ceiling at ~$5-8K MRR before something breaks.
- **Mitigation**: Time-blocking (70% engineering Month 1, shifting to 40% by Month 3). Managed/serverless infrastructure to minimize ops. First hire (DevRel/Support contractor) triggered at $3K MRR, not calendar-based.
- **Owner**: Founder

---

## 4. CROSS-SKILL INSIGHTS

### Reinforcing Signals (13/13 agents converge)
- **Customer validation is job #1**: Every agent that touches market assumptions flagged zero Mom Test conversations. This is not a nice-to-have — it's the gating condition on the GO verdict.
- **PLG is the right motion**: GTM, Sales, Marketing, Growth all independently concluded product-led growth with community seeding. The API itself is the demo. The docs are the marketing.
- **$10K is enough**: Finance confirmed this is a variable-cost business. Near-zero fixed costs (~$120-170/mo in dev mode). $10K is a cash buffer, not burn runway. Cash-flow positive from customer #1 if pricing is right.
- **Routing accuracy is the product**: Product, Growth, and Idea Validation all identified LLM routing as the make-or-break technical risk. If it doesn't work, nothing else matters.
- **Docs = Marketing = Onboarding = Support**: Customer Success, Marketing, GTM, and Sales all converged on the same insight — for a dev tool, documentation quality is the entire go-to-market motion.

### Contradictions Found
- **Pricing divergence**: Business Model suggests $0.10-0.50/generation. Finance says margins are unsustainable below $1.50/generation (25% gross margin at $1.00 with $0.75 COGS). **Resolution**: Price at $1.50-3.00/generation for complex workflows. The Business Model agent was pricing closer to raw compute; Finance correctly identified that the abstraction layer justifies and requires higher pricing. Anchor against "hiring a ComfyUI specialist" ($8-15K/mo), not against raw GPU costs.
- **Free tier sizing**: Growth says 100 free calls, Sales says 50. **Resolution**: Start at 50 free calls. At ~$0.75 COGS per call, 100 free calls = $75/signup cost. With $10K budget and uncertain conversion, conservative is correct. Can always increase.
- **First hire timing**: Operations says no hire before $3K MRR. Customer Success says support hire at 30-50 customers. **Resolution**: These are consistent — 30 customers × $200/mo average ≈ $6K MRR. Hire a part-time DevRel/Support contractor at $3K MRR, full-time at $6K+ MRR.

### Information Gaps
- **Actual agency demand**: Will agencies pay 3-5x over raw compute? Unknown. Requires customer conversations.
- **Routing accuracy**: Can an LLM reliably map natural language to the right ComfyUI workflow? Requires synthetic testing.
- **GPU cost per workflow**: Actual COGS varies by workflow complexity. Need benchmarking of the 5-8 MVP workflows.
- **Market timing**: Is demand 3 months away or 12? Live market research shows the agent wave is real but the specific need for agent-generated media may be early.

---

## 5. 90-DAY ACTION PLAN

### Month 1: Validate (Don't Build Yet)
- **Week 1-2**: 10 discovery calls with AI agency CTOs/engineers. Use the Mom Test. Don't pitch perstudio — ask about their generative media pain. Simultaneously: build the LLM router and test with 100 synthetic prompts.
- **Week 3-4**: If routing accuracy >70% AND discovery calls confirm pain: build MVP (Tier 1 only, 5-8 curated workflows, API key auth, webhook delivery, usage metering). If either fails: PIVOT or KILL.
- **Key milestone**: Validated demand signal from 10 conversations + routing accuracy >70% on synthetic prompts.

### Month 2: Ship & Seed
- **Week 5-6**: Ship v0.1 to 5-10 beta users (from discovery calls + ComfyUI community). White-glove onboard each one personally. Free tier: 50 generations.
- **Week 7-8**: Write 3 foundational content pieces (blog + Twitter thread + YouTube tutorial). Start daily presence in ComfyUI Discord and AI agent communities. Apply to GPU credit programs (NVIDIA Inception, GCP, AWS Activate, RunPod).
- **Key milestone**: 10 active developers making API calls. First feedback on routing quality and workflow gaps.

### Month 3: Convert & Learn
- **Week 9-10**: Usage-based conversion from free tier. Iterate on workflows based on actual usage patterns. Launch on Show HN.
- **Week 11-12**: First case study from a beta user. Product Hunt launch. Begin collecting LOIs for fundraise collateral.
- **Key milestone**: 3-5 paying customers. $500+ MRR. First case study published.

---

## 6. BUSINESS MODEL & UNIT ECONOMICS

- **Model**: Usage-based credits (1 credit = $0.01). Pay-per-generation with complexity-based pricing.
- **Pricing**: $1.50-3.00 per generation (simple: $1.50, complex/multi-step: $2.50-3.00). $5 free credits on signup (≈50 simple generations).
- **COGS per generation**: $0.50-1.25 (GPU compute $0.30-1.00 + LLM routing $0.02-0.25 depending on Opus vs self-hosted)
- **Gross Margin**: 55-75% Phase 1 (Opus routing), improving to 78-93% Phase 3 (self-hosted MiniMax + reserved GPUs)
- **LTV** (estimated): $2,400-4,800 at $200-400/mo average × 12-month retention
- **CAC** (estimated): $50-150 (organic/PLG, mostly founder time)
- **LTV:CAC**: 16-32x (very healthy for PLG)
- **Breakeven**: 5-8 paying customers at $200/mo average
- **Payback Period**: Near-instant for PLG (no paid acquisition costs)
- **Positioning anchor**: "Cheaper than hiring a ComfyUI specialist ($8-15K/mo)" — this is the value frame, not raw GPU cost comparison.

### Margin Improvement Path
| Phase | Routing Cost | GPU Cost | Blended Margin |
|-------|-------------|----------|:--------------:|
| 1: Opus API | $0.02-0.25/call | Serverless ($0.30-1.00) | 55-75% |
| 2: Self-hosted MiniMax | $0.001-0.005/call | Serverless | 70-90% |
| 3: Reserved GPUs | $0.001-0.005/call | Reserved ($0.15-0.50) | 78-93% |

Self-hosted MiniMax routing breaks even at ~3,000 calls/month. Don't self-host before Month 4-5.

---

## 7. GO-TO-MARKET STRATEGY

- **Motion**: Product-Led Growth with community seeding + founder-led sales-assist for accounts >$500/mo
- **Primary Channel**: ComfyUI community (Discord, Reddit) + AI agent builder communities (Twitter/X, LangChain/CrewAI forums)
- **Secondary Channel**: SEO content targeting "ComfyUI API", "AI agent image generation", "add image gen to AI agent"
- **First 100 Customers**:
  1. 10 from discovery calls (Month 1)
  2. 20 from ComfyUI community engagement (Month 2-3)
  3. 30 from Show HN + Product Hunt launches (Month 3)
  4. 40 from SEO + content marketing + word of mouth (Month 4-6)
- **Launch Plan**:
  - Pre-launch (Week 1-4): Community presence, value-first engagement, build credibility as "the ComfyUI-for-agents expert"
  - Soft launch (Week 5-8): 10-20 beta users, white-glove onboarding, iterate on feedback
  - Public launch (Week 9-12): Show HN + Product Hunt + Twitter announcement
- **Budget**: $0-1K on marketing. Everything else is organic. $7K+ goes to GPU infrastructure.

---

## 8. PRODUCT ROADMAP

### MVP — Weeks 1-4 (after validation)
- `POST /generate` with natural language intent (Tier 1 only)
- LLM intent router (Opus 4.6)
- 5-8 curated workflows: product photo background swap, social media image generation, image upscaling, background removal, style transfer, portrait enhancement, text overlay, marketing banner
- API key authentication
- Webhook delivery + job status polling
- Usage metering and rate limiting
- Basic error handling and retry logic

### V1.1 — Weeks 5-8
- `GET /capabilities` (Tier 2 — discovery)
- Interactive API playground on landing page
- Auto-generated OpenAPI docs
- Python SDK
- Self-serve signup + Stripe billing
- LangChain / CrewAI tool wrappers

### V1.2 — Weeks 9-12
- Tier 3 endpoints (browse workflows, inspect slots, run specific pipelines)
- Self-hosted MiniMax 2.5 routing (if volume justifies)
- Status page
- Usage dashboards and spend alerts for customers

### V2.0 — Months 4-6
- Video generation workflows
- Multi-step pipeline composition
- Workflow marketplace (community contributions)
- Custom LoRA / model upload

**North Star Metric**: Weekly API Calls from Paying Accounts

**Critical Technical Gate**: Build the LLM router first. Test with 100 synthetic prompts. If routing accuracy <70%, stop and rethink before building anything else.

---

## 9. FUNDRAISE ASSESSMENT

- **Ready to raise?**: No. Readiness is 2/10 today. No traction, no revenue, no co-founder.
- **Recommended path**: Bootstrap for 60-90 days. Raise only after 3+ paying customers.
- **Recommended stage**: Pre-seed ($500-750K on YC standard post-money SAFE, $4-6M cap)
- **Immediate capital unlock**: Apply to ALL GPU credit programs simultaneously:
  - NVIDIA Inception: up to $50K in GPU credits
  - GCP for Startups: up to $100K
  - AWS Activate: up to $100K
  - Azure for Startups: up to $150K
  - RunPod / Modal startup programs
  - This alone could add $100-300K in effective runway at zero cost.
- **Key gaps to close before raising**:
  1. 3+ paying customers (proves demand)
  2. Working demo (the POST /generate → output live demo is the pitch)
  3. Unit economics data (actual margins, not estimates)
  4. Advisory board or "founding engineer" hire to mitigate solo founder concern
- **Investor targeting**: AI/ML angels, dev tools micro-funds (Heavybit, Boldstart, Essence VC), AI agency founders as angels
- **$10K allocation**: $4K GPU compute, $1.5K LLM routing, $1K marketing/docs, $500 hosting, $3K reserve

---

## 10. LEGAL CHECKLIST

- **Entity**: Wyoming single-member LLC (~$300). Convert to Delaware C-Corp only if raising VC within 12 months.
- **Immediate actions (before launch)**:
  - [ ] Terms of Service with limitation of liability and indemnification
  - [ ] Privacy Policy (GDPR-compliant if targeting UK/EU agencies)
  - [ ] Acceptable Use Policy (NSFW content, deepfakes, IP infringement)
  - [ ] CSAM prevention: implement prompt filtering at minimum. Legally mandatory under 18 U.S.C. § 2252A.
  - [ ] Resolve Flux.1 Dev licensing: obtain commercial license OR exclude from workflow library
  - [ ] Business bank account (separate from personal)
  - [ ] Stripe account for usage-based billing
- **Before fundraise**:
  - [ ] Consider Delaware C-Corp conversion ($1,500-3,000)
  - [ ] Cap table preparation (Carta or Pulley free tier)
  - [ ] YC standard post-money SAFE template
  - [ ] DPA template ready for enterprise agency customers
- **Regulatory considerations**:
  - ComfyUI GPL-3.0: SaaS architecture is compliant (no distribution). Any custom nodes that are *distributed* must be open-sourced.
  - Open-source model licensing: verify commercial use rights for every model in the workflow library
  - AI-generated content copyright: outputs are likely not copyrightable. Set expectations in ToS.
  - IP-Adapter with face images creates CSAM and deepfake liability risk. Consider restricting or monitoring.

*Note: This is educational information, not legal advice. Consult a qualified attorney.*

---

## 11. METRICS TO TRACK FROM DAY 1

| Metric | Target | Why |
|--------|--------|-----|
| Discovery calls completed | 10 in Week 1-2 | Validates demand before building |
| LLM routing accuracy | >70% on synthetic tests | Core product viability gate |
| Time-to-first-API-call | <5 minutes | PLG activation metric |
| Weekly API calls (paying) | 500+ by Month 3 | North Star metric |
| Intent-to-output success rate | >80% | Quality metric — did the agent get what it asked for? |
| Gross margin per generation | >50% | Unit economics health |
| Monthly paying customers | 3-5 by Month 3 | Revenue traction |
| MRR | $500+ by Month 3 | Fundraise readiness signal |
| Customer churn rate | <5% monthly | LTV sustainability |
| GPU cost per free-tier signup | <$5 | PLG economics |

---

## 12. WHAT COULD KILL THIS

### 1. Nobody Actually Wants This (Demand Risk)
The entire thesis is untested. AI agencies might solve generative media needs with simpler approaches (direct model APIs, hiring a contractor, or waiting for models to get good enough that ComfyUI pipelines aren't needed). If the 10 discovery calls reveal lukewarm interest, this is a KILL — not because the product is bad, but because the market isn't ready. **Probability: 35%.**

### 2. fal.ai or Replicate Ships a Routing Layer (Competitive Risk)
These companies have $100M+ in funding, existing developer customer bases, and GPU infrastructure. If they add natural language intent routing (a few months of engineering work for them), perstudio's differentiation evaporates overnight. The only defense is speed — get to market first, build workflow library depth, and create community trust before they notice. **Probability: 25% within 12 months.**

### 3. The Router Doesn't Work Well Enough (Technical Risk)
If the LLM can't reliably map natural language to the right ComfyUI workflow — wrong workflow selection, bad parameter patching, inconsistent output quality — the core product fails. No amount of marketing fixes a broken router. This is why the 100-prompt synthetic test is the first thing to do, before any other work. **Probability: 20%.**

---

*Generated by ValiBjorn — Hyperthreaded Business Validation Engine*
*13 parallel skill-agents | 50+ practitioner frameworks | Cross-skill signal weaving*
*Based on frameworks from YC, Sequoia, April Dunford, Lenny Rachitsky, and dozens more*
