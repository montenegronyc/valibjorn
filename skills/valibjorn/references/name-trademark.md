# Name & Trademark Validation — Agent Reference

## Purpose
Validate that a proposed business name is safe to use commercially, identify conflicts, assess risk severity, and generate viable alternatives when the name is taken.

## Why This Agent Exists
A great business idea with a taken name is a preventable disaster. Founders waste months building brand equity around names they'll have to abandon. Trademark disputes are expensive ($50K-$250K to litigate), disruptive (forced rebrand), and entirely avoidable with 30 minutes of upfront research. This agent catches name collisions before the first dollar is spent on branding.

---

## PHASE 1: NAME CONFLICT SEARCH

### Search Methodology (Ordered by Priority)

#### 1. Web Presence Search
For the proposed name, search for:
- `"[name]"` — exact match
- `"[name] software"` — software/SaaS context
- `"[name] [industry]"` — industry-specific collision
- `"[name] app"` — app store presence
- `"[name] trademark"` — explicit trademark mentions

#### 2. Domain Availability Check
Check availability or current ownership of:
- `[name].com` — primary (most important)
- `[name].ai` — AI/tech products
- `[name].io` — developer/SaaS products
- `[name].co` — startup alternative
- `[name].app` — app products
- `[name][industry].com` — industry-specific fallback (e.g., `namelaw.com`)

#### 3. Trademark Database Search
- Search USPTO TESS (Trademark Electronic Search System) via web
- Search `https://tmsearch.uspto.gov` for registered and pending marks
- Note: International marks (EU EUIPO, UK IPO, WIPO) are relevant if expanding globally

#### 4. Software Registry Search
- GitHub: `github.com/[name]` and `github.com/search?q=[name]`
- npm: `npmjs.com/package/[name]`
- PyPI: `pypi.org/project/[name]`
- App stores (if relevant): search iOS App Store and Google Play

#### 5. Social Media Handle Check
- Twitter/X: `x.com/[name]`
- LinkedIn company: `linkedin.com/company/[name]`
- These are less critical but affect brand buildability

### Conflict Classification

For each conflict found, classify:

| Severity | Criteria | Action |
|----------|----------|--------|
| **BLOCKING** | Same name, same industry, registered trademark | Name is dead. Must rename. |
| **HIGH** | Same name, adjacent industry, active product | Strongly recommend rename. Legal risk is real. |
| **MODERATE** | Same name, different industry, no trademark | Usable with caution. Monitor and consider trademark filing. |
| **LOW** | Similar name, different industry, no trademark | Likely safe. Document the difference. |
| **CLEAR** | No meaningful conflicts found | Proceed. File trademark application. |

### Conflict Report Format

```markdown
## Name Conflict Report: [Proposed Name]

### Overall Verdict: [CLEAR / CAUTION / RENAME REQUIRED]

### Conflicts Found

| # | Entity | Industry | URL/Source | Registered TM? | Severity |
|---|--------|----------|------------|:---:|----------|
| 1 | [name] | [industry] | [url] | Yes/No/Unknown | BLOCKING/HIGH/MODERATE/LOW |

### Domain Status
- .com: [Available / Taken by X]
- .ai: [Available / Taken by X]
- .io: [Available / Taken by X]
- .co: [Available / Taken by X]

### Assessment
[2-3 sentences on whether this name is usable and what the primary risk is]

### Recommendation
[PROCEED / PROCEED WITH CAUTION / RENAME REQUIRED]
```

---

## PHASE 2: NAME BRAINSTORMING

When a name conflict requires renaming (or when the founder requests alternatives), generate candidates using these frameworks:

### Naming Frameworks

#### 1. Descriptive Names
Names that describe what the product does.
- Formula: `[Action] + [Object]` or `[Domain] + [Capability]`
- Examples from industry: Salesforce, Dropbox, YouTube, Basecamp
- Pros: Immediately understandable, good SEO
- Cons: Hard to trademark, can feel generic

#### 2. Metaphor Names
Names that evoke the product's essence through analogy.
- Formula: Think about what the product is LIKE, not what it IS
- Examples: Amazon (vast selection), Slack (loose communication), Notion (ideas)
- Pros: Memorable, trademarkable, brand-buildable
- Cons: Require more marketing to explain

#### 3. Coined/Invented Names
Entirely new words, often blending roots.
- Formula: `[Root 1] + [Root 2]` or phonetic invention
- Examples: Spotify (spot + identify), Hulu (Chinese: gourd/storage), Zillow (zillions + pillow)
- Pros: Highly trademarkable, unique, .com often available
- Cons: No inherent meaning, require brand-building investment

#### 4. Founder/Story Names
Names from the founding story or personal context.
- Formula: Draw from the problem, the origin story, the "aha moment"
- Examples: Under Armour (founder's sweat problem), Warby Parker (Kerouac characters)
- Pros: Authentic, conversational, differentiating
- Cons: May not scale, can feel small

#### 5. Acronym/Abbreviation Names
Names from initials or shortened forms.
- Formula: Take a descriptive phrase and abbreviate
- Examples: IBM, SAP, HubSpot
- Pros: Clean, professional, scalable
- Cons: Generic feeling, hard to remember initially

### Name Quality Criteria

Score each candidate 1-5 on:

| Criterion | Description | Weight |
|-----------|-------------|--------|
| **Uniqueness** | No conflicts in target industry | 25% |
| **Memorability** | Easy to remember after hearing once | 20% |
| **Pronounceability** | Easy to say, spell, and type | 15% |
| **Domain availability** | .com or strong alternative available | 15% |
| **Trademarkability** | Distinctive enough for TM registration | 15% |
| **Brand fit** | Matches positioning, tone, and audience | 10% |

### Industry-Specific Naming Considerations

#### Legal Tech
- Tone: Professional, trustworthy, authoritative
- Avoid: Cute/playful names, anything that sounds like a game or social app
- Good patterns: Latin/legal etymology, strength metaphors, intelligence/clarity metaphors
- Examples of good legal tech names: Relativity, Everlaw, Clio, LexisNexis, Fastcase

#### B2B SaaS
- Tone: Clean, competent, scalable
- Avoid: Names that sound like consumer apps
- Good patterns: Compound words, strong verbs, clarity/precision metaphors

#### Consumer/B2C
- Tone: Approachable, memorable, shareable
- Avoid: Names that sound like enterprise software
- Good patterns: Short (1-2 syllables), evocative, emotionally resonant

### Brainstorm Output Format

```markdown
## Alternative Name Candidates for [Original Name]

### Positioning Context
[1-2 sentences on what the product does, who it's for, and what brand tone is needed]

### Candidates

| # | Name | Type | .com? | Rationale | Score |
|---|------|------|:---:|-----------|:---:|
| 1 | [name] | [framework] | ✅/❌ | [why this works] | [X/25] |

### Top 3 Recommendations
1. **[Name]** — [Why this is the best option. 1-2 sentences.]
2. **[Name]** — [Why this is second best.]
3. **[Name]** — [Why this is third.]

### Quick Conflict Check
[For the top 3, note any obvious web presence conflicts found]
```

---

## PHASE 3: TRADEMARK FILING GUIDANCE

If the name is clear or a new name is selected:

### Pre-Filing Checklist
- [ ] Comprehensive web search shows no conflicts in target class
- [ ] Domain secured (at minimum .com or primary alternative)
- [ ] Social handles available or acquirable
- [ ] No USPTO registered marks in relevant classes
- [ ] Name passes the "phone test" (easy to spell when heard)

### Nice Classification for Common Startup Types
- **Class 9**: Software, mobile apps, downloadable software
- **Class 35**: Business consulting, data analysis services
- **Class 42**: SaaS, cloud computing, software design
- **Class 45**: Legal services (relevant for legal tech)
- **Class 36**: Financial services (relevant for fintech)

### Filing Recommendations
- **Intent-to-Use (ITU)**: File before launch to establish priority date ($250-350 per class)
- **Use-Based**: File after using the name in commerce ($250-350 per class)
- **Timeline**: ~12-18 months for registration if no opposition
- **Cost**: $250-350 per class (USPTO filing) + $0-2,000 for attorney review

*Note: This is educational information, not legal advice. Consult a trademark attorney for formal filing.*

---

## SIGNALS FOR OTHER AGENTS

The Name & Trademark agent should flag:
- **For Marketing/Brand**: Name availability affects brand strategy, domain-driven marketing, SEO
- **For Legal/Compliance**: Trademark registration should be on the legal checklist
- **For Finance**: Trademark filing costs ($500-2,500) and potential rebrand costs if deferred
- **For Go-to-Market**: Domain availability affects launch timeline and channel strategy
- **For Fundraising**: A clean, trademarkable name strengthens investor pitch

---

## AGENT OUTPUT SCHEMA

```
agent_name: "name_trademark"
output: Full conflict report + brainstormed alternatives (if needed)
confidence_score: 0-100 (based on search thoroughness — web searches may miss some conflicts)
risks: Name-specific risks (conflicts found, trademark exposure, domain issues)
signals: Cross-agent signals (brand impact, legal filing needs, cost implications)
frameworks_applied: "Name Conflict Search, Domain Check, USPTO Search, Naming Frameworks (Descriptive/Metaphor/Coined/Story/Acronym), Name Quality Scoring, Nice Classification"
```
