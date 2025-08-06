# Warp Results Collection and Analysis Script (PowerShell)
# This script collects warp results from all containers and generates a comparison report

param(
    [string]$Action = "all",
    [string]$ResultsDir = "./warp_results",
    [string]$Namespace = "timesheet",
    [switch]$Verbose
)

# Configuration
$WARP_POD_PREFIX = "warp-"
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path

# Function to print colored output
function Write-Status {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Function to check if kubectl is available
function Test-Kubectl {
    try {
        $null = Get-Command kubectl -ErrorAction Stop
        $null = kubectl cluster-info 2>$null
        return $true
    }
    catch {
        Write-Error "kubectl is not installed or cannot connect to cluster"
        return $false
    }
}

# Function to check if Python is available
function Test-Python {
    try {
        $null = Get-Command python3 -ErrorAction Stop
        return $true
    }
    catch {
        try {
            $null = Get-Command python -ErrorAction Stop
            return $true
        }
        catch {
            Write-Error "Python is not installed or not in PATH"
            return $false
        }
    }
}

# Function to get warp pod names
function Get-WarpPods {
    Write-Status "Getting warp pod names..."
    try {
        $pods = kubectl get pods -n $Namespace --no-headers -o custom-columns=":metadata.name" 2>$null | Where-Object { $_ -match "^$WARP_POD_PREFIX" }
        if (-not $pods) {
            Write-Error "No warp pods found in namespace $Namespace"
            return $null
        }
        return $pods
    }
    catch {
        Write-Error "Failed to get warp pods"
        return $null
    }
}

# Function to collect results from a single pod
function Collect-FromPod {
    param([string]$PodName)
    
    Write-Status "Collecting results from pod: $PodName"
    
    # Create directory for this pod's results
    $podResultsDir = Join-Path $ResultsDir $PodName
    New-Item -ItemType Directory -Path $podResultsDir -Force | Out-Null
    
    # Find all warp result files in the pod
    try {
        $resultFiles = kubectl exec -n $Namespace $PodName -- find / -name "warp-*.json.zst" 2>$null
    }
    catch {
        Write-Warning "No warp result files found in pod $PodName"
        return
    }
    
    if (-not $resultFiles) {
        Write-Warning "No warp result files found in pod $PodName"
        return
    }
    
    # Copy each result file
    $fileCount = 0
    foreach ($file in $resultFiles) {
        if ($file) {
            $filename = Split-Path $file -Leaf
            Write-Status "  Copying: $filename"
            try {
                kubectl cp "$Namespace/$PodName`:$file" "$podResultsDir/$filename" 2>$null
                $fileCount++
            }
            catch {
                Write-Warning "Failed to copy $filename from $PodName"
            }
        }
    }
    
    Write-Success "Collected $fileCount files from $PodName"
}

# Function to collect all results
function Collect-AllResults {
    Write-Status "Starting warp results collection..."
    
    # Create results directory
    New-Item -ItemType Directory -Path $ResultsDir -Force | Out-Null
    
    # Get all warp pods
    $pods = Get-WarpPods
    if (-not $pods) {
        return
    }
    
    Write-Status "Found warp pods:"
    foreach ($pod in $pods) {
        Write-Host "  - $pod"
    }
    
    # Collect from each pod
    $totalFiles = 0
    foreach ($pod in $pods) {
        Collect-FromPod $pod
        $podFileCount = (Get-ChildItem -Path (Join-Path $ResultsDir $pod) -Name "*.json.zst" -ErrorAction SilentlyContinue).Count
        $totalFiles += $podFileCount
    }
    
    Write-Success "Collection complete. Total files collected: $totalFiles"
}

# Function to run the parser
function Invoke-Parser {
    Write-Status "Running warp results parser..."
    
    $parserScript = Join-Path $SCRIPT_DIR "parse_warp_results.py"
    if (-not (Test-Path $parserScript)) {
        Write-Error "Parser script not found: $parserScript"
        return $false
    }
    
    # Run the parser
    Push-Location $SCRIPT_DIR
    try {
        $pythonCmd = if (Get-Command python3 -ErrorAction SilentlyContinue) { "python3" } else { "python" }
        $args = @("parse_warp_results.py", "--results-dir", $ResultsDir, "--output", "warp_comparison_report.md")
        if ($Verbose) {
            $args += "--verbose"
        }
        
        & $pythonCmd $args
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Report generated: warp_comparison_report.md"
            return $true
        }
        else {
            Write-Error "Failed to generate report"
            return $false
        }
    }
    finally {
        Pop-Location
    }
}

# Function to show usage
function Show-Usage {
    Write-Host "Usage: $($MyInvocation.MyCommand.Name) [OPTIONS]"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Action {collect|parse|all}    Action to perform (default: all)"
    Write-Host "  -ResultsDir PATH              Results directory (default: ./warp_results)"
    Write-Host "  -Namespace NAME               Kubernetes namespace (default: timesheet)"
    Write-Host "  -Verbose                      Verbose output"
    Write-Host "  -Help                         Show this help message"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  $($MyInvocation.MyCommand.Name)                    # Collect and parse all results"
    Write-Host "  $($MyInvocation.MyCommand.Name) -Action collect    # Only collect results"
    Write-Host "  $($MyInvocation.MyCommand.Name) -Action parse      # Only parse existing results"
    Write-Host "  $($MyInvocation.MyCommand.Name) -ResultsDir C:\results # Use custom results directory"
}

# Main function
function Main {
    # Handle help parameter
    if ($args -contains "-Help" -or $args -contains "-h") {
        Show-Usage
        return
    }
    
    Write-Status "Configuration:"
    Write-Host "  Namespace: $Namespace"
    Write-Host "  Results directory: $ResultsDir"
    Write-Host "  Action: $Action"
    Write-Host ""
    
    # Check prerequisites
    if (-not (Test-Kubectl)) {
        exit 1
    }
    
    if (-not (Test-Python)) {
        exit 1
    }
    
    # Execute requested action
    switch ($Action.ToLower()) {
        "collect" {
            Collect-AllResults
        }
        "parse" {
            if (-not (Test-Path $ResultsDir)) {
                Write-Error "Results directory not found: $ResultsDir"
                Write-Error "Run with -Action collect first to gather results"
                exit 1
            }
            Invoke-Parser
        }
        "all" {
            Collect-AllResults
            Invoke-Parser
        }
        default {
            Write-Error "Invalid action: $Action. Use collect, parse, or all"
            Show-Usage
            exit 1
        }
    }
    
    Write-Success "Script completed successfully!"
}

# Run main function
Main 