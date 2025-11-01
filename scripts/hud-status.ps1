<#
🌀 SpiralOS HUD Provenance Updater
Checks CI-Watermark integrity and updates HUD indicator status.
#>

$Watermark = "docs/codex/CI-Watermark.json"
$HUD = "docs/hud/hud.json"

if (!(Test-Path $Watermark)) { Write-Error "❌ CI-Watermark not found"; exit 1 }
if (!(Test-Path $HUD)) { Write-Error "❌ HUD config not found"; exit 1 }

# Read both files
$wm = Get-Content $Watermark -Raw | ConvertFrom-Json
$hud = Get-Content $HUD -Raw | ConvertFrom-Json

# Compute current hash to verify match
$currentHash = (Get-FileHash -Algorithm SHA256 $Watermark).Hash.ToLower()
# Refresh stored hash after any Codex reseal drift
$wm = Get-Content $Watermark -Raw | ConvertFrom-Json
$storedHash  = $wm.integrity.sha256.ToLower()

if ($currentHash -eq $storedHash) {
    Write-Host "✅ CI Provenance verified. Integrity intact."
    $hud.provenance.status = "verified"
    $hud.provenance.integrityHash = $storedHash
    $hud.provenance.lastCheck = (Get-Date).ToString("s")
    $hud.verificationIndicator.state = "active"
    $hud.verificationIndicator.updated = (Get-Date).ToString("s")
} else {
    Write-Warning "⚠️ CI Provenance mismatch detected."
    $hud.provenance.status = "invalid"
    $hud.provenance.integrityHash = $currentHash
    $hud.provenance.lastCheck = (Get-Date).ToString("s")
    $hud.verificationIndicator.state = "error"
    $hud.verificationIndicator.updated = (Get-Date).ToString("s")
}

## Write updated HUD file (cross-version safe)
#$hudJson = $hud | ConvertTo-Json -Depth 10
#[IO.File]::WriteAllText($HUD, $hudJson, [Text.Encoding]::UTF8)
#
#Write-Host "🌀 HUD updated with current CI verification status."

# Write updated HUD file – legacy-compatible
$hudJson = $hud | ConvertTo-Json -Depth 10
Set-Content -Path "docs/hud/hud.json" -Value $hudJson
Write-Host "🌀 HUD updated with current CI verification status."
