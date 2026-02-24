# The Soft Report — Pipeline Architecture
## Fully Cloud-Hosted Autonomous Daily Video Production

---

## System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    OpenClaw (VPS - $5-10/mo)                        │
│                    Pipeline Orchestrator                            │
│                                                                     │
│  Daily Cron (6 PM) ──► Skill: soft-report-daily                    │
│                                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │ Stage 1  │─►│ Stage 2  │─►│ Stage 3  │─►│ Stage 4  │           │
│  │ Ingest   │  │ Script   │  │ Voice    │  │ Video    │           │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘           │
│       │              │              │              │                 │
│  ┌────┴─────┐  ┌────┴─────┐  ┌────┴─────┐  ┌────┴─────┐           │
│  │ Stage 5  │  │ Stage 6  │  │ Stage 7  │  │ Monitor  │           │
│  │ Thumbnail│  │ Publish  │  │ Analytics│  │ Alerts   │           │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘           │
└─────────────────────────────────────────────────────────────────────┘
         │              │              │              │
         ▼              ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  Claude API │ │ ElevenLabs  │ │   RunComfy   │ │  YouTube    │
│  (scripts)  │ │ (voice TTS) │ │  (ComfyUI)   │ │  Data API   │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
                                       │
                        ┌──────────────┼──────────────┐
                        ▼              ▼              ▼
                   Lip Sync      Backdrop Gen    Composite
                  (Wav2Lip/      (FLUX/SDXL)    (ffmpeg or
                   SadTalker/                    ComfyUI)
                   LivePortrait)
         │
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     Supabase (Data Layer)                           │
│                                                                     │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐      │
│  │  episodes   │ │  scripts   │ │  analytics  │ │  config    │      │
│  │  (metadata) │ │  (content) │ │  (metrics)  │ │  (params)  │      │
│  └────────────┘ └────────────┘ └────────────┘ └────────────┘      │
│                                                                     │
│  ┌────────────┐ ┌────────────┐                                     │
│  │  Storage   │ │  Edge Fns  │                                     │
│  │  (audio,   │ │  (webhooks,│                                     │
│  │   video,   │ │   cron     │                                     │
│  │   thumbs)  │ │   backup)  │                                     │
│  └────────────┘ └────────────┘                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Stage-by-Stage Design

### Stage 1: News Ingestion
**Purpose**: Collect, rank, and select top 3-5 AI/tech stories of the day.

**Flow**:
1. OpenClaw cron triggers at ~6 PM daily
2. Fetch RSS feeds + API endpoints:
   - TechCrunch AI, The Verge AI, Ars Technica
   - ArXiv cs.AI (top papers by social engagement)
   - Hacker News /topstories (filtered for AI/ML)
   - Twitter/X trending AI topics (optional, API cost)
   - Reddit r/artificial, r/MachineLearning hot posts
3. Claude API ranks stories by: novelty, audience relevance, discussion potential
4. Claude selects top 3-5 stories with 1-sentence summaries
5. Store selected stories in Supabase `episodes` table with status `ingested`

**APIs**: RSS/Atom parsing, HN API (free), Reddit API (free tier), Claude API
**Cost**: ~$0.50-1.00/day (Claude API for ranking/selection)
**Failure mode**: If RSS feeds fail, fall back to cached source list. If Claude API fails, retry 3x then alert.

---

### Stage 2: Script Generation
**Purpose**: Generate 600-700 word script in The Soft Report's editorial voice.

**Flow**:
1. Read selected stories from Supabase
2. Claude API generates script with specific structure:
   - Cold open teaser (10 sec)
   - Soft intro with location reference (15 sec)
   - Story 1: headline + context + editorial take (60 sec)
   - Story 2: headline + context + editorial take (60 sec)
   - Story 3: headline + context + editorial take (60 sec)
   - Editorial whisper — the "so what" (30 sec)
   - Countdown 5-4-3-2-1 + sign-off (15 sec)
3. System prompt includes character bible (personality, tone, catchphrases)
4. Store script in Supabase `scripts` table
5. Update episode status to `scripted`

**APIs**: Claude API (Sonnet for cost efficiency, Opus for quality on editorial segments)
**Cost**: ~$0.30-0.80/day
**Failure mode**: If script quality check fails (length, structure), regenerate with adjusted prompt. Max 3 attempts.

**Quality gate**: Automated checks before proceeding:
- Word count 550-750
- Contains all structural segments
- No copyrighted text verbatim (Claude instructed to transform, not quote)
- Sentiment/tone within character parameters

---

### Stage 3: Voice Synthesis
**Purpose**: Convert script to ASMR whisper-style audio.

**Path A — Voice Actress (Primary)**:
1. Script chunked into segments with timing markers
2. Sent to voice actress via batch system (she records 5 episodes/batch)
3. Audio files uploaded to Supabase Storage
4. Pros: Unique voice, harder to replicate, warmer
5. Cons: Latency (batch recording), dependency on one person

**Path B — ElevenLabs (Backup/Default)**:
1. Script sent to ElevenLabs API with custom voice profile
2. ASMR-style voice settings: low pitch, slow pace, breathy quality
3. Audio returned and stored in Supabase Storage
4. Pros: Instant, consistent, no human dependency
5. Cons: Detectable as AI voice by trained ears, monthly API cost

**Path C — Open-source TTS on RunComfy (Future)**:
1. Coqui TTS / Bark / XTTS custom node on RunComfy
2. Lower quality but zero per-use cost after setup
3. Evaluate when open-source voice quality catches up

**Output**: MP3/WAV file in Supabase Storage, episode status → `voiced`
**Cost**: Path A ~$15/episode, Path B ~$10-20/day ($300-600/mo), Path C ~$0.50/day compute
**Failure mode**: If ElevenLabs fails, queue for voice actress batch. If both fail, skip day and alert.

---

### Stage 4: Video Generation (RunComfy)
**Purpose**: Generate the final video — AI host with lip sync, exotic backdrop, composited.

**This is the most complex stage. Three sub-stages on RunComfy:**

#### 4a: Backdrop Generation
**Workflow**: FLUX/SDXL on RunComfy
- Input: Location prompt from script ("rooftop garden in Kyoto at dusk")
- Output: High-quality 1920x1080 background image
- One workflow deployment, triggered via API
- Cost: ~$0.10-0.30 per image

#### 4b: Avatar/Lip Sync Generation
**Option 1: Open-source on RunComfy** (cost-effective, more control)
- **SadTalker or LivePortrait**: Reference face image + audio → talking head video
- **Wav2Lip**: Existing video + audio → lip-synced video
- Workflow: Upload reference image + audio → RunComfy API → poll for result
- Cost: ~$0.50-2.00 per 5-min video (GPU compute time)

**Option 2: HeyGen/Hedra API** (higher quality, higher cost)
- Upload avatar template + audio → API → video
- Cost: ~$20-40/day ($600-1,200/mo)

**Option 3: Hybrid**
- RunComfy generates the talking head (SadTalker/LivePortrait)
- HeyGen used only when RunComfy quality isn't sufficient
- A/B test both and let quality metrics decide

#### 4c: Compositing
**Workflow**: ComfyUI composite node OR ffmpeg on VPS
- Layer: backdrop image + talking head video + lower-third graphics + watermark
- Add intro/outro animation (pre-rendered, stored in Supabase)
- Output: Final MP4 1080p, ~5 minutes
- Store in Supabase Storage (or direct to YouTube via Stage 6)

**Total Stage 4 cost estimate**:
- Open-source path: $1-4/episode
- HeyGen path: $20-40/episode
- Hybrid: $5-15/episode

**Output**: MP4 in Supabase Storage, episode status → `rendered`
**Failure mode**: If RunComfy job fails, retry once. If still failing, alert and queue for manual review. Critical: never publish a broken video.

---

### Stage 5: Thumbnail Generation
**Purpose**: Generate click-worthy YouTube thumbnail.

**Flow**:
1. Claude API generates thumbnail concept based on top story
2. RunComfy FLUX/SDXL workflow generates the image:
   - AI host face/character (consistent reference)
   - Story-relevant visual element
   - Bold text overlay with episode hook
   - Exotic backdrop hint matching episode location
3. Store in Supabase Storage, episode status → `thumbnailed`

**Cost**: ~$0.10-0.30/thumbnail
**Alternative**: Canva API or pre-designed templates with dynamic text. Simpler, cheaper, possibly better CTR.

---

### Stage 6: Publishing
**Purpose**: Upload to YouTube and cross-post clips.

**Flow**:
1. YouTube Data API v3: upload video with metadata
   - Title: SEO-optimized (Claude generates 3 options, picks best)
   - Description: story links, timestamps, Patreon/Discord links, affiliate links
   - Tags: AI news, ASMR, tech, specific story keywords
   - Thumbnail: upload generated thumbnail
   - Schedule: 9 PM ET daily
   - AI content disclosure label (YouTube requirement)
2. Auto-generate 3x YouTube Shorts from episode highlights
   - Claude identifies the 3 most clip-worthy 30-sec segments
   - ffmpeg on VPS extracts and formats for vertical (9:16)
   - Upload as Shorts with cross-linking to full episode
3. Cross-post to TikTok/Instagram Reels (v2 — after YouTube is stable)
4. Update Supabase episode status → `published`
5. Post to Discord/community tab (if Patreon is active)

**APIs**: YouTube Data API v3 (free, quota: 10,000 units/day — upload costs 1,600 units)
**Cost**: Free (within API quotas)
**Failure mode**: If upload fails, retry 3x with exponential backoff. If still failing, alert founder for manual upload. Never double-publish.

---

### Stage 7: Analytics & Feedback Loop
**Purpose**: Track performance and feed insights back into content strategy.

**Flow** (runs daily, 24h after each episode):
1. YouTube Analytics API: pull metrics for each episode
   - Views, watch time, avg view duration, CTR, like ratio
   - Audience retention curve (where do viewers drop off?)
   - Traffic sources (search, browse, suggested, external)
   - Subscriber delta
2. Store in Supabase `analytics` table
3. Claude API analyzes weekly trends:
   - Which stories performed best/worst?
   - Which locations/backdrops correlated with higher retention?
   - Is average view duration trending up or down?
   - Content recommendations for next week
4. Weekly summary posted to founder via OpenClaw (Telegram/Discord message)
5. Monthly financial summary: revenue by stream, cost per episode, burn rate

**APIs**: YouTube Analytics API (free), Claude API
**Cost**: ~$0.10-0.20/day
**Failure mode**: Non-critical. If analytics fail, skip and retry next day.

---

## Infrastructure

### VPS (OpenClaw Host)
- **Provider**: Hetzner CX22 ($4.50/mo) or DigitalOcean Basic Droplet ($6/mo)
- **Specs**: 2 vCPU, 4GB RAM, 40GB SSD — more than enough for orchestration
- **OS**: Ubuntu 24.04 LTS
- **Running**: OpenClaw (Node.js), ffmpeg (for Shorts extraction + compositing fallback), cron
- **No GPU needed** — all heavy compute offloaded to RunComfy

### Supabase
- **Tier**: Free tier to start (500MB database, 1GB storage, 50K edge function invocations)
- **Scale to Pro ($25/mo)** when storage exceeds 1GB (~50 episodes with video files)
- **Note**: Don't store final videos in Supabase long-term. Upload directly to YouTube. Store audio, thumbnails, and metadata only.

### RunComfy
- **Deployments**: 3-4 serverless workflow endpoints:
  1. Backdrop generation (FLUX)
  2. Lip sync / talking head (SadTalker or LivePortrait)
  3. Composite (optional — may do this with ffmpeg on VPS instead)
  4. Thumbnail generation (FLUX)
- **Cost**: Pay-per-compute. Estimate $2-8/episode depending on video gen path.
- **Pro plan ($10/mo)** for discounted GPU rates and 200GB storage

---

## Cost Model Comparison

### Open-Source Path (RunComfy for video)
| Component | Monthly Cost |
|-----------|:----------:|
| VPS (Hetzner) | $5 |
| Supabase (Free→Pro) | $0-25 |
| Claude API (scripts + analysis) | $25-50 |
| ElevenLabs (voice, Path B) | $22-99 |
| RunComfy (video gen, ~22 eps) | $44-176 |
| YouTube API | Free |
| **Total** | **$96-355/mo** |

### Commercial API Path (HeyGen for video)
| Component | Monthly Cost |
|-----------|:----------:|
| VPS (Hetzner) | $5 |
| Supabase (Free→Pro) | $0-25 |
| Claude API | $25-50 |
| ElevenLabs | $22-99 |
| HeyGen/Hedra | $600-1,200 |
| RunComfy (thumbnails only) | $5-10 |
| YouTube API | Free |
| **Total** | **$657-1,389/mo** |

### Voice Actress + RunComfy (Optimal?)
| Component | Monthly Cost |
|-----------|:----------:|
| VPS (Hetzner) | $5 |
| Supabase (Free→Pro) | $0-25 |
| Claude API | $25-50 |
| Voice Actress (22 eps) | $330 |
| RunComfy (video gen) | $44-176 |
| YouTube API | Free |
| **Total** | **$404-586/mo** |

---

## Provider Abstraction Layer

Critical for resilience. Each stage should have a pluggable provider interface:

```
Stage 3 (Voice):
  ├── Provider A: ElevenLabs API
  ├── Provider B: Voice Actress (manual upload)
  └── Provider C: Open-source TTS (RunComfy/local)

Stage 4 (Video):
  ├── Provider A: RunComfy (SadTalker/LivePortrait)
  ├── Provider B: HeyGen API
  └── Provider C: Hedra API

Stage 5 (Thumbnail):
  ├── Provider A: RunComfy (FLUX)
  ├── Provider B: Canva API
  └── Provider C: Template-based (ImageMagick)
```

Config in Supabase `config` table determines which provider is active for each stage. Switchable without code changes.

---

## OpenClaw Skill Design

The pipeline runs as a single OpenClaw skill: `soft-report-daily`

```yaml
name: soft-report-daily
description: The Soft Report daily episode production pipeline
triggers:
  - cron: "0 18 * * *"  # 6 PM daily (3 hours before 9 PM publish)
  - command: "/produce"   # Manual trigger via Telegram/Discord

steps:
  - id: ingest
    action: fetch-and-rank-news
    timeout: 5m
    on_failure: alert + skip

  - id: script
    action: generate-script
    depends_on: ingest
    timeout: 3m
    on_failure: retry(3) + alert

  - id: voice
    action: synthesize-voice
    depends_on: script
    timeout: 10m
    on_failure: fallback(provider_b) + alert

  - id: backdrop
    action: generate-backdrop
    depends_on: script  # Can run parallel with voice
    timeout: 5m

  - id: avatar
    action: generate-talking-head
    depends_on: [voice, backdrop]
    timeout: 20m
    on_failure: retry(1) + alert

  - id: composite
    action: composite-final-video
    depends_on: avatar
    timeout: 10m

  - id: thumbnail
    action: generate-thumbnail
    depends_on: script  # Can run parallel with video stages
    timeout: 5m

  - id: shorts
    action: extract-shorts-clips
    depends_on: composite
    timeout: 5m

  - id: publish
    action: upload-youtube
    depends_on: [composite, thumbnail, shorts]
    timeout: 15m
    on_failure: alert(critical) + manual_queue

  - id: notify
    action: send-founder-summary
    depends_on: publish
    timeout: 1m
```

**Parallelism**: Voice (Stage 3) and Backdrop (Stage 4a) run in parallel. Thumbnail (Stage 5) runs in parallel with avatar generation. Total pipeline time: ~45-60 minutes.

---

## Supabase Schema

```sql
-- Episode lifecycle tracking
CREATE TABLE episodes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  episode_number SERIAL,
  production_date DATE NOT NULL,
  publish_date TIMESTAMPTZ,
  status TEXT NOT NULL DEFAULT 'pending',
  -- Status flow: pending → ingested → scripted → voiced → rendered → thumbnailed → published → analyzed
  stories JSONB,          -- Selected news stories
  location TEXT,          -- Backdrop location description
  youtube_video_id TEXT,
  youtube_shorts_ids JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Scripts with versioning
CREATE TABLE scripts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  episode_id UUID REFERENCES episodes(id),
  version INT DEFAULT 1,
  content TEXT NOT NULL,
  word_count INT,
  structure_valid BOOLEAN,
  voice_provider TEXT,    -- 'elevenlabs', 'actress', 'opensource'
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Asset storage references
CREATE TABLE assets (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  episode_id UUID REFERENCES episodes(id),
  asset_type TEXT NOT NULL,  -- 'audio', 'backdrop', 'avatar_video', 'composite', 'thumbnail', 'short_1', 'short_2', 'short_3'
  storage_path TEXT NOT NULL, -- Supabase Storage path
  provider TEXT,             -- Which service generated it
  metadata JSONB,            -- Duration, resolution, file size, etc.
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- YouTube analytics per episode
CREATE TABLE analytics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  episode_id UUID REFERENCES episodes(id),
  fetched_at TIMESTAMPTZ DEFAULT NOW(),
  views INT,
  watch_time_minutes FLOAT,
  avg_view_duration_pct FLOAT,
  likes INT,
  dislikes INT,
  comments INT,
  ctr FLOAT,
  subscriber_delta INT,
  traffic_sources JSONB,
  retention_curve JSONB,
  revenue_estimate FLOAT
);

-- Pipeline configuration
CREATE TABLE config (
  key TEXT PRIMARY KEY,
  value JSONB NOT NULL,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Pipeline run logs
CREATE TABLE pipeline_runs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  episode_id UUID REFERENCES episodes(id),
  started_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ,
  status TEXT DEFAULT 'running', -- running, completed, failed, partial
  stages JSONB,  -- Per-stage timing, status, errors
  total_cost FLOAT,
  notes TEXT
);
```

---

## Failure & Recovery

| Failure | Impact | Recovery |
|---------|--------|----------|
| Claude API down | Can't script | Retry 3x over 30 min. If persistent, alert + skip day. |
| ElevenLabs down | Can't voice | Fall back to voice actress queue or open-source TTS. |
| RunComfy job fails | Can't render video | Retry once. If fails, alert + queue for manual review. |
| YouTube upload fails | Can't publish | Retry 3x. If fails, alert founder for manual upload. |
| VPS goes down | Pipeline doesn't trigger | Supabase Edge Function as backup cron trigger. |
| Supabase down | No state management | Pipeline halts gracefully. Episodes queue until recovery. |

**Critical rule**: Never auto-publish a broken or low-quality video. Quality gate before Stage 6 (publish) checks: video duration within 10% of expected, audio sync verified, thumbnail exists.

---

## Phase 1 Build Order (MVP)

Build these in order, testing each before moving on:

1. **Supabase schema + config** — Foundation. 1 day.
2. **Stage 1 (Ingest)** — RSS fetching + Claude ranking. 1 day.
3. **Stage 2 (Script)** — Claude script gen with character bible. 1 day.
4. **Stage 3 (Voice)** — ElevenLabs integration. 1 day.
5. **Stage 4a (Backdrop)** — RunComfy FLUX workflow. 1-2 days.
6. **Stage 4b (Avatar)** — RunComfy lip sync workflow. 2-3 days (hardest stage).
7. **Stage 4c (Composite)** — ffmpeg on VPS. 1 day.
8. **Stage 5 (Thumbnail)** — RunComfy or template-based. 0.5 days.
9. **Stage 6 (Publish)** — YouTube Data API. 1 day.
10. **Stage 7 (Analytics)** — YouTube Analytics API. 1 day.
11. **OpenClaw orchestration** — Wire all stages into daily skill. 1-2 days.
12. **Shorts extraction** — ffmpeg clip extraction. 0.5 days.

**Total estimate: 12-15 days** for a working pipeline producing daily episodes.

---

## Open Questions

1. **Avatar reference image**: Need a consistent AI-generated host face. Generate once with FLUX/Midjourney, use as reference for all lip sync. Should this be designed first?
2. **RunComfy workflow testing**: Need to test SadTalker vs LivePortrait vs Wav2Lip quality with ASMR whisper audio before committing. Budget 1-2 days for comparison.
3. **ElevenLabs voice profile**: Need to create and fine-tune the ASMR whisper voice. May require uploading voice actress samples for voice cloning.
4. **Character bible**: Needs to be written before Stage 2 can produce consistent scripts. Personality, catchphrases, editorial perspective, what she says/doesn't say.
5. **News source licensing**: Some RSS feeds have terms of service. Review before scraping.
6. **YouTube AI disclosure**: YouTube requires labeling AI-generated content. How does this affect the algorithm? Research needed.
