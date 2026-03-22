# MusicFun Project Setup Guide for Windows PowerShell

## Quick Setup Commands

Copy and paste these commands into PowerShell (run as Administrator if needed):

### 1. Basic Setup (Recommended)

```powershell
# Run the quick setup script
.\scripts\quick_setup.ps1
```

### 2. Manual Setup Commands

If you prefer to run commands manually, use this sequence:

```powershell
# Clear screen and show header
Clear-Host
Write-Host "=== MusicFun Setup ===" -ForegroundColor Cyan

# 1. Check Python
Write-Host "[1/5] Checking Python..." -ForegroundColor Yellow
python --version
if ($LASTEXITCODE -ne 0) { 
    Write-Host "Python not found! Install from https://python.org" -ForegroundColor Red
    exit 1 
}
Write-Host "✓ Python OK" -ForegroundColor Green

# 2. Check and upgrade pip
Write-Host "[2/5] Checking pip..." -ForegroundColor Yellow
python -m pip --version
if ($LASTEXITCODE -ne 0) { 
    Write-Host "Installing pip..." -ForegroundColor Yellow
    python -m ensurepip --upgrade
}
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip
Write-Host "✓ pip OK" -ForegroundColor Green

# 3. Install dependencies with progress
Write-Host "[3/5] Installing dependencies..." -ForegroundColor Yellow
$packages = Get-Content requirements.txt | Where-Object { $_ -notmatch '^\s*#' -and $_.Trim() -ne '' }
$total = $packages.Count
$current = 0

foreach ($pkg in $packages) {
    $current++
    $percent = [math]::Round(($current / $total) * 100)
    Write-Progress -Activity "Installing Packages" -Status "$current/$total: $pkg" -PercentComplete $percent
    
    Write-Host "[$current/$total] $pkg" -NoNewline -ForegroundColor Gray
    python -m pip install $pkg 2>&1 | Out-Null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host " - ✓" -ForegroundColor Green
    } else {
        Write-Host " - ✗" -ForegroundColor Red
    }
}
Write-Progress -Activity "Installing Packages" -Completed
Write-Host "✓ Dependencies installed" -ForegroundColor Green

# 4. Verify key packages
Write-Host "[4/5] Verifying packages..." -ForegroundColor Yellow
$tests = @(
    "python -c 'import requests; print(\"✓ requests\")' 2>&1",
    "python -c 'import pandas; print(\"✓ pandas\")' 2>&1",
    "python -c 'import pydantic; print(\"✓ pydantic\")' 2>&1",
    "python -c 'import loguru; print(\"✓ loguru\")' 2>&1",
    "python -c 'import bs4; print(\"✓ beautifulsoup4\")' 2>&1"
)

foreach ($test in $tests) {
    Invoke-Expression $test
}
Write-Host "✓ Packages verified" -ForegroundColor Green

# 5. Test configuration
Write-Host "[5/5] Testing configuration..." -ForegroundColor Yellow
if (Test-Path "scripts/simple_test.py") {
    python scripts/simple_test.py
    Write-Host "✓ Configuration test complete" -ForegroundColor Green
}

Write-Host "\n=== Setup Complete! ===" -ForegroundColor Green
Write-Host "Next: Copy .env.example to .env and configure your settings" -ForegroundColor Cyan
```

### 3. One-Liner Setup

For a quick one-command setup (less verbose):

```powershell
# One-liner setup
Clear-Host; Write-Host "Setting up MusicFun..." -ForegroundColor Cyan; python --version; python -m pip install --upgrade pip; python -m pip install -r requirements.txt; if (Test-Path "scripts/simple_test.py") { python scripts/simple_test.py }; Write-Host "\nDone!" -ForegroundColor Green
```

## Setup Scripts

We provide two setup scripts:

### `scripts/setup.ps1` - Full setup with detailed output
```powershell
# Run with detailed output
.\scripts\setup.ps1

# Run with verbose output
.\scripts\setup.ps1 -Verbose
```

**Features:**
- Color-coded output
- Progress bars for installation
- Detailed error reporting
- Package verification
- Configuration testing

### `scripts/quick_setup.ps1` - Quick setup with basic output
```powershell
# Quick setup
.\scripts\quick_setup.ps1
```

**Features:**
- Minimal output
- Progress indicators
- Basic verification
- Fast execution

## Post-Setup Steps

After running the setup, complete these steps:

### 1. Configure Environment
```powershell
# Copy environment template
Copy-Item .env.example .env

# Edit .env file (use your preferred editor)
notepad .env
# or
code .env
```

### 2. Configure .env File
Edit `.env` and set at minimum:
```env
# Required for Netease Music
NETEASE_COOKIES=your_cookies_here

# Optional but recommended
DEBUG=false
LOG_LEVEL=INFO
```

### 3. Test the Setup
```powershell
# Run configuration test
python scripts/simple_test.py

# Run the original test (if needed)
python scripts/test_config.py
```

### 4. Install Development Dependencies (Optional)
```powershell
# For development work
python -m pip install -r requirements-dev.txt
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Python not found
```powershell
# Check if Python is in PATH
Get-Command python

# If not found, add Python to PATH or reinstall with "Add Python to PATH" checked
```

#### 2. Permission errors
```powershell
# Run PowerShell as Administrator
# Or use user install flag
python -m pip install --user -r requirements.txt
```

#### 3. Specific package installation fails
```powershell
# Try installing individually
python -m pip install requests
python -m pip install pandas

# Or upgrade pip first
python -m pip install --upgrade pip setuptools wheel
```

#### 4. Unicode/Encoding errors
```powershell
# Set console encoding
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001
```

#### 5. SSL certificate errors
```powershell
# Temporary fix (not recommended for production)
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12

# Or set environment variable
$env:PYTHONHTTPSVERIFY = "0"
```

## Verification Commands

After setup, verify everything works:

```powershell
# Check Python and packages
python --version
python -m pip list | Select-String -Pattern "requests|pandas|pydantic|loguru"

# Test imports
python -c "import requests, pandas, pydantic, loguru; print('All imports OK')"

# Test configuration
python scripts/simple_test.py
```

## Project Structure Verification

```powershell
# Check project structure
tree /F /A

# Expected structure:
# MusicFun/
# │   .env.example
# │   .gitignore
# │   pyproject.toml
# │   README.md
# │   requirements.txt
# │   setup.py
# ├── config/
# ├── data/
# ├── logs/
# ├── scripts/
# └── src/
```

## Running the Setup Scripts

### Execution Policy
If you get execution policy errors:

```powershell
# Check current policy
Get-ExecutionPolicy

# Set policy for current session (temporary)
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

# Then run the script
.\scripts\setup.ps1
```

### Alternative: Run commands directly
If scripts are blocked, copy the commands from `quick_setup.ps1` and run them manually.

## Quick Reference

| Command | Purpose |
|---------|---------|
| `python --version` | Check Python installation |
| `python -m pip --version` | Check pip installation |
| `python -m pip install -r requirements.txt` | Install all dependencies |
| `python scripts/simple_test.py` | Test project configuration |
| `Copy-Item .env.example .env` | Create environment file |
| `python -m pip install --upgrade pip` | Upgrade pip to latest |

## Support

If you encounter issues:
1. Check the error messages
2. Verify Python and pip are correctly installed
3. Check internet connection
4. Try running individual package installations
5. Consult the project README.md for more details
