#!/usr/bin/env bash
# Music bed ducked under a voiceover track, summed without normalisation, limited, at an exact length.
# Usage: bash duck_mix.sh music.wav voice.wav total_seconds out.wav [bed_volume=0.30] [voice_gain=1.8] [music_start=0]
# voice.wav is the full-length voice track (takes already placed). Optional loudness pass afterwards:
#   ffmpeg -i out.wav -af loudnorm=I=-14:TP=-1.5:LRA=11 -ar 48000 out_norm.wav
set -euo pipefail
music=$1; voice=$2; total=$3; out=$4; bed=${5:-0.30}; vgain=${6:-1.8}; mstart=${7:-0}
fade_out_start=$(python3 -c "print(max(0, $total - 1.5))" 2>/dev/null || echo 0)
ffmpeg -nostdin -v error -y -ss "$mstart" -i "$music" -i "$voice" -filter_complex \
 "[0:a]aresample=48000,aformat=channel_layouts=stereo,volume=$bed,afade=t=in:d=0.4,afade=t=out:st=$fade_out_start:d=1.5[m];\
  [1:a]aresample=48000,aformat=channel_layouts=stereo,volume=$vgain,asplit=2[vo][sc];\
  [m][sc]sidechaincompress=threshold=0.02:ratio=16:attack=6:release=650[md];\
  [md][vo]amix=inputs=2:normalize=0:duration=first,apad,atrim=0:$total,alimiter=limit=0.95[a]" \
 -map "[a]" -ar 48000 -ac 2 -t "$total" "$out"
echo "mix: $out ($(ffprobe -v error -show_entries format=duration -of csv=p=0 "$out") s)"
