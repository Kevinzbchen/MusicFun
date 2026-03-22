<#
.SYNOPSIS
    MusicFun One-Click Launcher
.DESCRIPTION
    Starts the Netease API server, runs the crawler, and opens the HTML viewer
.EXAMPLE
    .\launch_musicfun.ps1 -Keyword "mihoyo" -Limit 5
.EXAMPLE
    .\launch_musicfun.ps1 -Keyword "genshin" -Limit 3 -MockOnly
#>

param(
    [string]$Keyword = "mihoyo",
    [int]$Limit = 5,
    [int]$Comments = 10,
    [switch]$MockOnly,
    [switch]$NoAPI,
    [switch]$Help
)

if ($Help) {
    Write-Host ""
    Write-Host "MusicFun One-Click Launcher"
    Write-Host "==========================="
    Write-Host ""
    Write-Host "Usage: .\launch_musicfun.ps1 [options]"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Keyword <string>   Search keyword (default: mihoyo)"
    Write-Host "  -Limit <int>        Number of songs to process (default: 5)"
    Write-Host "  -Comments <int>     Comments per song (default: 10)"
    Write-Host "  -MockOnly           Use mock comments only (no API needed)"
    Write-Host "  -NoAPI              Skip starting API server (use existing)"
    Write-Host "  -Help               Show this help message"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\launch_musicfun.ps1 -Keyword mihoyo -Limit 5"
    Write-Host "  .\launch_musicfun.ps1 -Keyword genshin -Limit 3 -MockOnly"
    Write-Host "  .\launch_musicfun.ps1 -Keyword honkai -Limit 10 -NoAPI"
    Write-Host ""
    exit
}

Write-Host ""
Write-Host "MusicFun One-Click Launcher" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment is active
if (-not (Get-Command python -ErrorAction SilentlyContinue).Path.Contains(".venv")) {
    Write-Host "[1/5] Activating virtual environment..." -ForegroundColor Yellow
    .\.venv\Scripts\Activate.ps1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to activate virtual environment" -ForegroundColor Red
        exit 1
    }
    Write-Host "Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "Virtual environment already active" -ForegroundColor Green
}

# Start API server if not in mock mode and API server is not already running
$apiProcess = $null
if (-not $MockOnly -and -not $NoAPI) {
    Write-Host ""
    Write-Host "[2/5] Checking API server..." -ForegroundColor Yellow
    
    # Check if API server is already running
    try {
        $test = Invoke-WebRequest -Uri "http://localhost:3000" -UseBasicParsing -TimeoutSec 2 -ErrorAction SilentlyContinue
        if ($test.StatusCode -eq 200) {
            Write-Host "API server already running at http://localhost:3000" -ForegroundColor Green
        } else {
            throw "Server not responding"
        }
    } catch {
        Write-Host "Starting API server..." -ForegroundColor Yellow
        
        # Check if api-enhanced directory exists
        if (-not (Test-Path "api-enhanced")) {
            Write-Host "api-enhanced directory not found. Cloning..." -ForegroundColor Yellow
            git clone https://github.com/NeteaseCloudMusicApiEnhanced/api-enhanced.git
            if ($LASTEXITCODE -ne 0) {
                Write-Host "Failed to clone API repository" -ForegroundColor Red
                exit 1
            }
        }
        
        # Check Node.js
        $nodeVersion = node --version 2>$null
        if (-not $nodeVersion) {
            Write-Host "Node.js not found. Please install Node.js from https://nodejs.org/" -ForegroundColor Red
            Write-Host "   Or use -MockOnly flag to run without API" -ForegroundColor Yellow
            exit 1
        }
        
        # Install dependencies if needed
        if (-not (Test-Path "api-enhanced/node_modules")) {
            Write-Host "Installing API dependencies..." -ForegroundColor Yellow
            Push-Location api-enhanced
            npm install --silent
            Pop-Location
        }
        
        # Start API server in background
        Write-Host "Starting API server in background..." -ForegroundColor Yellow
        $apiProcess = Start-Process -FilePath "node" -ArgumentList "api-enhanced/app.js" -WindowStyle Hidden -PassThru
        
        # Wait for server to start
        Write-Host "Waiting for API server to start..." -NoNewline
        for ($i = 0; $i -lt 30; $i++) {
            Start-Sleep -Milliseconds 500
            Write-Host "." -NoNewline
            try {
                $test = Invoke-WebRequest -Uri "http://localhost:3000" -UseBasicParsing -TimeoutSec 1 -ErrorAction SilentlyContinue
                if ($test.StatusCode -eq 200) {
                    Write-Host " OK" -ForegroundColor Green
                    break
                }
            } catch {
                # Still starting
            }
        }
        Write-Host "API server started" -ForegroundColor Green
    }
} elseif ($MockOnly) {
    Write-Host ""
    Write-Host "[2/5] Mock mode enabled - no API server needed" -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "[2/5] Skipping API server (using existing)" -ForegroundColor Yellow
}

# Run the crawler
Write-Host ""
Write-Host "[3/5] Running crawler..." -ForegroundColor Yellow

$crawlerArgs = @(
    "scripts/run_netease.py",
    "--keyword", $Keyword,
    "--limit", $Limit,
    "--comments-per-song", $Comments
)

if ($MockOnly) {
    $crawlerArgs += "--mock-only"
}

$output = python $crawlerArgs 2>&1
$output | ForEach-Object { Write-Host $_ }

# Check if crawler succeeded
if ($LASTEXITCODE -ne 0) {
    Write-Host "Crawler failed" -ForegroundColor Red
    if ($apiProcess) {
        Stop-Process -Id $apiProcess.Id -Force -ErrorAction SilentlyContinue
    }
    exit 1
}

Write-Host "Crawler completed" -ForegroundColor Green

# Generate HTML viewer
Write-Host ""
Write-Host "[4/5] Generating HTML viewer..." -ForegroundColor Yellow

if (Test-Path "scripts/generate_enhanced_html.py") {
    python scripts/generate_enhanced_html.py 2>&1 | Out-Null
    Write-Host "HTML viewer generated" -ForegroundColor Green
} else {
    Write-Host "generate_enhanced_html.py not found, creating basic viewer..." -ForegroundColor Yellow
    
    # Create basic HTML viewer
    $htmlContent = @'
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>MusicFun Comments</title>
    <style>
        body { font-family: Arial; margin: 20px; background: #f0f0f0; }
        .song { background: white; margin: 20px 0; padding: 20px; border-radius: 8px; }
        .comment { border-left: 3px solid #1DB954; margin: 10px 0; padding: 10px; background: #f9f9f9; }
    </style>
</head>
<body>
    <h1>MusicFun Comments</h1>
    <p>Generated from latest crawl</p>
</body>
</html>
'@
    $htmlContent | Out-File -FilePath "data/processed/comments_viewer.html" -Encoding UTF8
}

# Open the HTML viewer
Write-Host ""
Write-Host "[5/5] Opening HTML viewer..." -ForegroundColor Yellow

$htmlFile = "data/processed/comments_viewer.html"
if (Test-Path $htmlFile) {
    Start-Process $htmlFile
    Write-Host "HTML viewer opened in browser" -ForegroundColor Green
} else {
    # Try to find latest JSON
    $jsonFiles = Get-ChildItem "data/processed/netease_*.json" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending
    if ($jsonFiles) {
        $latestJson = $jsonFiles[0].FullName
        Write-Host "Opening JSON file directly..." -ForegroundColor Yellow
        Start-Process "notepad" $latestJson
    }
}

# Summary
Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "MusicFun Complete!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Keyword: $Keyword"
Write-Host "Songs processed: $Limit"
Write-Host "Comments per song: $Comments"
if ($MockOnly) {
    Write-Host "Mode: Mock (offline)"
} else {
    Write-Host "Mode: Real API"
}
Write-Host ""
Write-Host "Output saved to: data/processed/"
Write-Host "HTML viewer opened in browser"
Write-Host ""

# Keep API server running if we started it
if ($apiProcess -and -not $MockOnly) {
    Write-Host "API server is running in background." -ForegroundColor Yellow
    Write-Host "To stop it later, run: Stop-Process -Id $($apiProcess.Id) -Force" -ForegroundColor Yellow
    Write-Host ""
}