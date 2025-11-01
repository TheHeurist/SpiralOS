<#
🌀 SpiralOS Codex Integrity Generator (PowerShell edition)
Computes and injects a SHA-256 hash into docs/codex/CI-Watermark.json.
#>

$Watermark = "docs/codex/CI-Watermark.json"

if (-not (Test-Path $Watermark)) {
    Write-Error "❌  Watermark not found: $Watermark"
    exit 1
}

Write-Host "🔍 Computing integrity hash for $Watermark ..."
$Hash = (Get-FileHash -Algorithm SHA256 $Watermark).Hash.ToLower()

# Read JSON, update integrity.sha256, write back
$json = Get-Content $Watermark -Raw | ConvertFrom-Json
if (-not $json.integrity) { $json | Add-Member -MemberType NoteProperty -Name integrity -Value @{} }
$json.integrity.sha256 = $Hash
$json | ConvertTo-Json -Depth 10 | Set-Content -Encoding UTF8 $Watermark

Write-Host "✅  Updated integrity SHA256: $Hash"
Write-Host "✅  Watermark updated successfully."
exit 0
