# Recording with a stopwatch

Two PowerShell helpers in `scripts/`:

- `timer.ps1`: an always-on-top window that never takes focus (so it cannot steal input from Paint), showing a stopwatch. It starts when the start flag file appears and freezes (green, "Done") when the stop flag file appears. Params: `-StartFlag`, `-StopFlag` (Windows or Git Bash paths), `-Title`, `-Subtitle`, `-X`, `-Y` (default 1290, 420: right of a centred canvas at 1920x1080; keep it off the canvas and the ribbon).
- `record.ps1`: ffmpeg gdigrab of the whole desktop at 30 fps (libx264 ultrafast, CRF 23, 1 s keyframes, fragmented MP4), stopped GRACEFULLY by sending `q` when its stop flag appears, after `-TailSeconds` (3) more seconds so the frozen stopwatch and the finished canvas are in the footage, then remuxed with `+faststart` to `-Out`.

## Recipe

```bash
S=$(cygpath -w "$SKILL_DIR/scripts"); F=C:\\tmp\\run1          # any folder for the flag files
rm -f /c/tmp/run1.start /c/tmp/run1.stop /c/tmp/run1.rec.stop
powershell -NoProfile -Command "Start-Process powershell -WindowStyle Hidden -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File','$S\\record.ps1','-Out','C:\\Users\\<user>\\Downloads\\run1.mp4','-StopFlag','$F.rec.stop'"
powershell -NoProfile -Command "Start-Process powershell -WindowStyle Hidden -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-STA','-File','$S\\timer.ps1','-StartFlag','$F.start','-StopFlag','$F.stop','-Subtitle','Mona Lisa | one call'"
```

1. Run the pre-flight. Make sure Paint is still in front after starting the helpers (both are no-activate, but check `melaya_computer_current_app`).
2. In ONE short Bash call, touch the start flag: `touch /c/tmp/run1.start`. Your very next tool call is `melaya_computer_batch` with the stored plan.
3. Collect with `run_id` until the summary arrives. The moment it arrives, your very next tool call is ONE Bash command that only touches both stop flags: `touch /c/tmp/run1.stop /c/tmp/run1.rec.stop`. Put nothing before it in that command (no sleep, no kill, no remux).
4. `record.ps1` keeps recording 3 s, stops ffmpeg cleanly and writes the MP4.

## What the stopwatch shows

The visible time is wall time from the start touch to the stop touch. It includes the MCP call latency before the tool starts executing (about 3 s) and the agent's latency between the batch summary and the stop touch (several seconds: model turn plus any Bash hooks). It is therefore a few seconds longer than the run's own execution time in the batch summary; report the batch's own duration as the run time and say the stopwatch includes that latency.

## The bug this replaces (verified)

In the Mona Lisa recording the stopwatch looked like it never stopped. Cause: the stop flag was touched about 8 s after the batch returned, in the same command as `sleep 4; taskkill //F //IM ffmpeg.exe`. Force-killing ffmpeg on a fragmented MP4 dropped the last fragment (x264's default keyframe interval is 250 frames, about 8 s), so the footage ended before the freeze (the remux printed "Invalid NAL unit size ... missing picture"). The timer itself froze correctly. Fixes: `record.ps1` (graceful `q`, 1 s keyframes, tail seconds), flags touched alone and immediately, timer paths tested literally, stale stop flag removed at launch. Verified: flags 4 s apart froze the clock at 00:04.0 and the recording kept 3.4 s of the frozen green clock.
