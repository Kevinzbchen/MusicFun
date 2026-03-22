$filePath = 'scripts/run_netease.py'
$content = Get-Content -Path $filePath -Raw
# Write back without BOM
[System.IO.File]::WriteAllText($filePath, $content, [System.Text.UTF8Encoding]::new($false))
Write-Host 'File rewritten without BOM' -ForegroundColor Green
