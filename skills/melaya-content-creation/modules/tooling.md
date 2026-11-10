# Tooling, hosts and the no-renderer handoff

> **Use when:** starting work on a new machine or host, deciding what can be built here, installing the renderer and media tools, running inside a host without a shell (a chat, a hosted agent, a pipeline step), or preparing a handoff for someone else to render.
> **Inputs:** the host (a coding agent with a shell, or not), the deliverables in the brief.
> **Outputs:** a tool status line in `brief.md`; installed tools (only with the user's yes); or the handoff package.
> **Next:** [hyperframes.md](hyperframes.md) when a renderer is available, otherwise the handoff below.

## Detect first

Run [../scripts/detect_tools.sh](../scripts/detect_tools.sh) (prints one JSON object) or check by hand:

| Tool | Needed for | Check | Minimum |
|---|---|---|---|
| Node.js | HyperFrames, Remotion, browser captures | `node -v` | 22 for HyperFrames 0.8+, 18 for Remotion |
| ffmpeg and ffprobe | every mix, frame grab, poster, encode, caption burn | `ffmpeg -version` | a build with libx264, libass and the `subtitles` filter |
| HyperFrames CLI | build, check, render, tts, transcribe, beats | the CLI's `doctor --json` (always exits 0: read its `ok` field) | 0.8 for `check`, `beats`, `keyframes` |
| Chrome or Chromium | headless rendering | `doctor` reports it; the CLI can download a pinned one | |
| Python 3 with NumPy | beat grid, audio-reactive data, caption files | `python3 -c "import numpy"` | 3.9 |
| A speech recogniser | captions from recorded speech | the HyperFrames `transcribe` command, or faster-whisper | |

## Install (ask first)

Installing software changes the user's machine: show the commands and run them only after a yes, or hand them over.

```bash
# macOS
brew install node ffmpeg
# Debian or Ubuntu
sudo apt-get install -y nodejs ffmpeg python3-numpy
# Windows
winget install OpenJS.NodeJS.LTS Gyan.FFmpeg
# HyperFrames runs through the npm package runner; pin the version a project uses
npx hyperframes@latest doctor --json
npx hyperframes browser ensure
# optional: the HyperFrames agent skills (composition rules, registry, media tools)
npx skills add heygen-com/hyperframes
```

Behind a certificate-intercepting proxy, the package runner can fail to reach the registry even when the package is cached: run the cached CLI directly and pin a known-good version. In a sandbox that kills Chrome at launch, render outside the sandbox or hand off.

## Hosts

| Host | How this skill loads | What it can do |
|---|---|---|
| A coding agent with a shell (Claude Code, Codex CLI, Gemini CLI, Cursor, others) | as a skill folder, or `SKILL.md` as project instructions | everything: build, check, render, mix, QA |
| A chat or hosted assistant with no shell | `SKILL.md` and the modules as uploaded knowledge or instructions | plan, write, design and author the composition source as files or text; hand off rendering |
| An automated pipeline step or a business agent | its instructions or a knowledge source made of these files | the same as a chat unless it is given a renderer tool; produce the handoff package |

When the HyperFrames agent skills are installed, prefer them for composition rules and media resolution ([hyperframes.md](hyperframes.md)); this skill keeps the creative method, the brand, the story, the quality bar and the delivery.

## Fallbacks

| Missing | Do instead |
|---|---|
| Any shell | the handoff package below |
| Node or the CLI (and the user declines to install) | write the composition and the handoff; or build stills only as HTML for a human to capture |
| ffmpeg | render without mixing: put music, voice and SFX as audio elements inside the composition; skip poster bake and burn-in, and list them in the handoff |
| ffmpeg without the `subtitles` filter (no libass) | captions as a caption track inside the composition, or a transparent caption-band overlay; or a full ffmpeg build with the user's yes |
| Python and NumPy | the CLI's `beats` command for the beat grid; captions timed from the transcribe output |
| A voice engine | write the voiceover script with per-line timing budgets for a human or a hosted voice |
| Music | a silent master with the cue plan, or a generated bed with the user's yes |
| Network at render time | everything already local (it must be anyway) |

## The handoff package (no renderer here)

Deliver, as files or as clearly separated text blocks:

1. `brief.md`, `script.md`, `storyboard.md`, `design.md`, `timeline.json`.
2. `composition/index.html` (and sub-compositions) complete, with every asset listed by its expected relative path and source (`assets/ledger.md`).
3. The exact commands to run, in order: install check, lint, check, draft render, frame grabs, final render, poster bake, mix and caption burn.
4. The QA checklist with the reveal and transition times to look at ([../templates/render-checklist.md](../templates/render-checklist.md)).
5. `share-copy.txt` and the publishing package.

Say plainly that nothing was rendered, and what the person running it should expect (duration, frame count, file names).

## Working alongside other agents

Each builder writes only inside its own folder; long renders run in the background with a log that ends in an explicit exit line; tool calls stay short (a few minutes at most) so a hung step is noticed; one live screen capture at a time.
