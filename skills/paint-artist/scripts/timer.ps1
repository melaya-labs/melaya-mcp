# Always-on-top, never-activating stopwatch for screen recordings of a run.
# Starts when -StartFlag appears (or at launch when no StartFlag is given), freezes (green, "Done") when -StopFlag appears.
# Paths may be Windows (C:\...) or Git Bash (/c/...) style; they are tested literally (no wildcards).
# Usage: powershell -NoProfile -ExecutionPolicy Bypass -STA -File timer.ps1 -StartFlag C:\tmp\t.start -StopFlag C:\tmp\t.stop `
#        -Title 'Melaya Computer Control' -Subtitle 'Mona Lisa | one call' -X 1290 -Y 420
param([string]$StopFlag, [string]$StartFlag, [string]$Title = 'Melaya Computer Control',
      [string]$Subtitle = 'one call', [int]$X = 1290, [int]$Y = 420)

function Norm([string]$p) {
  if (-not $p) { return $p }
  if ($p -match '^/([a-zA-Z])/(.*)$') { $p = $Matches[1] + ':\' + ($Matches[2] -replace '/', '\') }
  return [IO.Path]::GetFullPath($p)
}
$StopFlag = Norm $StopFlag; $StartFlag = Norm $StartFlag
if ($StopFlag -and [IO.File]::Exists($StopFlag)) { [IO.File]::Delete($StopFlag) }   # a stale stop flag would block the start

Add-Type -AssemblyName System.Windows.Forms, System.Drawing
Add-Type -ReferencedAssemblies System.Windows.Forms -TypeDefinition @"
using System; using System.Windows.Forms;
public class NoActivateForm : Form {
  protected override bool ShowWithoutActivation { get { return true; } }
  protected override CreateParams CreateParams { get { var p = base.CreateParams; p.ExStyle |= 0x08000000 | 0x00000008; return p; } }
}
"@ 2>$null
$f = New-Object NoActivateForm
$f.FormBorderStyle = 'None'; $f.TopMost = $true; $f.StartPosition = 'Manual'; $f.ShowInTaskbar = $false
$f.Location = New-Object Drawing.Point($X, $Y); $f.Size = New-Object Drawing.Size(420, 170)
$f.BackColor = [Drawing.Color]::FromArgb(11, 14, 40)
$t1 = New-Object Windows.Forms.Label; $t1.Text = $Title; $t1.ForeColor = [Drawing.Color]::FromArgb(140, 160, 255)
$t1.Font = New-Object Drawing.Font('Segoe UI Semibold', 13); $t1.AutoSize = $false; $t1.Size = New-Object Drawing.Size(400, 28); $t1.Location = New-Object Drawing.Point(14, 10)
$t2 = New-Object Windows.Forms.Label; $t2.Text = $Subtitle; $t2.ForeColor = [Drawing.Color]::FromArgb(190, 195, 215)
$t2.Font = New-Object Drawing.Font('Segoe UI', 10); $t2.AutoSize = $false; $t2.Size = New-Object Drawing.Size(400, 22); $t2.Location = New-Object Drawing.Point(14, 38)
$clock = New-Object Windows.Forms.Label; $clock.Text = '00:00.0'; $clock.ForeColor = [Drawing.Color]::White
$clock.Font = New-Object Drawing.Font('Consolas', 48, [Drawing.FontStyle]::Bold); $clock.AutoSize = $false
$clock.Size = New-Object Drawing.Size(400, 90); $clock.Location = New-Object Drawing.Point(10, 66); $clock.TextAlign = 'MiddleLeft'
$f.Controls.AddRange(@($t1, $t2, $clock))

$script:sw = New-Object Diagnostics.Stopwatch
$script:done = $false
if (-not $StartFlag) { $script:sw.Start() }
$tm = New-Object Windows.Forms.Timer; $tm.Interval = 50
$tm.Add_Tick({
  if ($script:done) { return }
  if (-not $script:sw.IsRunning -and $StartFlag -and [IO.File]::Exists($StartFlag)) { $script:sw.Start() }
  if ($script:sw.IsRunning -and $StopFlag -and [IO.File]::Exists($StopFlag)) {
    $script:sw.Stop(); $script:done = $true
    $clock.ForeColor = [Drawing.Color]::FromArgb(90, 230, 150); $t2.Text = "Done  |  $Subtitle"
  }
  $e = $script:sw.Elapsed
  $clock.Text = ('{0:00}:{1:00}.{2}' -f [int][math]::Floor($e.TotalMinutes), $e.Seconds, [int][math]::Floor($e.Milliseconds / 100))
})
$tm.Start()
[Windows.Forms.Application]::Run($f)
