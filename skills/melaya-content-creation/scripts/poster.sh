#!/usr/bin/env bash
# Pick a settled frame as poster.jpg and bake it as frame 0 (duration, frame count and audio unchanged).
# Usage: bash poster.sh video.mp4 3.2 [poster.jpg]
set -euo pipefail
video=$1; t=$2; poster=${3:-$(dirname "$video")/poster.jpg}
ffmpeg -nostdin -v error -y -ss "$t" -i "$video" -frames:v 1 -q:v 2 "$poster"
tmp="${video%.*}.poster.tmp.mp4"
ffmpeg -nostdin -v error -y -i "$video" -i "$poster" \
  -filter_complex "[0:v][1:v]overlay=0:0:enable='eq(n,0)'[v]" -map "[v]" -map "0:a?" \
  -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -c:a copy -movflags +faststart "$tmp"
before=$(ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of csv=p=0 "$video")
after=$(ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of csv=p=0 "$tmp")
if [ "$before" != "$after" ]; then echo "frame count changed ($before -> $after); keeping the original" >&2; rm -f "$tmp"; exit 1; fi
mv "$tmp" "$video"
echo "poster: $poster (t=$t s), baked as frame 0 of $video ($after frames)"
