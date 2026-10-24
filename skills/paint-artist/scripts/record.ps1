# Screen recorder for a run: ffmpeg gdigrab of the whole desktop, stopped GRACEFULLY ('q' on stdin) when -StopFlag
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
$psi = New-Object Diagnostics.ProcessStartInfo
$psi.FileName = 'ffmpeg'
# -g = 1 s keyframe interval: short fragments, so even an unexpected crash loses at most ~1 s
$psi.Arguments = "-y -loglevel error -f gdigrab -framerate $Fps -i desktop -c:v libx264 -preset ultrafast -crf 23 -g $Fps -pix_fmt yuv420p -movflags +frag_keyframe+empty_moov `"$raw`""
$psi.UseShellExecute = $false; $psi.RedirectStandardInput = $true; $psi.CreateNoWindow = $true
$p = [Diagnostics.Process]::Start($psi)
"recording -> $raw (pid $($p.Id)); stop with: touch $StopFlag"
while (-not [IO.File]::Exists($StopFlag) -and -not $p.HasExited) { Start-Sleep -Milliseconds 200 }
Start-Sleep -Seconds $TailSeconds           # keep the frozen stopwatch / final canvas on screen in the footage
if (-not $p.HasExited) { $p.StandardInput.Write('q'); $p.StandardInput.Close(); [void]$p.WaitForExit(30000) }
& ffmpeg -y -loglevel error -i $raw -c copy -movflags +faststart $Out
if ($LASTEXITCODE -eq 0) { Remove-Item -LiteralPath $raw; "saved $Out" } else { "remux failed, raw kept at $raw" }
