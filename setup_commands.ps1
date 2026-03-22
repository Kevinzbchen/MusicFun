<#
MusicFun Setup Commands

Run these commands in PowerShell to set up the project.
Copy and paste each section or run the entire file.
#>

# ========== SECTION 1: BASIC CHECKS ==========
Write-Host "=== MusicFun Setup ===" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "[1/5] Checking Python..." -ForegroundColor Yellow
$pythonCheck = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Python: $pythonCheck" -ForegroundColor Green
} else {
    Write-Host "  ✗ Python not found" -ForegroundColor Red
    Write-Host "  Download from: https://python.org" -ForegroundColor Yellow
    exit 1
}

# Check pip
Write-Host "[2/5] Checking pip..." -ForegroundColor Yellow
$pipCheck = python -m pip --version 2>&1
if ($LASTEXITCODE -eq 0) {
    $pipVersion = ($pipCheck -split ' ')[1]
    Write-Host "  ✓ pip: $pipVersion" -ForegroundColor Green
} else {
    Write-Host "  Installing pip..." -ForegroundColor Yellow
    python -m ensurepip --upgrade 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ pip installed" -ForegroundColor Green
    } else {
        Write-Host "  ✗ pip installation failed" -ForegroundColor Red
        exit 1
    }
}

# ========== SECTION 2: INSTALL DEPENDENCIES ==========
Write-Host "[3/5] Installing dependencies..." -ForegroundColor Yellow

if (-not (Test-Path "requirements.txt")) {
    Write-Host "  ✗ requirements.txt not found" -ForegroundColor Red
    exit 1
}

# Read packages
$packages = Get-Content requirements.txt | Where-Object { 
    $_ -notmatch '^\s*#' -and $_.Trim() -ne '' 
}

$total = $packages.Count
$current = 0

foreach ($pkg in $packages) {
    $current++
    $percent = [math]::Round(($current / $total) * 100)
    
    Write-Progress -Activity "Installing Packages" `
        -Status "Package $current of $total" `
        -PercentComplete $percent `
        -CurrentOperation $pkg
    
    Write-Host "  [$current/$total] $pkg" -NoNewline -ForegroundColor Gray
    
    # Install package
    python -m pip install $pkg 2>&1 | Out-Null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host " - OK" -ForegroundColor Green
    } else {
        Write-Host " - FAILED" -ForegroundColor Red
    }
}

Write-Progress -Activity "Installing Packages" -Completed
Write-Host "  ✓ All packages installed" -ForegroundColor Green

# ========== SECTION 3: VERIFY INSTALLATION ==========
Write-Host "[4/5] Verifying installation..." -ForegroundColor Yellow

# Test key imports
$importTests = @(
    @{Name="requests"; Code="import requests; print('OK')"},
    @{Name="pandas"; Code="import pandas; print('OK')"},
    @{Name="pydantic"; Code="import pydantic; print('OK')"},
    @{Name="loguru"; Code="import loguru; print('OK')"},
    @{Name="beautifulsoup4"; Code="import bs4; print('OK')"}
)

$successCount = 0
foreach ($test in $importTests) {
    Write-Host "  - $($test.Name): " -NoNewline -ForegroundColor Gray
    
    $output = python -c $test.Code 2>&1
    if ($LASTEXITCODE -eq 0 -and $output -eq "OK") {
        Write-Host "OK" -ForegroundColor Green
        $successCount++
    } else {
        Write-Host "FAILED" -ForegroundColor Red
    }
}

Write-Host "  ✓ $successCount/$($importTests.Count) packages verified" -ForegroundColor Green

# ========== SECTION 4: TEST CONFIGURATION ==========
Write-Host "[5/5] Testing configuration..." -ForegroundColor Yellow

if (Test-Path "scripts/simple_test.py") {
    Write-Host "  Running configuration test..." -ForegroundColor Gray
    python scripts/simple_test.py 2>&1 | Out-Null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Configuration test passed" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ Configuration test had issues" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ⚠ Test script not found" -ForegroundColor Yellow
}

# ========== SECTION 5: FINAL MESSAGE ==========
Write-Host ""
Write-Host "=== Setup Complete! ===" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Create environment file:" -ForegroundColor Yellow
Write-Host "   Copy-Item .env.example .env" -ForegroundColor White
Write-Host ""
Write-Host "2. Configure .env file:" -ForegroundColor Yellow
Write-Host "   - Set NETEASE_COOKIES (required for Netease Music)" -ForegroundColor White
Write-Host "   - Adjust other settings as needed" -ForegroundColor White
Write-Host ""
Write-Host "3. Test the project:" -ForegroundColor Yellow
Write-Host "   python scripts/simple_test.py" -ForegroundColor White
Write-Host ""
Write-Host "Optional development setup:" -ForegroundColor Cyan
Write-Host "   python -m pip install -r requirements-dev.txt" -ForegroundColor White
Write-Host ""
