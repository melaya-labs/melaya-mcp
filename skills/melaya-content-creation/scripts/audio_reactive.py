#!/usr/bin/env python3
"""Per-frame audio data for subtle audio-reactive visuals (glow, depth, presence).

    python3 audio_reactive.py music.wav --fps 30 --bands 8 [--start 0 --duration 20] [--js] > audio-data.json

Output: {"fps", "frames", "rms": [...], "bass": [...], "bands": [[...], ...]}, every
value normalised to 0..1 (each series to its own peak). Bands are log-spaced from
30 Hz to 16 kHz; band 0 is the bass. With --js, prints `var AUDIO = {...};` ready
to paste into a composition script, so nothing is fetched at render time.
Sample it on the timeline by frame index: value = AUDIO.bass[Math.round(t * fps)].
Needs ffmpeg on the path and NumPy.
"""
import argparse
import json
import subprocess

import numpy as np

SR = 44100


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("--fps", type=float, default=30.0)
    ap.add_argument("--bands", type=int, default=8)
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--duration", type=float, default=0.0)
    ap.add_argument("--js", action="store_true")
    a = ap.parse_args()
    cmd = ["ffmpeg", "-nostdin", "-v", "error", "-ss", str(a.start)]
    if a.duration:
        cmd += ["-t", str(a.duration)]
    cmd += ["-i", a.audio, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    y = np.frombuffer(subprocess.run(cmd, capture_output=True, stdin=subprocess.DEVNULL, check=True).stdout, np.float32)
    hop = SR / a.fps
    n = int(len(y) / hop)
    nfft = 4096
    freqs = np.fft.rfftfreq(nfft, 1 / SR)
    edges = np.geomspace(30, 16000, a.bands + 1)
    rms, bands = [], []
    win = np.hanning(nfft)
    for f in range(n):
        s = int(f * hop)
        frame = y[s:s + int(hop)]
        rms.append(float(np.sqrt(np.mean(frame ** 2))) if len(frame) else 0.0)
        chunk = y[s:s + nfft]
        if len(chunk) < nfft:
            chunk = np.pad(chunk, (0, nfft - len(chunk)))
        mag = np.abs(np.fft.rfft(chunk * win))
        bands.append([float(mag[(freqs >= lo) & (freqs < hi)].max(initial=0.0)) for lo, hi in zip(edges[:-1], edges[1:])])
    rms = np.array(rms)
    b = np.array(bands) if bands else np.zeros((0, a.bands))
    norm = lambda v: (v / (v.max() + 1e-9)).round(4)
    b = b / (b.max(axis=0, keepdims=True) + 1e-9)
    out = {"fps": a.fps, "frames": n, "rms": norm(rms).tolist(), "bass": b[:, 0].round(4).tolist() if n else [],
           "bands": b.round(4).tolist()}
    text = json.dumps(out, separators=(",", ":"))
    print(f"var AUDIO = {text};" if a.js else text)


if __name__ == "__main__":
    main()
