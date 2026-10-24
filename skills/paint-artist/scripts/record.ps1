# Screen recorder for a run: ffmpeg capture of the whole desktop (GPU Desktop Duplication first), stopped GRACEFULLY ('q' on stdin) when -StopFlag
# appears, then remuxed with +faststart. Never stop the recorder with taskkill /F: a hard kill drops the last
# fragment (up to one GOP), so the end of the run (the frozen stopwatch) would be missing from the footage.
# Usage (background): powershell -NoProfile -ExecutionPolicy Bypass -File record.ps1 -Out C:\Users\me\Downloads\run.mp4 `
#        -StopFlag C:\tmp\rec.stop [-Fps 30] [-TailSeconds 3]
param([Parameter(Mandatory)][string]$Out, [Parameter(Mandatory)][string]$StopFlag, [int]$Fps = 30, [int]$TailSeconds = 3)
function Norm([string]$p) {
  if ($p -match '^/([a-zA-Z])/(.*)$') { $p = $Matches[1] + ':\' + ($Matches[2] -replace '/', '\') }
  return [IO.Path]::GetFullPath($p)
}
$Out = Norm $Out; $StopFlag = Norm $StopFlag
if ([IO.File]::Exists($StopFlag)) { [IO.File]::Delete($StopFlag) }
$raw = [IO.Path]::ChangeExtension($Out, '.raw.mp4')
# Capture paths, cheapest first. gdigrab (GDI BitBlt + CPU x264) competes with the painted app and slowed Paint about 3x
# in recorded runs; Desktop Duplication (ddagrab) keeps frames on the GPU: Quick Sync encodes them zero-copy on the
# display GPU, NVENC takes a download first, gdigrab is the last resort. A path that fails exits within ~2 s.
# -g = 1 s keyframe interval: short fragments, so even an unexpected crash loses at most ~1 s
$frag = "-movflags +frag_keyframe+empty_moov `"$raw`""
$paths = @(
  @('ddagrab+qsv',   "-y -loglevel error -f lavfi -i ddagrab=output_idx=0:framerate=$($Fps):draw_mouse=1,hwmap=derive_device=qsv,format=qsv -c:v h264_qsv -global_quality 23 -g $Fps $frag"),
  @('ddagrab+nvenc', "-y -loglevel error -f lavfi -i ddagrab=output_idx=0:framerate=$($Fps):draw_mouse=1,hwdownload,format=bgra -c:v h264_nvenc -preset p4 -cq 21 -g $Fps -pix_fmt yuv420p $frag"),
  @('gdigrab+x264',  "-y -loglevel error -f gdigrab -framerate $Fps -i desktop -c:v libx264 -preset ultrafast -crf 23 -g $Fps -pix_fmt yuv420p $frag"))
if ($env:PA_RECORD_PATH) { $paths = @($paths | Where-Object { $_[0] -eq $env:PA_RECORD_PATH }) }   # force one path
foreach ($c in $paths) {
  $psi = New-Object Diagnostics.ProcessStartInfo
  $psi.FileName = 'ffmpeg'; $psi.Arguments = $c[1]
  $psi.UseShellExecute = $false; $psi.RedirectStandardInput = $true; $psi.CreateNoWindow = $true
  $p = [Diagnostics.Process]::Start($psi)
  Start-Sleep -Milliseconds 2500
  if (-not $p.HasExited) { $path = $c[0]; break }
}
if (-not $path) { "no capture path worked (ddagrab+qsv, ddagrab+nvenc, gdigrab+x264)"; exit 1 }
"recording ($path) -> $raw (pid $($p.Id)); stop with: touch $StopFlag"
while (-not [IO.File]::Exists($StopFlag) -and -not $p.HasExited) { Start-Sleep -Milliseconds 200 }
Start-Sleep -Seconds $TailSeconds           # keep the frozen stopwatch / final canvas on screen in the footage
if (-not $p.HasExited) { $p.StandardInput.Write('q'); $p.StandardInput.Close(); [void]$p.WaitForExit(30000) }
& ffmpeg -y -loglevel error -i $raw -c copy -movflags +faststart $Out
if ($LASTEXITCODE -eq 0) { Remove-Item -LiteralPath $raw; "saved $Out" } else { "remux failed, raw kept at $raw" }
