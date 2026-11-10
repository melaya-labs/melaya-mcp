#!/usr/bin/env python3
"""Caption files (SRT, VTT, ASS) from word timings or from a script plus its voice take.

  From word timings (a transcript: [{"text","start","end"}, ...], e.g. the output of a
  Whisper-class model or the HyperFrames transcribe command):
    python3 captions.py --words words.json --out captions [--total 45.0]

  From a script you voiced (no speech recognition): speech segments are measured with
  ffmpeg silencedetect and the script is split after each period and comma:
    python3 captions.py --script script.txt --audio vo.wav --offset 0.5 --out captions

Writes <out>.srt, <out>.vtt and <out>.ass (burn-in). Rules: at most --chars characters
per line (42) and 2 balanced lines; cues start on speech and hold +0.25 s after it
(at most +0.5 s); minimum 0.8 s; a cue under 0.9 s merges into the next when the gap
is under 0.6 s; at least --gap seconds between cues (0.07 = two frames); everything ends
0.4 s before --total. Lines listed in --no-burn (one per line, already on screen
verbatim) stay in SRT and VTT but are left out of the ASS burn file.
Script mode needs ffmpeg on the path.
"""
import argparse
import json
import re
import subprocess


def speech_segments(audio, noise_db=-35, min_sil=0.18):
    p = subprocess.run(["ffmpeg", "-nostdin", "-i", audio, "-af", f"silencedetect=noise={noise_db}dB:d={min_sil}", "-f", "null", "-"],
                       capture_output=True, text=True, stdin=subprocess.DEVNULL)
    h, m, sec = re.search(r"Duration: (\d+):(\d+):([\d.]+)", p.stderr).groups()
    dur = int(h) * 3600 + int(m) * 60 + float(sec)
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", p.stderr)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", p.stderr)]
    segs, t = [], 0.0
    for s, e in zip(starts, ends + [dur] * (len(starts) - len(ends))):
        if s - t > 0.05:
            segs.append((t, s))
        t = e
    if dur - t > 0.05:
        segs.append((t, dur))
    return segs


def chunks_from_script(text):
    parts = re.split(r"(?<=[.,;:?!])\s+", re.sub(r"\s+", " ", text.strip()))
    return [p for p in parts if p]


def map_chunks(chunks, segs):
    if len(chunks) == len(segs):
        return [(c, s, e) for c, (s, e) in zip(chunks, segs)]
    total = sum(len(c) for c in chunks)
    speech = sum(e - s for s, e in segs)
    out, acc = [], 0
    # place each chunk on the speech timeline by its character share
    def at(share):
        target = share * speech
        for s, e in segs:
            if target <= e - s:
                return s + target
            target -= e - s
        return segs[-1][1]
    for c in chunks:
        a0, acc = acc, acc + len(c)
        out.append((c, at(a0 / total), at(acc / total)))
    return out


def balance(text, chars):
    if len(text) <= chars:
        return [text]
    words, best = text.split(), None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        score = max(len(a), len(b)) - (6 if re.search(r"[.,;:?!]$", a) else 0)  # prefer breaks at punctuation
        if best is None or score < best[0]:
            best = (score, [a, b])
    return best[1]


def build_cues(items, chars, total, gap):
    """items: (text, start, end) phrases; returns cues (text_lines, start, end)."""
    cues = []
    for text, s, e in items:
        words = text.split()
        # split a phrase that does not fit in two lines
        while words:
            take, cur = [], ""
            for w in words:
                trial = (cur + " " + w).strip()
                if len(trial) > 2 * chars - 4 and take:
                    break
                take.append(w)
                cur = trial
            share = len(cur) / max(1, len(" ".join(words)))
            span = (e - s) * share
            cues.append([cur, s, s + span])
            s += span
            words = words[len(take):]
    # holds, minimums, merges, gaps
    for i, c in enumerate(cues):
        nxt = cues[i + 1][1] if i + 1 < len(cues) else (total - 0.4 if total else c[2] + 0.5)
        c[2] = min(c[2] + 0.25, nxt - gap)
        if c[2] - c[1] < 0.8:
            c[2] = min(c[1] + 0.8, nxt - gap)
    merged = []
    for c in cues:
        if (merged and merged[-1][2] - merged[-1][1] < 0.9 and c[1] - merged[-1][2] < 0.6
                and len(merged[-1][0]) + len(c[0]) + 1 < 80 and not re.search(r"[.?!]$", merged[-1][0])):
            merged[-1][0] = merged[-1][0] + " " + c[0]
            merged[-1][2] = c[2]
        else:
            merged.append(c)
    if total:
        merged = [c for c in merged if c[1] < total - 0.4]
        for c in merged:
            c[2] = min(c[2], total - 0.4)
    return [(balance(t, chars), s, e) for t, s, e in merged]


def ts(t, sep=","):
    t = max(0.0, t)
    h, m, s = int(t // 3600), int(t % 3600 // 60), t % 60
    return f"{h:02d}:{m:02d}:{int(s):02d}{sep}{int(round((s - int(s)) * 1000)):03d}"


def ass_ts(t):
    h, m, s = int(t // 3600), int(t % 3600 // 60), t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--words")
    ap.add_argument("--script")
    ap.add_argument("--audio")
    ap.add_argument("--offset", type=float, default=0.0, help="where the voice take starts in the piece (s)")
    ap.add_argument("--out", default="captions")
    ap.add_argument("--chars", type=int, default=42)
    ap.add_argument("--total", type=float, default=0.0, help="piece length (s)")
    ap.add_argument("--gap", type=float, default=0.07)
    ap.add_argument("--no-burn", help="file with lines already on screen verbatim")
    ap.add_argument("--font", default="Sans")
    ap.add_argument("--size", type=int, default=44)
    ap.add_argument("--width", type=int, default=1920)
    ap.add_argument("--height", type=int, default=1080)
    a = ap.parse_args()

    if a.words:
        words = json.load(open(a.words))
        words = words.get("words", words) if isinstance(words, dict) else words
        items, cur = [], None
        for w in words:
            t = str(w["text"]).strip()
            if cur is None:
                cur = [t, float(w["start"]), float(w["end"])]
            else:
                cur[0] += " " + t
                cur[2] = float(w["end"])
            if re.search(r"[.,;:?!]$", t):
                items.append(tuple(cur))
                cur = None
        if cur:
            items.append(tuple(cur))
    elif a.script and a.audio:
        segs = speech_segments(a.audio)
        items = map_chunks(chunks_from_script(open(a.script).read()), segs)
    else:
        raise SystemExit("give --words, or --script with --audio")
    items = [(t, s + a.offset, e + a.offset) for t, s, e in items]
    cues = build_cues(items, a.chars, a.total, a.gap)
    no_burn = set()
    if a.no_burn:
        no_burn = {re.sub(r"\W+", " ", l).strip().lower() for l in open(a.no_burn) if l.strip()}

    with open(a.out + ".srt", "w") as f:
        for i, (lines, s, e) in enumerate(cues, 1):
            f.write(f"{i}\n{ts(s)} --> {ts(e)}\n" + "\n".join(lines) + "\n\n")
    with open(a.out + ".vtt", "w") as f:
        f.write("WEBVTT\n\n")
        for lines, s, e in cues:
            f.write(f"{ts(s, '.')} --> {ts(e, '.')}\n" + "\n".join(lines) + "\n\n")
    with open(a.out + ".ass", "w") as f:
        f.write(f"[Script Info]\nScriptType: v4.00+\nPlayResX: {a.width}\nPlayResY: {a.height}\nWrapStyle: 2\nScaledBorderAndShadow: yes\n\n")
        f.write("[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
                "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n")
        f.write(f"Style: Cap,{a.font},{a.size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H9E000000,-1,0,0,0,100,100,0,0,3,14,0,2,200,200,52,1\n\n")
        f.write("[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
        for lines, s, e in cues:
            if re.sub(r"\W+", " ", " ".join(lines)).strip().lower() in no_burn:
                continue
            f.write(f"Dialogue: 0,{ass_ts(s)},{ass_ts(e)},Cap,,0,0,0,,{{\\fad(90,90)}}" + "\\N".join(lines) + "\n")
    print(json.dumps({"cues": len(cues), "files": [a.out + x for x in (".srt", ".vtt", ".ass")]}))


if __name__ == "__main__":
    main()
