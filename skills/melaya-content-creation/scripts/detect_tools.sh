#!/usr/bin/env bash
# Detect the tools this skill can use and print one JSON object.
# Usage: bash detect_tools.sh            (read-only: installs nothing, runs no network command)
ver() { "$@" 2>/dev/null | head -n 1 | tr -d '"\\' ; }
has() { command -v "$1" >/dev/null 2>&1; }
node_v=""; has node && node_v=$(node -v 2>/dev/null)
node_major=$(echo "$node_v" | sed -E 's/^v([0-9]+).*/\1/'); [ -z "$node_major" ] && node_major=0
ff=""; has ffmpeg && ff=$(ver ffmpeg -version | awk '{print $3}')
ffprobe_ok=false; has ffprobe && ffprobe_ok=true
libass=false; has ffmpeg && ffmpeg -hide_banner -filters 2>/dev/null | grep -q " subtitles " && libass=true
py=""; has python3 && py=$(python3 -c 'import sys;print("%d.%d"%sys.version_info[:2])' 2>/dev/null)
numpy=false; [ -n "$py" ] && python3 -c 'import numpy' 2>/dev/null && numpy=true
# HyperFrames: a cached CLI in the npm package-runner cache, or a project-local install (no network call)
hf_path=""; hf_ver=""
for p in ./node_modules/hyperframes "$HOME"/.npm/_npx/*/node_modules/hyperframes; do
  if [ -f "$p/package.json" ]; then
    v=$(sed -n 's/.*"version": *"\([^"]*\)".*/\1/p' "$p/package.json" | head -n 1)
    if [ -z "$hf_ver" ] || [ "$(printf '%s\n%s\n' "$hf_ver" "$v" | sort -V | tail -n 1)" = "$v" ]; then hf_ver=$v; hf_path=$p; fi
  fi
done
skills=""
for s in hyperframes hyperframes-core hyperframes-animation hyperframes-audio hyperframes-registry hyperframes-cli media-use remotion-to-hyperframes; do
  for base in "$HOME/.claude/skills" "$HOME/.agents/skills" "./.agents/skills" "./.claude/skills"; do
    if [ -f "$base/$s/SKILL.md" ]; then skills="$skills\"$s\","; break; fi
  done
done
skills="[${skills%,}]"
chrome=false
for c in "/Applications/Google Chrome.app" "/Applications/Chromium.app"; do [ -d "$c" ] && chrome=true; done
has google-chrome && chrome=true; has chromium && chrome=true; has chromium-browser && chrome=true
render_ready=false; [ "$node_major" -ge 22 ] && [ -n "$ff" ] && render_ready=true
cat <<JSON
{"node": "$node_v", "node_ok_for_hyperframes": $([ "$node_major" -ge 22 ] && echo true || echo false),
 "ffmpeg": "$ff", "ffprobe": $ffprobe_ok, "ffmpeg_subtitles_filter": $libass,
 "python": "$py", "numpy": $numpy,
 "hyperframes_cli_cached": "$hf_ver", "hyperframes_cli_path": "$hf_path",
 "chrome_found": $chrome, "agent_skills": $skills,
 "render_ready": $render_ready,
 "next": "$( $render_ready && echo 'build and render here (modules/hyperframes.md)' || echo 'install the missing tools with the user'"'"'s yes, or prepare the handoff (modules/tooling.md)')"}
JSON
