<#
  Expert-profile launcher for the local assistant.
    D:\dockerData\assistant\assistant.ps1              # list profiles + show which is running
    D:\dockerData\assistant\assistant.ps1 marketing    # load the 'marketing' expert
    D:\dockerData\assistant\assistant.ps1 -Stop        # stop the assistant
  A profile = base model + knowledge base + persona + GPU/context tuning (see profiles.json).
  One model runs at a time on http://127.0.0.1:8082 (alias "assistant").
#>
param([string]$Profile, [switch]$Stop, [switch]$List)

$ErrorActionPreference = 'Stop'
$root    = 'D:\dockerData\assistant'
$compose = 'D:\dockerData\config\compose.assistant.yaml'
$cfg     = (Get-Content "$root\profiles.json" -Raw | ConvertFrom-Json).profiles
$names   = ($cfg.PSObject.Properties.Name | Sort-Object)

function Show-State {
    $running = (docker ps --filter name=^assistant$ --format '{{.Status}}')
    $active  = if (Test-Path "$root\.active-profile") { Get-Content "$root\.active-profile" -Raw } else { '(none)' }
    "Profiles: $($names -join ', ')"
    "Active profile: $($active.Trim())   Container: $(if ($running) { $running } else { 'stopped' })"
}

if ($List -or (-not $Profile -and -not $Stop)) { Show-State; return }

# Free port 8082: stop any other model container from earlier compose files.
foreach ($c in 'qwen35-4b-assistant','qwen35-4b-llama-gpu','k2-horizon-37b-llama-gpu','k2-horizon-llama-gpu') {
    if (docker ps -q -f "name=^$c$") { docker stop $c | Out-Null }
}

if ($Stop) {
    docker compose -f $compose down | Out-Null
    'Assistant stopped.'; return
}

if ($Profile -notin $names) { throw "Unknown profile '$Profile'. Available: $($names -join ', ')" }
$p = $cfg.$Profile
$modelPath = Join-Path 'D:\dockerData\models' $p.model
if (-not (Test-Path $modelPath)) { throw "Model file not found: $modelPath" }

# 1. Persona = profile role + shared base persona -> ui-config.json (the web UI's default system message).
$base = (Get-Content "$root\persona.md" -Raw)
$sys  = ($p.role + "`n`n" + $base).Trim()
[IO.File]::WriteAllText("$root\ui-config.json", (@{ systemMessage = $sys } | ConvertTo-Json -Compress), (New-Object Text.UTF8Encoding $false))

# 2. Pre-select the knowledge base so the expert starts pointed at the right docs.
$kbActive = "$root\kb\.active"
if ($p.kb) { [IO.File]::WriteAllText($kbActive, $p.kb, (New-Object Text.UTF8Encoding $false)) }
elseif (Test-Path $kbActive) { Remove-Item $kbActive }

# 3. Launch the generic compose with this profile's model/tuning.
$env:ASSISTANT_MODEL = $p.model
$env:ASSISTANT_ALIAS = 'assistant'
$env:ASSISTANT_NGL   = [string]$p.ngl
$env:ASSISTANT_CTX   = [string]$p.ctx
docker compose -f $compose up -d --force-recreate | Out-Null
[IO.File]::WriteAllText("$root\.active-profile", $Profile, (New-Object Text.UTF8Encoding $false))

# 4. Wait for health.
$t0 = Get-Date
do {
    Start-Sleep 8
    $ok = try { (Invoke-WebRequest http://127.0.0.1:8082/health -UseBasicParsing -TimeoutSec 5).StatusCode -eq 200 } catch { $false }
    $st = docker inspect -f '{{.State.Status}} {{.State.ExitCode}}' assistant 2>$null
} until ($ok -or $st -notmatch '^running' -or ((Get-Date) - $t0).TotalMinutes -gt 10)

if ($ok) {
    "Loaded '$Profile'  ($($p.model), ngl=$($p.ngl), ctx=$($p.ctx), kb=$(if ($p.kb) { $p.kb } else { 'none' }))"
    "Ready at http://127.0.0.1:8082  after $([int]((Get-Date)-$t0).TotalSeconds)s"
} else {
    "Failed to start (state: $st). Last log lines:"
    docker logs --tail 8 assistant 2>&1
}
