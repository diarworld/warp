# Warp Benchmark Results Parser

This repository contains scripts to collect and analyze warp benchmark results from Kubernetes pods and generate comprehensive comparison reports.

## Overview

The warp tool generates performance benchmark results for S3-compatible storage systems. This project provides tools to:

1. **Collect results** from all warp containers in a Kubernetes cluster
2. **Parse and analyze** the compressed JSON result files
3. **Generate comprehensive reports** comparing performance across different job types and environments
4. **Compare PROD vs TEST** results with regression detection and statistical analysis

## Files

- `parse_warp_results.py` - Python script to parse warp result files and generate reports
- `collect_warp_results.sh` - Shell script to collect results from Kubernetes pods
- `collect_warp_results.ps1` - PowerShell script for Windows users
- `run_comparison.py` - Simple script to run PROD vs TEST comparison analysis
- `comparison_config.yaml` - Configuration file for regression thresholds and settings
- `warp.yaml` - Kubernetes deployment for warp tool
- `Jobs.yaml` - Kubernetes jobs for different benchmark scenarios
- `results.md` - Example results file

## Prerequisites

- Python 3.6+
- kubectl configured to access your Kubernetes cluster
- Bash shell (for the collection script)

## Installation

1. Clone or download the scripts to your local machine
2. Make the shell script executable:
   ```bash
   chmod +x collect_warp_results.sh
   ```

## Usage

### Quick Start

To collect all results and generate a report in one command:

```bash
./collect_warp_results.sh
```

This will:
1. Find all warp pods in the `timesheet` namespace
2. Collect all `.json.zst` result files from each pod
3. Parse the results and generate a comprehensive report

### Step by Step

#### 1. Collect Results Only

```bash
./collect_warp_results.sh --collect
```

This will collect all warp result files from the pods but not parse them.

#### 2. Parse Existing Results

If you already have result files:

```bash
./collect_warp_results.sh --parse
```

Or run the Python parser directly:

```bash
python3 parse_warp_results.py --results-dir ./warp_results --output my_report.md
```

### Advanced Usage

#### Custom Namespace

```bash
./collect_warp_results.sh --namespace my-namespace
```

#### Custom Results Directory

```bash
./collect_warp_results.sh --dir /path/to/results
```

#### Verbose Output

```bash
python3 parse_warp_results.py --verbose
```

## Output

The scripts generate:

1. **Collected Results**: `./warp_results/` directory containing all result files organized by pod
2. **Comparison Report**: `warp_comparison_report.md` with detailed analysis

### Report Contents

The generated report includes:

- **Executive Summary**: PROD vs TEST comparison with regression detection
- **Summary Table**: Overview of all job types and their performance metrics
- **PROD vs TEST Comparisons**: Detailed analysis for each operation type
- **Detailed Statistics**: For each job type:
  - Mean, min, max, and standard deviation for throughput and latency
  - Individual results from each container
  - Client throughput distribution
- **Performance Metrics**:
  - Throughput (MiB/s and objects/s)
  - Latency (average, P50, P90, P99)
  - Time to First Byte (TTFB) when available
- **Regression Analysis**: Automatic detection of performance regressions
- **Recommendations**: Actionable insights based on analysis results

## File Structure

After running the collection script, you'll have:

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

## Job Types

The parser recognizes different job types based on the warp operation:

- **GET**: Read operations
- **PUT**: Write operations  
- **MIXED**: Mixed read/write operations
- **DELETE**: Delete operations
- **STAT**: Stat operations

Each job type is analyzed separately for both PROD and TEST environments.

## PROD vs TEST Comparison

The enhanced parser automatically compares PROD and TEST results for the same operations:

### Regression Detection
- **Throughput Regression**: Detected when TEST throughput is >5% lower than PROD
- **Latency Regression**: Detected when TEST latency is >10% higher than PROD
- **Significance Levels**: HIGH, MEDIUM, LOW based on statistical analysis

### Comparison Features
- **Statistical Analysis**: Coefficient of variation and significance testing
- **Performance Metrics**: Side-by-side comparison of throughput and latency
- **Recommendations**: Actionable insights for detected regressions
- **Executive Summary**: Quick overview with status indicators

### Configuration
Regression thresholds and analysis settings can be customized in `comparison_config.yaml`:
- Throughput degradation threshold (default: 5%)
- Latency increase threshold (default: 10%)
- Significance level thresholds
- Report configuration options

## Troubleshooting

### Common Issues

1. **No warp pods found**
   - Check that warp is deployed in the correct namespace
   - Verify kubectl can access the cluster

2. **No result files found**
   - Ensure warp jobs have completed successfully
   - Check that results are saved in `/tmp` directory in pods

3. **Permission errors**
   - Ensure kubectl has proper permissions to exec into pods
   - Check file permissions on the local machine

### Debug Mode

Run with verbose output to see detailed information:

```bash
./collect_warp_results.sh --verbose
python3 parse_warp_results.py --verbose
```

## Customization

### Adding New Job Types

To support new warp operations, modify the `parse_filename` method in `parse_warp_results.py`.

### Custom Metrics

To extract additional metrics, extend the `WarpResult` dataclass and `extract_metrics_from_report` method.

### Report Format

The report format can be customized by modifying the `generate_report` method in the `WarpResultsParser` class.

## Example Output

```
# Warp Benchmark Results Comparison Report

Generated: 2025-01-27 10:30:15
Total results parsed: 25

## Summary

| Job Type | Environment | Results Count | Avg Throughput (MiB/s) | Avg Latency (ms) |
|----------|-------------|---------------|------------------------|------------------|
| GET_PROD | PROD | 8 | 42.26 | 96.9 |
| GET_TEST | TEST | 8 | 150.60 | 24.2 |
| PUT_PROD | PROD | 5 | 473.72 | 1147.0 |
| PUT_TEST | TEST | 4 | 633.05 | 1105.5 |
```

## Contributing

Feel free to submit issues and enhancement requests! 