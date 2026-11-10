#!/usr/bin/env python3
"""Measure a music track's beat grid with NumPy only (no librosa), and optionally
cut per-segment beat files from a timeline.

    python3 beatgrid.py track.mp3 [--offset 0] [--duration 60] [--bpm-min 70 --bpm-max 180]
                        [--timeline timeline.json --music-start 12.5] [--out beats.json]

Prints JSON: tempo (bpm), beat length, first beat, first downbeat, bar length,
confidence (mean onset z-score on the grid; above about 2 is solid), the beat
grid, the strong downbeats (bars), loudness (RMS) every 2 s, and the strongest
onsets. With --timeline, also writes one beats file per segment with times
relative to the segment start (the music slice played under that segment starts
at --music-start + segment start in the track).

Method: mono 11025 Hz, hop 64, Hann window 1024, log-magnitude spectral flux
(z-scored) as the onset curve; comb search over the BPM range in 0.05 steps with
60 phases per beat; downbeat = the beat offset (of 4) with the strongest
low-band (kick) onsets. Half or double tempo: narrow --bpm-min / --bpm-max.
Needs ffmpeg on the path and NumPy.
"""
import argparse
import json
import subprocess
import sys

import numpy as np

SR = 11025
HOP = 64
NFFT = 1024


def decode(path, offset, duration):
    cmd = ["ffmpeg", "-nostdin", "-v", "error", "-ss", str(offset)]
    if duration:
        cmd += ["-t", str(duration)]
    cmd += ["-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    raw = subprocess.run(cmd, capture_output=True, stdin=subprocess.DEVNULL, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def onset_curves(y):
    n_frames = (len(y) - NFFT) // HOP
    if n_frames < 16:
        raise SystemExit("audio too short to analyse")
    idx = np.arange(NFFT)[None, :] + HOP * np.arange(n_frames)[:, None]
    spec = np.abs(np.fft.rfft(y[idx] * np.hanning(NFFT), axis=1))
    logs = np.log1p(spec)
    flux = np.maximum(0.0, np.diff(logs, axis=0))
    full = flux.sum(axis=1)
    kick = flux[:, 1:12].sum(axis=1)  # about 10-130 Hz
    z = lambda a: (a - a.mean()) / (a.std() + 1e-9)
    return z(full), z(kick)


def comb(onset, fps, bpm_min, bpm_max):
    best = (-1e9, None, None)
    n = len(onset)
    for bpm in np.arange(bpm_min, bpm_max + 1e-9, 0.05):
        per = 60.0 / bpm * fps
        k = np.arange(int((n - per) // per))
        if len(k) < 4:
            continue
        for ph in np.linspace(0, per, 60, endpoint=False):
            pos = (ph + per * k).astype(int)
            score = onset[pos].mean()
            if score > best[0]:
                best = (score, bpm, ph)
    return best


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("track")
    ap.add_argument("--offset", type=float, default=0.0, help="analysis start in the track (s)")
    ap.add_argument("--duration", type=float, default=0.0, help="analysis length (s), 0 = to the end")
    ap.add_argument("--bpm-min", type=float, default=70.0)
    ap.add_argument("--bpm-max", type=float, default=180.0)
    ap.add_argument("--timeline", help="timeline.json with fps and segments[{name,start_frame,frames}]")
    ap.add_argument("--music-start", type=float, default=0.0, help="track time (s) under timeline frame 0")
    ap.add_argument("--slices-dir", default=".", help="where per-segment beats files go")
    ap.add_argument("--out", help="write the result JSON here as well")
    a = ap.parse_args()

    y = decode(a.track, a.offset, a.duration)
    fps = SR / HOP
    onset, kick = onset_curves(y)
    score, bpm, phase = comb(onset, fps, a.bpm_min, a.bpm_max)
    if bpm is None:
        raise SystemExit("no tempo found")
    beat = 60.0 / bpm
    first_beat = phase / fps
    dur = len(y) / SR
    beats = np.arange(first_beat, dur, beat)
    # downbeat: which of the 4 offsets carries the strongest kick onsets
    kick_scores = []
    for o in range(4):
        pos = ((beats[o::4]) * fps).astype(int)
        pos = pos[pos < len(kick)]
        kick_scores.append(float(kick[pos].mean()) if len(pos) else -1e9)
    down_off = int(np.argmax(kick_scores))
    first_down = first_beat + down_off * beat
    bar = 4 * beat
    downbeats = np.arange(first_down, dur, bar)
    # loudness every 2 s (rising = build, plateau = body, dip = breakdown, jump = drop)
    win = int(2 * SR)
    rms = [round(float(np.sqrt(np.mean(y[i:i + win] ** 2))), 4) for i in range(0, len(y) - win + 1, win)]
    # strongest onsets near the grid (candidates for major cues)
    pos = (beats * fps).astype(int)
    pos = pos[pos < len(onset)]
    strengths = onset[pos]
    top = np.argsort(-strengths)[: min(12, len(strengths))]
    strong = sorted(round(float(beats[i]) + a.offset, 4) for i in top)

    out = {
        "track": a.track, "analysis_offset_s": a.offset, "bpm": round(float(bpm), 2), "beat_s": round(beat, 5),
        "bar_s": round(bar, 5), "first_beat_s": round(first_beat + a.offset, 4),
        "first_downbeat_s": round(first_down + a.offset, 4), "confidence": round(float(score), 3),
        "beats": [round(float(t) + a.offset, 4) for t in beats],
        "downbeats": [round(float(t) + a.offset, 4) for t in downbeats],
        "strong_onsets": strong, "rms_every_2s": rms,
    }

    if a.timeline:
        tl = json.load(open(a.timeline))
        tfps = float(tl.get("fps", 30))
        slices = {}
        for seg in tl.get("segments", []):
            s = a.music_start + seg["start_frame"] / tfps
            d = seg["frames"] / tfps
            rel = lambda arr: [round(float(t) - s, 4) for t in arr if s <= float(t) < s + d]
            entry = {"name": seg["name"], "track_start_s": round(s, 6), "duration_s": round(d, 6), "frames": seg["frames"],
                     "bpm": out["bpm"], "beats": rel(out["beats"]), "downbeats_strong": rel(out["downbeats"])}
            slices[seg["name"]] = entry
            with open(f"{a.slices_dir.rstrip('/')}/{seg['name']}.beats.json", "w") as fh:
                json.dump(entry, fh, indent=1)
        out["segments"] = slices

    text = json.dumps(out, indent=1)
    if a.out:
        open(a.out, "w").write(text + "\n")
    print(text)


if __name__ == "__main__":
    sys.exit(main())
