# Warp Results Parser Usage Guide

This guide explains how to use the warp results parsing scripts to collect and analyze benchmark results from your Kubernetes cluster.

## Quick Start

### For Windows Users (PowerShell)

1. **Collect and analyze all results:**
   ```powershell
   .\collect_warp_results.ps1
   ```

2. **Collect results only:**
   ```powershell
   .\collect_warp_results.ps1 -Action collect
   ```

3. **Parse existing results:**
   ```powershell
   .\collect_warp_results.ps1 -Action parse
   ```

### For Linux/Mac Users (Bash)

1. **Make the script executable:**
   ```bash
   chmod +x collect_warp_results.sh
   ```

2. **Collect and analyze all results:**
   ```bash
   ./collect_warp_results.sh
   ```

3. **Collect results only:**
   ```bash
   ./collect_warp_results.sh --collect
   ```

4. **Parse existing results:**
   ```bash
   ./collect_warp_results.sh --parse
   ```

## Prerequisites

Before running the scripts, ensure you have:

1. **kubectl** configured and connected to your Kubernetes cluster
2. **Python 3.6+** installed
3. **Warp pods** running in your cluster (deployed using `warp.yaml`)
4. **Warp jobs** completed (deployed using `Jobs.yaml`)

## Step-by-Step Process

### 1. Deploy Warp Infrastructure

First, deploy the warp infrastructure to your cluster:

```bash
# Deploy warp StatefulSet
kubectl apply -f warp.yaml

# Deploy warp jobs
kubectl apply -f Jobs.yaml
```

### 2. Wait for Jobs to Complete

Monitor the jobs until they complete:

```bash
kubectl get jobs -n timesheet
kubectl logs -f job/warp-write-prod -n timesheet
```

### 3. Collect Results

Run the collection script to gather all result files:

```bash
# Windows
.\collect_warp_results.ps1 -Action collect

# Linux/Mac
./collect_warp_results.sh --collect
```

This will:
- Find all warp pods in the `timesheet` namespace
- Copy all `.json.zst` result files from each pod
- Organize files by pod in the `./warp_results/` directory

### 4. Generate Analysis Report

Parse the collected results and generate a comprehensive report:

```bash
# Windows
.\collect_warp_results.ps1 -Action parse

# Linux/Mac
./collect_warp_results.sh --parse
```

Or run both steps at once:

```bash
# Windows
.\collect_warp_results.ps1

# Linux/Mac
./collect_warp_results.sh
```

## Output Files

After running the scripts, you'll have:

### 1. Collected Results Directory
```
warp_results/
├── warp-0/
│   ├── warp-get-2025-08-05[213436]-e5bywi.json.zst
│   ├── warp-put-2025-08-05[210837]-9YXefe.json.zst
│   └── ...
├── warp-1/
│   ├── warp-get-2025-08-05[213757]-8F7a1D.json.zst
│   └── ...
└── ...
```

### 2. Analysis Report
- `warp_comparison_report.md` - Comprehensive comparison report

## Report Contents

The generated report includes:

### Summary Table
- Overview of all job types and their performance metrics
- Average throughput and latency across all runs

### Detailed Analysis by Job Type
For each job type (GET_PROD, GET_TEST, PUT_PROD, PUT_TEST, etc.):

1. **Statistics**
   - Mean, min, max, and standard deviation for throughput and latency
   - Total number of runs

2. **Individual Results**
   - Detailed metrics for each individual run
   - Throughput (MiB/s and objects/s)
   - Latency (average, P50, P90, P99)

3. **Client Distribution**
   - Average throughput per client across all runs
   - Shows load distribution across containers

## Advanced Usage

### Custom Namespace

If your warp pods are in a different namespace:

```bash
# Windows
.\collect_warp_results.ps1 -Namespace my-namespace

# Linux/Mac
./collect_warp_results.sh --namespace my-namespace
```

### Custom Results Directory

Specify a custom directory for results:

```bash
# Windows
.\collect_warp_results.ps1 -ResultsDir C:\my-results

# Linux/Mac
./collect_warp_results.sh --dir /path/to/results
```

### Verbose Output

Get detailed information about the process:

```bash
# Windows
.\collect_warp_results.ps1 -Verbose

# Linux/Mac
./collect_warp_results.sh --verbose
```

### Manual Python Parser

You can also run the Python parser directly:

```bash
python parse_warp_results.py --results-dir ./warp_results --output my_report.md --verbose
```

## Troubleshooting

### Common Issues

1. **"No warp pods found"**
   - Check that warp is deployed: `kubectl get pods -n timesheet`
   - Verify namespace: `kubectl get namespaces`

2. **"No result files found"**
   - Ensure warp jobs completed successfully
   - Check job logs: `kubectl logs job/warp-write-prod -n timesheet`

3. **"kubectl not found"**
   - Install kubectl and configure cluster access
   - Test connection: `kubectl cluster-info`

4. **"Python not found"**
   - Install Python 3.6 or later
   - Verify installation: `python --version`

### Debug Mode

For troubleshooting, run with verbose output:

```bash
# Windows
.\collect_warp_results.ps1 -Verbose

# Linux/Mac
./collect_warp_results.sh --verbose
```

### Manual File Collection

If the automatic collection fails, you can manually copy files:

```bash
# List files in a pod
kubectl exec -n timesheet warp-0 -- find /tmp -name "*.json.zst"

# Copy a specific file
kubectl cp timesheet/warp-0:/tmp/warp-get-2025-08-05[213436]-e5bywi.json.zst ./local-file.json.zst
```

## Example Workflow

Here's a complete example workflow:

```bash
# 1. Deploy infrastructure
kubectl apply -f warp.yaml
kubectl apply -f Jobs.yaml

# 2. Wait for jobs to complete
kubectl get jobs -n timesheet -w

# 3. Collect and analyze results
./collect_warp_results.sh --verbose

# 4. View the report
cat warp_comparison_report.md
```

## File Structure

Your project should look like this:

```
warp/
├── warp.yaml                    # Kubernetes StatefulSet
├── Jobs.yaml                    # Kubernetes Jobs
├── parse_warp_results.py        # Python parser script
├── collect_warp_results.sh      # Bash collection script
├── collect_warp_results.ps1     # PowerShell collection script
├── test_parser.py              # Test script for results.md
├── README.md                   # Project documentation
├── USAGE.md                    # This usage guide
├── results.md                  # Example results file
├── warp_results/               # Collected results (generated)
│   ├── warp-0/
│   ├── warp-1/
│   └── ...
└── warp_comparison_report.md   # Generated report
```

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Run with verbose output to get more details
3. Verify your Kubernetes cluster and kubectl configuration
4. Ensure warp jobs completed successfully before collecting results 