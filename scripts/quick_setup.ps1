<#
MusicFun Quick Setup - PowerShell Commands

Run these commands in PowerShell to set up the MusicFun project.
#>

# Clear screen and show header
Clear-Host
Write-Host "==============================================================" -ForegroundColor Magenta
Write-Host "          MusicFun Project Quick Setup" -ForegroundColor Magenta
Write-Host "==============================================================" -ForegroundColor Magenta
Write-Host ""

# Step 1: Check Python
Write-Host "[1/6] Checking Python installation..." -ForegroundColor Cyan
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Python found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "  ✗ Python not found or not in PATH" -ForegroundColor Red
    Write-Host "  Please install Python 3.8+ from https://python.org" -ForegroundColor Yellow
    exit 1
}

# Step 2: Check pip
Write-Host "[2/6] Checking pip..." -ForegroundColor Cyan
$pipVersion = python -m pip --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ pip found: $($pipVersion.Split(' ')[1])" -ForegroundColor Green
} else {
    Write-Host "  ✗ pip not found, installing..." -ForegroundColor Yellow
    python -m ensurepip --upgrade 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ pip installed successfully" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Failed to install pip" -ForegroundColor Red
        exit 1
    }
}

# Step 3: Upgrade pip
Write-Host "[3/6] Upgrading pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ pip upgraded" -ForegroundColor Green
} else {
    Write-Host "  ⚠ pip upgrade failed (continuing)" -ForegroundColor Yellow
}

# Step 4: Install dependencies
Write-Host "[4/6] Installing dependencies..." -ForegroundColor Cyan
if (Test-Path "requirements.txt") {
    $packages = Get-Content requirements.txt | Where-Object { $_ -notmatch '^\s*#' -and $_.Trim() -ne '' }
    $total = $packages.Count
    $current = 0
    
    foreach ($pkg in $packages) {
        $current++
        $percent = [math]::Round(($current / $total) * 100)
        Write-Progress -Activity "Installing Dependencies" -Status "Installing: $pkg" -PercentComplete $percent
        
        Write-Host "  [$current/$total] $pkg" -NoNewline -ForegroundColor Gray
        python -m pip install $pkg 2>&1 | Out-Null
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host " - ✓" -ForegroundColor Green
        } else {
            Write-Host " - ✗" -ForegroundColor Red
        }
    }
    Write-Progress -Activity "Installing Dependencies" -Completed
    Write-Host "  ✓ All dependencies installed" -ForegroundColor Green
} else {
    Write-Host "  ✗ requirements.txt not found" -ForegroundColor Red
    exit 1
}

# Step 5: Verify key packages
Write-Host "[5/6] Verifying key packages..." -ForegroundColor Cyan
$keyPackages = @(
    @{Name="requests"; Test="python -c 'import requests; print(\"requests OK\")' 2>&1"},
    @{Name="pandas"; Test="python -c 'import pandas; print(\"pandas OK\")' 2>&1"},
    @{Name="pydantic"; Test="python -c 'import pydantic; print(\"pydantic OK\")' 2>&1"},
    @{Name="loguru"; Test="python -c 'import loguru; print(\"loguru OK\")' 2>&1"},
    @{Name="beautifulsoup4"; Test="python -c 'import bs4; print(\"beautifulsoup4 OK\")' 2>&1"}
)

$successCount = 0
foreach ($pkg in $keyPackages) {
    Write-Host "  - $($pkg.Name): " -NoNewline -ForegroundColor Gray
    $result = Invoke-Expression $pkg.Test
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓" -ForegroundColor Green
        $successCount++
    } else {
        Write-Host "✗" -ForegroundColor Red
    }
}
Write-Host "  ✓ $successCount/$($keyPackages.Count) key packages verified" -ForegroundColor Green

# Step 6: Test configuration
Write-Host "[6/6] Testing configuration..." -ForegroundColor Cyan
if (Test-Path "scripts/simple_test.py") {
    $testResult = python scripts/simple_test.py 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Configuration test passed" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ Configuration test warnings" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ⚠ Test script not found" -ForegroundColor Yellow
}

# Final message
Write-Host ""
Write-Host "==============================================================" -ForegroundColor Magenta
Write-Host "          SETUP COMPLETE!" -ForegroundColor Green
Write-Host "==============================================================" -ForegroundColor Magenta
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Copy .env.example to .env" -ForegroundColor Yellow
Write-Host "   Copy-Item .env.example .env" -ForegroundColor White
Write-Host "2. Edit .env and configure your settings" -ForegroundColor Yellow
Write-Host "3. Test the project: python scripts/simple_test.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "Optional: Install dev dependencies" -ForegroundColor Cyan
Write-Host "   pip install -r requirements-dev.txt" -ForegroundColor White
Write-Host ""
