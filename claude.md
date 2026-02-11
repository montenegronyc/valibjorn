# ValiBjorn

Hyperthreaded multi-agent business validation engine for Claude Code.

Based on the [Linus Beliunas one-person unicorn concept](https://www.linkedin.com/pulse/built-complete-startup-operating-system-using-ai-12-linus-beliunas-wofqe/) — 12 interconnected startup skills covering the entire founder journey — but reimagined and expanded as a parallel orchestration system that runs 14 agents simultaneously and weaves them into a single, integrated Founder Operating Brief.

## What It Does

You describe your startup idea. ValiBjorn launches 14 specialized AI agents in parallel:

| Agent | Analyzes |
|-------|----------|
| Idea Validation | GO/PIVOT/KILL using YC, Mom Test, Bilyeu frameworks |
| Business Model | Model selection, pricing, unit economics, positioning |
| Fundraising | Pitch deck, VC psychology, projections, readiness |
| Go-to-Market | Launch strategy, channels, first 100 customers |
| Product | MVP scope, PRD skeleton, roadmap, user stories |
| Sales | Sales motion, methodology, outreach, pipeline |
| Marketing & Brand | Brand voice, content pillars, SEO, PR, community |
| Growth & Analytics | AARRR metrics, North Star, retention, experiments |
| Operations | Hiring plan, OKRs, board readiness |
| Finance & Accounting | Burn rate, runway, cash flow, financial model |
| Customer Success | Onboarding, churn prevention, health scoring |
| Legal & Compliance | Entity, equity, vesting, SAFEs, compliance |
| Competitive Intelligence | Landscape mapping, moat analysis, incumbent threats, market timing |
| Name & Trademark | Name generation, conflict checking, domain validation |

The results are woven together — contradictions surfaced, risks aggregated, signals cross-referenced — into a unified **Founder Operating Brief** with a GO/PIVOT/KILL verdict.

## What Makes This Different

| Beliunas Original | ValiBjorn |
|-------------------|-----------|
| Sequential skill execution | 14 parallel agent threads |
| Each skill standalone | Signals propagate between agents |
| 12 separate outputs | One unified Founder Operating Brief |
| Manual skill selection | Auto-orchestration of all 14 |
| Single pass, one skill at a time | Simultaneous analysis with cross-weaving |

## Installation

1. Clone this repo
2. Copy the `skills/valibjorn/` folder into your Claude Code skills directory:
   ```bash
   cp -r skills/valibjorn ~/.claude/skills/valibjorn
   ```
3. Use it in Claude Code by saying: **"validate my idea"** or **"valibjorn"**

## Usage

```
> validate my idea: [describe your startup concept]
```

ValiBjorn will:
1. **Intake** — Ask 7 diagnostic questions about your idea, market, and founder context
2. **Dispatch** — Launch 14 parallel skill-agents via Claude Code's Task tool
3. **Weave** — Cross-reference findings, resolve contradictions, aggregate risks
4. **Synthesize** — Produce a unified Founder Operating Brief
5. **Deliver** — Present the brief with GO/PIVOT/KILL verdict and 90-day action plan

## Project Structure

```
skills/valibjorn/
├── SKILL.md                      # Orchestrator (intake, dispatch, weave, synthesize)
└── references/
    ├── idea-validation.md        # Kevin Hale/YC, Mom Test, GO/PIVOT/KILL
    ├── business-model.md         # 55 patterns, pricing, unit economics, Dunford
    ├── fundraising.md            # Pitch deck, VC research, projections, outreach
    ├── go-to-market.md           # Rachitsky tactics, Racecar, first 100 customers
    ├── product.md                # PRD (Yien/Square), RICE, user stories, roadmap
    ├── sales.md                  # MEDDIC/BANT/Challenger, outreach, demos, pipeline
    ├── marketing-brand.md        # Brand voice, content, SEO, PR, community
    ├── growth-analytics.md       # AARRR, North Star, A/B testing, cohorts
    ├── operations.md             # Hiring, OKRs, board management, updates
    ├── finance-accounting.md     # Burn rate, runway, cash flow, reporting
    ├── customer-success.md       # Onboarding, churn, NPS, health scoring
    ├── legal-compliance.md       # Entity, vesting, ESOP, SAFEs, cap table
    ├── competitive-intelligence.md # Porter's 5 Forces, 7 Powers, moat analysis, incumbent threats
    └── name-trademark.md         # Name generation, conflict search, domain validation
```

## Frameworks Included

Distilled from 50+ practitioners and methodologies:

- **YC** (Kevin Hale, standard documents, SAFE)
- **April Dunford** (positioning methodology)
- **Lenny Rachitsky** (GTM tactics, growth, retention)
- **Rob Fitzpatrick** (The Mom Test)
- **Tom Bilyeu** (60-minute validation)
- **Sequoia** (pitch deck structure)
- **Intercom** (RICE scoring, PRD philosophy)
- **Google/Liz Wessel** (OKR framework)
- **MEDDIC, BANT, Challenger, SPIN** (sales methodologies)
- **Hamilton Helmer** (7 Powers moat framework)
- **Michael Porter** (Five Forces, competitive strategy)
- **Clayton Christensen** (disruption theory, innovator's dilemma)
- And many more embedded in each agent's prompt

## Output: The Founder Operating Brief

A single integrated document containing:

1. **Verdict** — GO / PIVOT / KILL with confidence score
2. **Idea Scorecard** — 14 dimensions scored 1-10
3. **Business in One Page** — Problem, solution, customer, insight, model, positioning
4. **Critical Risks** — Top 5 with severity, mitigation, and owner
5. **Cross-Skill Insights** — Reinforcing signals, contradictions, information gaps
6. **90-Day Action Plan** — Month-by-month with specific weekly actions
7. **Business Model & Unit Economics** — Model, pricing, LTV, CAC, margins
8. **Go-to-Market Strategy** — Motion, channels, first 100 customers, launch plan
9. **Product Roadmap** — MVP/V1.1/V2 with North Star metric
10. **Fundraise Assessment** — Readiness, stage, amount, gaps
11. **Legal Checklist** — Entity, equity, compliance
12. **Metrics to Track** — Day 1 dashboard
13. **What Could Kill This** — Top 3 existential threats

## License

MIT
