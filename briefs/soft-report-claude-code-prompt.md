# Claude Code Prompt: Build The Soft Report Pipeline

Copy everything below the line into a fresh Claude Code session.

---

## Project Setup

I'm building **The Soft Report** — a fully automated daily YouTube channel that produces 5-minute AI/tech news briefings delivered by an AI-generated female host in ASMR whisper voice, set against rotating exotic global backdrops.

The entire pipeline runs autonomously with <1hr/week human intervention.

## Tech Stack

- **Orchestration**: OpenClaw (running on Hetzner VPS, Ubuntu 24.04)
- **Data Layer**: Supabase (Postgres + Storage + Edge Functions)
- **Script Generation**: Claude API (Anthropic)
- **Voice Synthesis**: ElevenLabs API (primary), with voice actress upload path as backup
- **Avatar / Lip Sync**: HeyGen API (primary) — frontier-quality talking head generation. Must be frontier quality for ASMR format where viewers scrutinize the face.
- **Backdrop & Thumbnails**: RunComfy (cloud-hosted ComfyUI) — FLUX/SDXL for exotic location images and YouTube thumbnails
- **Compositing**: ffmpeg on VPS (layer backdrop + HeyGen avatar output + lower-thirds + watermark)
- **Publishing**: YouTube Data API v3
- **Analytics**: YouTube Analytics API
- **Language**: TypeScript (OpenClaw skills) + Python (utility scripts if needed)

## Architecture

The pipeline has 7 stages that run daily, triggered by OpenClaw cron at 6 PM ET:

```
Stage 1: News Ingestion — Fetch RSS/APIs, Claude ranks and selects top 3-5 stories
Stage 2: Script Generation — Claude writes 600-700 word script in character voice
Stage 3: Voice Synthesis — ElevenLabs converts script to ASMR whisper audio
Stage 4: Video Generation — RunComfy generates backdrop, HeyGen generates lip-synced avatar, ffmpeg composites
Stage 5: Thumbnail — RunComfy FLUX generates click-worthy YouTube thumbnail
Stage 6: Publish — YouTube Data API uploads video scheduled for 9 PM ET
Stage 7: Analytics — YouTube Analytics API pulls metrics, Claude analyzes trends
```

Stages 3 and 4a (backdrop) run in parallel. Stage 5 (thumbnail) runs in parallel with Stage 4b/4c (avatar + composite).

## Supabase Schema

Create these tables first:

```sql
-- Episode lifecycle tracking
CREATE TABLE episodes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  episode_number SERIAL,
  production_date DATE NOT NULL,
  publish_date TIMESTAMPTZ,
  status TEXT NOT NULL DEFAULT 'pending',
  stories JSONB,
  location TEXT,
  youtube_video_id TEXT,
  youtube_shorts_ids JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE scripts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  episode_id UUID REFERENCES episodes(id),
  version INT DEFAULT 1,
  content TEXT NOT NULL,
  word_count INT,
  structure_valid BOOLEAN,
  voice_provider TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE assets (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  episode_id UUID REFERENCES episodes(id),
  asset_type TEXT NOT NULL,
  storage_path TEXT NOT NULL,
  provider TEXT,
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

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

CREATE TABLE config (
  key TEXT PRIMARY KEY,
  value JSONB NOT NULL,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE pipeline_runs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  episode_id UUID REFERENCES episodes(id),
  started_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ,
  status TEXT DEFAULT 'running',
  stages JSONB,
  total_cost FLOAT,
  notes TEXT
);
```

## Provider Abstraction

Each external API should be wrapped in a provider interface so we can swap providers without changing pipeline logic:

```typescript
// Voice providers
interface VoiceProvider {
  synthesize(script: string, voiceConfig: VoiceConfig): Promise<AudioAsset>;
}
// Implementations: ElevenLabsProvider, VoiceActressProvider, OpenSourceTTSProvider

// Backdrop providers (image generation)
interface BackdropProvider {
  generate(locationPrompt: string): Promise<ImageAsset>;
}
// Implementations: RunComfyProvider, DalleProvider

// Avatar / Lip Sync providers (talking head video)
interface AvatarProvider {
  generateTalkingHead(avatarId: string, audio: AudioAsset): Promise<VideoAsset>;
}
// Implementations: HeyGenProvider (primary), HedraProvider, RunComfyProvider (future — SadTalker/LivePortrait when quality catches up)

// Thumbnail providers
interface ThumbnailProvider {
  generate(concept: string, referenceImage: string): Promise<ImageAsset>;
}
// Implementations: RunComfyProvider, CanvaProvider, TemplateProvider
```

Active provider for each stage is stored in Supabase `config` table and read at runtime.

## HeyGen Integration (Avatar / Lip Sync — Primary)

HeyGen handles the hardest part: frontier-quality talking head generation with lip sync. This MUST be high quality — ASMR viewers stare at the face and listen closely. Any uncanny valley kills the format.

**HeyGen API flow:**
1. Pre-create an avatar (one-time setup in HeyGen dashboard — upload reference photos/video of the AI host character)
2. For each episode: POST audio file + avatar ID → HeyGen renders talking head video
3. Poll for completion → download MP4
4. Composite with backdrop using ffmpeg

**Key HeyGen API endpoints:**
- Create video from avatar + audio
- Check video generation status
- Download completed video

HeyGen pricing is per-minute of generated video. ~5 min/episode at their rates = primary cost driver.

**Future migration path:** When open-source lip sync (SadTalker, LivePortrait, or whatever comes next) reaches frontier quality, swap HeyGen for RunComfy via the provider abstraction layer. Monitor quality quarterly.

## RunComfy Integration (Backdrops + Thumbnails)

RunComfy handles image generation only (not video — that's HeyGen's job for now):

```
POST https://api.runcomfy.net/prod/v1/deployments/{deployment_id}/inference
Authorization: Bearer {api_token}
Content-Type: application/json

{
  "overrides": {
    "node_id": {
      "inputs": { ... }
    }
  }
}
```

Jobs are async — POST to queue, poll status, GET result when complete. We need 2 deployed workflows:
1. Backdrop generation (FLUX/SDXL) — exotic location images, 1920x1080
2. Thumbnail generation (FLUX) — click-worthy YouTube thumbnails, 1280x720

## OpenClaw Skill Structure

The pipeline runs as an OpenClaw skill. Structure it as:

```
skills/
  soft-report/
    skill.yaml          # Skill definition, cron trigger
    src/
      pipeline.ts       # Main orchestrator
      stages/
        ingest.ts       # Stage 1: News ingestion
        script.ts       # Stage 2: Script generation
        voice.ts        # Stage 3: Voice synthesis
        video.ts        # Stage 4: Video generation (backdrop + avatar + composite)
        thumbnail.ts    # Stage 5: Thumbnail generation
        publish.ts      # Stage 6: YouTube upload
        analytics.ts    # Stage 7: Analytics collection
      providers/
        claude.ts       # Claude API wrapper
        elevenlabs.ts   # ElevenLabs API wrapper
        heygen.ts       # HeyGen API wrapper (avatar + lip sync)
        runcomfy.ts     # RunComfy API wrapper (backdrops + thumbnails)
        youtube.ts      # YouTube Data + Analytics API wrapper
        supabase.ts     # Supabase client
      config/
        character.ts    # Character bible (personality, voice params, editorial rules)
        sources.ts      # RSS feed URLs, API endpoints
      utils/
        ffmpeg.ts       # ffmpeg compositing and Shorts extraction
        quality.ts      # Quality gates (word count, duration check, sync verification)
```

## Character Bible

The AI host character (name TBD, channel name "The Soft Report") has these traits:
- Warm, intelligent, slightly wry
- Speaks in whisper register — intimate, not sleepy
- Has opinions but presents them as observations, not arguments
- References previous episodes (continuity)
- Signature countdown: "Five... four... three... two... one. Sweet dreams, darlings."
- Never uses hyperbole or clickbait language
- Explains technical concepts through metaphor, not jargon
- Slight sense of mystery — where is she broadcasting from? Why does the location change daily?

Include this as a system prompt template that Stage 2 (script generation) uses every episode.

## Quality Gates

Before publishing (Stage 6), verify:
- [ ] Video duration within 4:30-5:30 (±30 sec of target)
- [ ] Audio and video are in sync (lip sync check — even basic duration matching)
- [ ] Thumbnail exists and is correct dimensions (1280x720)
- [ ] Script word count was 550-750
- [ ] YouTube title is <100 chars, description includes required links
- [ ] AI content disclosure is set in YouTube metadata

If any gate fails, alert founder and do NOT publish. Queue for manual review.

## Environment Variables Needed

```
ANTHROPIC_API_KEY=
ELEVENLABS_API_KEY=
ELEVENLABS_VOICE_ID=
HEYGEN_API_KEY=
HEYGEN_AVATAR_ID=
RUNCOMFY_API_TOKEN=
RUNCOMFY_BACKDROP_DEPLOYMENT_ID=
RUNCOMFY_THUMBNAIL_DEPLOYMENT_ID=
SUPABASE_URL=
SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=
YOUTUBE_CLIENT_ID=
YOUTUBE_CLIENT_SECRET=
YOUTUBE_REFRESH_TOKEN=
OPENCLAW_WEBHOOK_URL=  # For alerts
```

## Build Order

Build and test each stage independently before wiring them together:

1. **Supabase schema** — Run the SQL above. Seed config table with default providers.
2. **Stage 1 (Ingest)** — RSS fetching + Claude story ranking. Test: outputs 3-5 ranked stories.
3. **Stage 2 (Script)** — Claude script generation with character bible. Test: produces a structurally valid 600-700 word script.
4. **Stage 3 (Voice)** — ElevenLabs whisper synthesis. Test: produces clear ASMR-quality audio from script.
5. **Stage 4a (Backdrop)** — RunComfy FLUX workflow. Test: produces 1920x1080 exotic location image.
6. **Stage 4b (Avatar)** — HeyGen API: upload audio + avatar ID → talking head video. Test: produces frontier-quality lip-synced video from audio. This is the quality-critical stage — if the output isn't convincing for ASMR close-up viewing, the whole format fails.
7. **Stage 4c (Composite)** — ffmpeg layering. Test: produces final video with backdrop + HeyGen avatar output + lower-third graphics.
8. **Stage 5 (Thumbnail)** — RunComfy FLUX. Test: produces 1280x720 thumbnail.
9. **Stage 6 (Publish)** — YouTube Data API. Test: uploads test video (unlisted).
10. **Stage 7 (Analytics)** — YouTube Analytics API. Test: pulls metrics for existing video.
11. **Orchestrator** — Wire all stages into pipeline.ts with error handling, parallelism, and status tracking.
12. **Shorts extraction** — ffmpeg clip cutting. Test: produces 3 vertical clips from full episode.
13. **OpenClaw skill wiring** — Cron trigger, manual trigger, alerting.

## Constraints

- All compute is cloud-hosted. No local GPU required. Heavy work offloaded to RunComfy.
- The VPS (Hetzner CX22, 2 vCPU, 4GB RAM) runs OpenClaw + ffmpeg only.
- Target total pipeline runtime: <60 minutes from trigger to published.
- Target cost: ~$25-40/episode (HeyGen + ElevenLabs + RunComfy). HeyGen is the primary cost driver. When open-source lip sync reaches frontier quality, swap via provider abstraction to cut cost to <$10/episode.
- Must be resilient to individual API failures — retry logic + fallback providers + alerts.
- Never auto-publish a quality gate failure. Fail safely and alert.

## Start Here

Begin with Step 1 (Supabase schema). Set up the database, then work through each stage. I want to see each stage working independently before we wire them together. Let's go.
