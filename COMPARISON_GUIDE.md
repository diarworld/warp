# PROD vs TEST Comparison Guide

This guide explains how to use the enhanced PROD vs TEST comparison functionality in the warp results parser.

## Overview

The comparison feature automatically analyzes performance differences between PROD and TEST environments, detecting regressions and providing actionable insights.

## Quick Start

### 1. Run Comparison Analysis

```bash
# Simple comparison analysis
python run_comparison.py

# Or use the full parser with comparison
python parse_warp_results.py --verbose
```

### 2. View Results

The analysis will show:
- **Comparison Summary**: Quick overview of all operations
- **Regression Detection**: Automatic identification of performance issues
- **Statistical Analysis**: Significance levels and confidence metrics
- **Recommendations**: Actionable insights for detected issues

## Comparison Features

### Automatic Regression Detection

The system automatically detects regressions based on configurable thresholds:

| Metric | Default Threshold | Description |
|--------|------------------|-------------|
| Throughput | -5% | TEST throughput lower than PROD |
| Latency | +10% | TEST latency higher than PROD |
| P99 Latency | +15% | TEST P99 latency higher than PROD |

### Significance Levels

Results are classified by significance level:

- **🔴 HIGH**: Large differences (>20%) or high variability
- **🟡 MEDIUM**: Moderate differences (10-20%) or moderate variability  
- **🟢 LOW**: Small differences (<10%) or low variability

### Status Indicators

- **✅ PASS**: No regressions detected
- **⚠️ REGRESSION**: Performance degradation detected

## Example Output

```
🔍 Warp PROD vs TEST Comparison Analysis
==================================================

📁 Found 25 warp result files
✅ Successfully parsed 25 results
📊 PROD results: 12
🧪 TEST results: 13

🔍 Found 3 operation comparisons

📈 Comparison Summary:
--------------------------------------------------------------------------------
Operation   Throughput      Latency        Status        Significance
--------------------------------------------------------------------------------
GET         +78.2%         -8.7%          ✅ PASS       🟢 LOW
PUT         +27.0%         -6.1%          ✅ PASS       🟡 MEDIUM
MIXED       -12.5%         +15.2%         ⚠️ REGRESSION 🔴 HIGH
--------------------------------------------------------------------------------

⚠️  1 regression(s) detected!
   Check the detailed report for more information.

💡 Quick Recommendations:
   • MIXED: Investigate performance changes
     - Throughput decreased by 12.5%
     - Latency increased by 15.2%

🎯 Analysis complete!
```

## Configuration

### Customize Thresholds

Edit `comparison_config.yaml` to adjust regression detection:

```yaml
regression_thresholds:
  throughput_degradation_percent: 5.0    # 5% throughput degradation
  latency_increase_percent: 10.0         # 10% latency increase
  p99_latency_increase_percent: 15.0     # 15% P99 latency increase
```

### Significance Thresholds

```yaml
significance_thresholds:
  high_significance:
    throughput_diff_percent: 20.0        # 20% difference = HIGH
    combined_cv_threshold: 0.3           # High variability = HIGH
  medium_significance:
    throughput_diff_percent: 10.0        # 10% difference = MEDIUM
    combined_cv_threshold: 0.15          # Moderate variability = MEDIUM
```

## Report Sections

### Executive Summary

Quick overview with status indicators:

| Operation | Throughput Change | Latency Change | Status | Significance |
|-----------|-------------------|----------------|--------|--------------|
| GET | +78.2% | -8.7% | ✅ PASS | 🟢 LOW |
| PUT | +27.0% | -6.1% | ✅ PASS | 🟡 MEDIUM |

### Detected Regressions

Detailed analysis of performance issues:

```
⚠️ Detected Regressions

MIXED:
- Throughput decreased by 12.5%
- Latency increased by 15.2%
- Significance: HIGH
```

### Detailed Comparisons

For each operation, the report includes:

#### Performance Metrics
| Metric | PROD | TEST | Difference |
|--------|------|------|------------|
| Throughput (MiB/s) | 473.72 | 601.43 | +27.0% |
| Latency (ms) | 1147.00 | 1076.85 | -6.1% |

#### Statistical Analysis
- **Significance Level**: MEDIUM
- **PROD Sample Size**: 5 runs
- **TEST Sample Size**: 8 runs
- **PROD Throughput StdDev**: 45.2
- **TEST Throughput StdDev**: 52.1

#### Recommendations
- ✅ **No regressions detected** - Performance is within acceptable limits
- 🟡 **Medium significance** - Monitor for trends

## Use Cases

### 1. Continuous Integration

Add comparison analysis to your CI/CD pipeline:

```bash
# In your CI script
python run_comparison.py
if [ $? -ne 0 ]; then
    echo "Performance regression detected!"
    exit 1
fi
```

### 2. Release Validation

Compare new release against production baseline:

```bash
# Collect baseline results
./collect_warp_results.ps1 --collect

# After deployment, compare
python run_comparison.py
```

### 3. Performance Monitoring

Regular performance checks:

```bash
# Daily performance check
python run_comparison.py > daily_report.md
```

## Troubleshooting

### No Comparisons Available

If you see "No PROD vs TEST comparisons available":

1. **Check Environment Names**: Ensure results are properly tagged as PROD/TEST
2. **Verify Operation Names**: Both environments must have the same operation types
3. **Check File Names**: Results must follow the naming convention

### False Positives

If you get false regression alerts:

1. **Adjust Thresholds**: Modify `comparison_config.yaml`
2. **Increase Sample Size**: More runs provide better statistical confidence
3. **Check Environment Differences**: Ensure fair comparison conditions

### High Variability

If significance levels are consistently HIGH:

1. **Check Test Conditions**: Ensure consistent test environment
2. **Increase Sample Size**: More data points reduce variability
3. **Review Test Parameters**: Check for configuration differences

## Advanced Usage

### Custom Analysis Script

Create custom analysis scripts:

```python
from parse_warp_results import WarpResultsParser

# Load results
parser = WarpResultsParser("./results")
results = parser.find_and_parse_results()

# Run comparison
comparisons = parser.compare_prod_vs_test()

# Custom analysis
for comp in comparisons:
    if comp.throughput_regression:
        print(f"Regression in {comp.operation}: {comp.throughput_diff_percent:.1f}%")
```

### Integration with Monitoring

Send alerts for regressions:

```python
import requests

# Check for regressions
comparisons = parser.compare_prod_vs_test()
regressions = [c for c in comparisons if c.throughput_regression or c.latency_regression]

if regressions:
    # Send alert
    requests.post("https://your-webhook.com", json={
        "regressions": [r.operation for r in regressions]
    })
```

## Best Practices

### 1. Baseline Management
- Maintain stable PROD baselines
- Update baselines after confirmed improvements
- Version control your baseline results

### 2. Test Consistency
- Use identical test parameters across environments
- Ensure consistent hardware/network conditions
- Run tests at similar times to avoid time-based variations

### 3. Sample Size
- Aim for at least 5-10 runs per environment
- More samples provide better statistical confidence
- Consider running longer tests for more stable results

### 4. Threshold Tuning
- Start with conservative thresholds
- Adjust based on your specific requirements
- Document threshold changes and rationale

### 5. Regular Monitoring
- Run comparisons regularly (daily/weekly)
- Track trends over time
- Investigate regressions promptly

## Support

For issues with the comparison functionality:

1. Check the troubleshooting section above
2. Verify your configuration in `comparison_config.yaml`
3. Ensure you have both PROD and TEST results
4. Check the generated report for detailed analysis 