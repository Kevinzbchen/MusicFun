# MusicFun PowerShell Setup Guide

## Quick Start

### Option 1: Run the setup script (Recommended)
```powershell
# Make sure you're in the MusicFun project directory
cd C:\path\to\MusicFun

# Run the setup script
powershell -ExecutionPolicy Bypass -File setup_commands.ps1
```

### Option 2: Copy and paste commands
```powershell
# Run these commands in PowerShell

# 1. Check Python
python --version
if ($LASTEXITCODE -ne 0) { 
    Write-Host "Install Python from https://python.org" -ForegroundColor Red
    exit 1 
}

# 2. Upgrade pip
python -m pip install --upgrade pip

# 3. Install dependencies
python -m pip install -r requirements.txt

# 4. Test installation
python -c "import requests, pandas, pydantic; print('Core packages OK')"

# 5. Test configuration
python scripts/simple_test.py
```

## Complete Setup Commands

### Full Setup with Progress Display
```powershell
# Clear screen
Clear-Host

# Header
Write-Host "=== MusicFun Project Setup ===" -ForegroundColor Cyan
Write-Host ""

# Step 1: Python check
Write-Host "[1/4] Checking Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "  ✗ Python not found" -ForegroundColor Red
    exit 1
}

# Step 2: Pip upgrade
Write-Host "[2/4] Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip 2>&1 | Out-Null
Write-Host "  ✓ pip upgraded" -ForegroundColor Green

# Step 3: Install packages with progress
Write-Host "[3/4] Installing packages..." -ForegroundColor Yellow
$packages = @(
    "requests>=2.31.0",
    "beautifulsoup4>=4.12.2",
    "pandas>=2.1.0",
    "pydantic>=2.4.0",
    "loguru>=0.7.2",
    "aiohttp>=3.9.0",
    "python-dotenv>=1.0.0",
    "pyyaml>=6.0",
    "tenacity>=8.2.0",
    "tqdm>=4.66.0"
)

$i = 0
foreach ($pkg in $packages) {
    $i++
    Write-Host "  [$i/$($packages.Count)] $pkg" -NoNewline -ForegroundColor Gray
    python -m pip install $pkg 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host " - OK" -ForegroundColor Green
    } else {
        Write-Host " - Failed" -ForegroundColor Red
    }
}
Write-Host "  ✓ Packages installed" -ForegroundColor Green

# Step 4: Verify and test
Write-Host "[4/4] Verifying setup..." -ForegroundColor Yellow
python scripts/simple_test.py 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Setup verified" -ForegroundColor Green
} else {
    Write-Host "  ⚠ Setup completed with warnings" -ForegroundColor Yellow
}

# Final message
Write-Host ""
Write-Host "=== Setup Complete! ===" -ForegroundColor Green
Write-Host ""
Write-Host "Next: Configure your .env file" -ForegroundColor Cyan
Write-Host "Copy-Item .env.example .env" -ForegroundColor White
Write-Host ""
```

## One-Line Setup Commands

### Minimal setup
```powershell
python -m pip install -r requirements.txt && python scripts/simple_test.py
```

### Setup with checks
```powershell
python --version && python -m pip install --upgrade pip && python -m pip install -r requirements.txt && python scripts/simple_test.py
```

## Available Setup Scripts

| Script | Description | Usage |
|--------|-------------|-------|
| `setup_commands.ps1` | Complete setup with progress | `powershell -File setup_commands.ps1` |
| `scripts/setup.ps1` | Detailed setup with colors | `powershell -File scripts/setup.ps1` |
| `scripts/quick_setup.ps1` | Quick setup | `powershell -File scripts/quick_setup.ps1` |

## Post-Setup Configuration

### 1. Create environment file
```powershell
# Copy the example file
Copy-Item .env.example .env

# Or create manually
if (-not (Test-Path .env)) {
    @"
# MusicFun Configuration
DEBUG=false
LOG_LEVEL=INFO
NETEASE_COOKIES=
NETEASE_PROXY=
DATABASE_URL=sqlite:///data/music.db
"@ | Out-File .env -Encoding UTF8
}
```

### 2. Edit .env file
Open `.env` in your editor and configure:
- `NETEASE_COOKIES`: Your Netease Music cookies (required)
- Other settings as needed

### 3. Test the setup
```powershell
# Test configuration
python scripts/simple_test.py

# Test imports
python -c "import requests, pandas, pydantic, loguru, aiohttp; print('All imports OK')"
```

## Troubleshooting Commands

### Check installation
```powershell
# List installed packages
python -m pip list | Select-String -Pattern "requests|pandas|pydantic|loguru"

# Check specific package
python -c "import requests; print(f'requests {requests.__version__}')"
python -c "import pandas; print(f'pandas {pandas.__version__}')"
```

### Fix common issues
```powershell
# Permission error - use user install
python -m pip install --user -r requirements.txt

# SSL error
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12

# Encoding error
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001
```

### Reinstall packages
```powershell
# Reinstall all packages
python -m pip install --upgrade --force-reinstall -r requirements.txt

# Reinstall specific package
python -m pip install --upgrade --force-reinstall requests pandas pydantic
```

## Development Setup

### Install development dependencies
```powershell
python -m pip install -r requirements-dev.txt
```

### Run tests
```powershell
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_config.py -v
```

### Code formatting
```powershell
# Format code with black
python -m black src/

# Sort imports
python -m isort src/

# Check code style
python -m flake8 src/
```

## Project Verification

### Check project structure
```powershell
# List files
get-childitem -Recurse -File | Select-Object -First 20 Name

# Check key files
Test-Path requirements.txt
Test-Path config/settings.py
Test-Path scripts/simple_test.py
Test-Path .env.example
```

### Run all verification
```powershell
# Verification script
$checks = @(
    @{Name="Python"; Command="python --version"},
    @{Name="pip"; Command="python -m pip --version"},
    @{Name="requests"; Command="python -c 'import requests'"},
    @{Name="pandas"; Command="python -c 'import pandas'"},
    @{Name="pydantic"; Command="python -c 'import pydantic'"},
    @{Name="config"; Command="python scripts/simple_test.py"}
)

foreach ($check in $checks) {
    Write-Host "Checking $($check.Name)..." -NoNewline -ForegroundColor Yellow
    Invoke-Expression $check.Command 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host " ✓" -ForegroundColor Green
    } else {
        Write-Host " ✗" -ForegroundColor Red
    }
}
```

## Quick Reference Table

| Task | Command |
|------|---------|
| Check Python | `python --version` |
| Upgrade pip | `python -m pip install --upgrade pip` |
| Install deps | `python -m pip install -r requirements.txt` |
| Test setup | `python scripts/simple_test.py` |
| Create .env | `Copy-Item .env.example .env` |
| List packages | `python -m pip list` |
| Test import | `python -c "import requests; print('OK')"` |
| Dev setup | `python -m pip install -r requirements-dev.txt` |

## Notes

1. **Run as Administrator** if you encounter permission errors
2. **Internet connection** is required for package installation
3. **Python 3.8+** is required
4. **.env file** must be configured before running crawlers
5. **Check logs** in `logs/` directory for runtime issues

## Support

If setup fails:
1. Check error messages
2. Verify Python installation
3. Check internet connection
4. Try individual package installation
5. Consult project README.md

Example of installing key packages individually:
```powershell
python -m pip install requests
python -m pip install pandas
python -m pip install pydantic
python -m pip install loguru
python -m pip install aiohttp
```
