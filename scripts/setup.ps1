<#
MusicFun Project Setup Script for Windows PowerShell

This script sets up the MusicFun project environment by:
1. Checking Python installation
2. Checking pip availability
3. Installing dependencies from requirements.txt
4. Verifying key packages are installed

Usage:
    .\setup.ps1 [-Verbose]

Note: Run PowerShell as Administrator if you encounter permission issues.
#>

param(
    [switch]$Verbose
)

# Set error handling
$ErrorActionPreference = "Stop"

# ANSI color codes for better output
$ColorReset = "`e[0m"
$ColorGreen = "`e[32m"
$ColorYellow = "`e[33m"
$ColorRed = "`e[31m"
$ColorBlue = "`e[34m"
$ColorCyan = "`e[36m"
$ColorMagenta = "`e[35m"

# Function to print colored output
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White",
        [switch]$NoNewLine
    )
    
    $colorCode = switch ($Color) {
        "Green" { $ColorGreen }
        "Yellow" { $ColorYellow }
        "Red" { $ColorRed }
        "Blue" { $ColorBlue }
        "Cyan" { $ColorCyan }
        "Magenta" { $ColorMagenta }
        default { "" }
    }
    
    if ($NoNewLine) {
        Write-Host "${colorCode}${Message}${ColorReset}" -NoNewline
    } else {
        Write-Host "${colorCode}${Message}${ColorReset}"
    }
}

# Function to print section header
function Write-SectionHeader {
    param([string]$Title)
    
    Write-ColorOutput "`n================================================================================" -Color Cyan
    Write-ColorOutput "  $Title" -Color Cyan
    Write-ColorOutput "================================================================================" -Color Cyan
}

# Function to print step
function Write-Step {
    param([string]$Step, [int]$Number)
    
    Write-ColorOutput "`n[Step $Number] $Step" -Color Blue
}

# Function to check if a command exists
function Test-CommandExists {
    param([string]$Command)
    
    try {
        $null = Get-Command $Command -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

# Function to get Python version
function Get-PythonVersion {
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            return $pythonVersion
        }
        return $null
    } catch {
        return $null
    }
}

# Function to get pip version
function Get-PipVersion {
    try {
        $pipVersion = python -m pip --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            return $pipVersion
        }
        return $null
    } catch {
        return $null
    }
}

# Function to install dependencies with progress
function Install-Dependencies {
    param([string]$RequirementsFile)
    
    if (-not (Test-Path $RequirementsFile)) {
        Write-ColorOutput "ERROR: Requirements file not found: $RequirementsFile" -Color Red
        return $false
    }
    
    Write-ColorOutput "Installing dependencies from: $RequirementsFile" -Color Yellow
    
    # Read requirements file
    $requirements = Get-Content $RequirementsFile | Where-Object { $_ -notmatch '^\s*#' -and $_.Trim() -ne '' }
    $totalPackages = $requirements.Count
    
    Write-ColorOutput "Found $totalPackages packages to install" -Color Cyan
    
    # Create progress bar
    $currentPackage = 0
    
    foreach ($requirement in $requirements) {
        $currentPackage++
        $percentComplete = [math]::Round(($currentPackage / $totalPackages) * 100, 1)
        
        Write-Progress -Activity "Installing Dependencies" -Status "Installing: $requirement" `
            -PercentComplete $percentComplete -CurrentOperation "Package $currentPackage of $totalPackages"
        
        Write-ColorOutput "[$currentPackage/$totalPackages] Installing: $requirement" -Color Yellow -NoNewLine
        
        try {
            # Install package
            $output = python -m pip install $requirement 2>&1
            
            if ($LASTEXITCODE -eq 0) {
                Write-ColorOutput " - SUCCESS" -Color Green
                if ($Verbose) {
                    Write-ColorOutput "  Output: $($output | Select-String -Pattern 'Successfully|Requirement already') | Select-Object -First 1)" -Color Cyan
                }
            } else {
                Write-ColorOutput " - FAILED" -Color Red
                Write-ColorOutput "  Error: $output" -Color Red
                return $false
            }
            
        } catch {
            Write-ColorOutput " - ERROR" -Color Red
            Write-ColorOutput "  Exception: $_" -Color Red
            return $false
        }
    }
    
    Write-Progress -Activity "Installing Dependencies" -Completed
    return $true
}

# Function to verify key packages
function Verify-KeyPackages {
    $keyPackages = @(
        @{Name="requests"; TestCommand="python -c 'import requests; print(f\"requests {requests.__version__}\")'"},
        @{Name="pandas"; TestCommand="python -c 'import pandas; print(f\"pandas {pandas.__version__}\")'"},
        @{Name="pydantic"; TestCommand="python -c 'import pydantic; print(f\"pydantic {pydantic.__version__}\")'"},
        @{Name="loguru"; TestCommand="python -c 'import loguru; print(\"loguru OK\")'"},
        @{Name="beautifulsoup4"; TestCommand="python -c 'import bs4; print(f\"beautifulsoup4 {bs4.__version__}\")'"},
        @{Name="aiohttp"; TestCommand="python -c 'import aiohttp; print(f\"aiohttp {aiohttp.__version__}\")'"},
        @{Name="tenacity"; TestCommand="python -c 'import tenacity; print(\"tenacity OK\")'"},
        @{Name="tqdm"; TestCommand="python -c 'import tqdm; print(f\"tqdm {tqdm.__version__}\")'"}
    )
    
    Write-ColorOutput "`nVerifying key packages:" -Color Cyan
    
    $successCount = 0
    $failedPackages = @()
    
    foreach ($package in $keyPackages) {
        Write-Host "  - $($package.Name): " -NoNewline
        
        try {
            $output = Invoke-Expression $package.TestCommand 2>&1
            
            if ($LASTEXITCODE -eq 0) {
                Write-ColorOutput "INSTALLED ($output)" -Color Green
                $successCount++
            } else {
                Write-ColorOutput "MISSING" -Color Red
                $failedPackages += $package.Name
            }
        } catch {
            Write-ColorOutput "ERROR" -Color Red
            $failedPackages += $package.Name
        }
    }
    
    return @{
        SuccessCount = $successCount
        TotalCount = $keyPackages.Count
        FailedPackages = $failedPackages
    }
}

# Main execution
Clear-Host
Write-ColorOutput "==============================================================" -Color Magenta
Write-ColorOutput "          MusicFun Project Setup Script" -Color Magenta
Write-ColorOutput "==============================================================" -Color Magenta
Write-ColorOutput "Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -Color Cyan
Write-ColorOutput "Working Directory: $(Get-Location)" -Color Cyan

# Step 1: Check Python installation
Write-SectionHeader "STEP 1: CHECKING PYTHON INSTALLATION"

if (Test-CommandExists "python") {
    $pythonVersion = Get-PythonVersion
    if ($pythonVersion) {
        Write-ColorOutput "✓ Python found: $pythonVersion" -Color Green
    } else {
        Write-ColorOutput "✗ Python found but version check failed" -Color Red
        exit 1
    }
} else {
    Write-ColorOutput "✗ Python not found in PATH" -Color Red
    Write-ColorOutput "Please install Python 3.8 or higher from https://python.org" -Color Yellow
    exit 1
}

# Step 2: Check pip availability
Write-SectionHeader "STEP 2: CHECKING PIP AVAILABILITY"

$pipVersion = Get-PipVersion
if ($pipVersion) {
    Write-ColorOutput "✓ pip found: $($pipVersion.Split(' ')[1])" -Color Green
} else {
    Write-ColorOutput "✗ pip not found or not working" -Color Red
    Write-ColorOutput "Attempting to install/upgrade pip..." -Color Yellow
    
    try {
        python -m ensurepip --upgrade 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "✓ pip installed/upgraded successfully" -Color Green
        } else {
            Write-ColorOutput "✗ Failed to install pip" -Color Red
            exit 1
        }
    } catch {
        Write-ColorOutput "✗ Error installing pip: $_" -Color Red
        exit 1
    }
}

# Step 3: Upgrade pip
Write-SectionHeader "STEP 3: UPGRADING PIP"

Write-ColorOutput "Upgrading pip to latest version..." -Color Yellow

try {
    $upgradeOutput = python -m pip install --upgrade pip 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-ColorOutput "✓ pip upgraded successfully" -Color Green
        if ($Verbose) {
            Write-ColorOutput "Output: $($upgradeOutput | Select-String -Pattern 'Successfully')" -Color Cyan
        }
    } else {
        Write-ColorOutput "⚠ pip upgrade failed (continuing anyway)" -Color Yellow
        if ($Verbose) {
            Write-ColorOutput "Error: $upgradeOutput" -Color Red
        }
    }
} catch {
    Write-ColorOutput "⚠ pip upgrade error (continuing anyway): $_" -Color Yellow
}

# Step 4: Install dependencies
Write-SectionHeader "STEP 4: INSTALLING DEPENDENCIES"

$requirementsFile = "requirements.txt"
if (Test-Path $requirementsFile) {
    $success = Install-Dependencies -RequirementsFile $requirementsFile
    if (-not $success) {
        Write-ColorOutput "✗ Failed to install some dependencies" -Color Red
        exit 1
    }
    Write-ColorOutput "✓ All dependencies installed successfully" -Color Green
} else {
    Write-ColorOutput "✗ Requirements file not found: $requirementsFile" -Color Red
    exit 1
}

# Step 5: Verify key packages
Write-SectionHeader "STEP 5: VERIFYING KEY PACKAGES"

$verificationResult = Verify-KeyPackages

Write-ColorOutput "`nVerification Summary:" -Color Cyan
Write-ColorOutput "  Successfully verified: $($verificationResult.SuccessCount)/$($verificationResult.TotalCount) packages" -Color Green

if ($verificationResult.FailedPackages.Count -gt 0) {
    Write-ColorOutput "  Failed packages: $($verificationResult.FailedPackages -join ', ')" -Color Red
    
    # Try to install failed packages individually
    Write-ColorOutput "`nAttempting to install failed packages individually..." -Color Yellow
    
    foreach ($package in $verificationResult.FailedPackages) {
        Write-ColorOutput "  Installing $package..." -Color Yellow -NoNewLine
        
        try {
            $output = python -m pip install $package 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-ColorOutput " SUCCESS" -Color Green
            } else {
                Write-ColorOutput " FAILED" -Color Red
            }
        } catch {
            Write-ColorOutput " ERROR" -Color Red
        }
    }
}

# Step 6: Test configuration
Write-SectionHeader "STEP 6: TESTING PROJECT CONFIGURATION"

if (Test-Path "scripts/simple_test.py") {
    Write-ColorOutput "Running configuration test..." -Color Yellow
    
    try {
        $testOutput = python scripts/simple_test.py 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "✓ Configuration test passed" -Color Green
            if ($Verbose) {
                Write-ColorOutput "Test output:" -Color Cyan
                $testOutput | ForEach-Object { Write-Host "  $_" }
            }
        } else {
            Write-ColorOutput "⚠ Configuration test completed with warnings" -Color Yellow
            Write-ColorOutput "Output: $testOutput" -Color Yellow
        }
    } catch {
        Write-ColorOutput "⚠ Configuration test error: $_" -Color Yellow
    }
} else {
    Write-ColorOutput "⚠ Configuration test script not found" -Color Yellow
}

# Final summary
Write-SectionHeader "SETUP COMPLETE"

Write-ColorOutput "✓ MusicFun project setup completed successfully!" -Color Green
Write-ColorOutput "`nNext steps:" -Color Cyan
Write-ColorOutput "1. Copy .env.example to .env and configure your settings" -Color Yellow
Write-ColorOutput "   Copy-Item .env.example .env" -Color White
Write-ColorOutput "2. Edit .env file and set your configuration (especially NETEASE_COOKIES)" -Color Yellow
Write-ColorOutput "3. Run the project test: python scripts/simple_test.py" -Color Yellow
Write-ColorOutput "4. Start developing your crawler!" -Color Yellow
Write-ColorOutput "`nFor development, you can also install dev dependencies:" -Color Cyan
Write-ColorOutput "   pip install -r requirements-dev.txt" -Color White

Write-ColorOutput "`nSetup completed at: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -Color Cyan
Write-ColorOutput "==============================================================" -Color Magenta
