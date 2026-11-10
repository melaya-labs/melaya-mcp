#!/usr/bin/env bash
# Frame QA for a render: stills at given times, a contact sheet, frame count, duration and loudness.
# Usage: bash qa_frames.sh video.mp4 qa_dir "0.05 1.2 1.9 3.6 5.8" [expected_frames] [caption_band_y]
set -euo pipefail
video=$1; out=${2:-qa}; times=${3:-"0.05"}; expect=${4:-}; band=${5:-}
mkdir -p "$out"
for t in $times; do
  ffmpeg -nostdin -v error -y -ss "$t" -i "$video" -frames:v 1 "$out/qa_$t.png"
  if [ -n "$band" ]; then
    ffmpeg -nostdin -v error -y -ss "$t" -i "$video" -frames:v 1 -vf "drawbox=y=$band:w=iw:h=ih-$band:color=red@0.25:t=fill" "$out/band_$t.png"
  fi
done
ffmpeg -nostdin -v error -y -i "$video" -vf "fps=2,scale=480:-1,tile=6x6" -frames:v 1 "$out/contact.jpg"
frames=$(ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of csv=p=0 "$video")
vdur=$(ffprobe -v error -select_streams v:0 -show_entries stream=duration -of csv=p=0 "$video")
adur=$(ffprobe -v error -select_streams a:0 -show_entries stream=duration -of csv=p=0 "$video" || true)
loud=$(ffmpeg -nostdin -hide_banner -i "$video" -af ebur128=peak=true -f null - 2>&1 | awk '/Integrated loudness:/{f=1} f&&/I:/{i=$2} f&&/Peak:/{p=$2} END{print i" LUFS, true peak "p" dBFS"}' || true)
{
  echo "# QA report for $video"
  echo "- frames: $frames${expect:+ (expected $expect)}"
  echo "- video duration: $vdur s; audio duration: ${adur:-none} s"
  echo "- loudness: ${loud:-n/a} (target about -14 LUFS, -1.5 dBTP for social)"
  echo "- stills: $(ls "$out"/qa_*.png | wc -l | tr -d ' ') in $out (look at every one), contact sheet: $out/contact.jpg"
  if [ -n "$expect" ] && [ "$frames" != "$expect" ]; then echo "- FAIL: frame count differs from the plan"; fi
} | tee "$out/report.md"
