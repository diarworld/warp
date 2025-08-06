# Warp Benchmark Results Comparison Report

Generated: 2025-08-07 01:58:22
Total results parsed: 7

## Executive Summary

### PROD vs TEST Comparison Summary

| Operation | Throughput Change | Latency Change | Status |
|-----------|-------------------|----------------|--------|
| GET | +78.2% | -8.7% | ✅ PASS |
| PUT | +27.0% | -6.1% | ✅ PASS |

## Detailed Results Summary

| Job Type | Environment | Results Count | Avg Throughput (MiB/s) | Avg Latency (ms) |
|----------|-------------|---------------|------------------------|------------------|
| PUT_PROD | PROD | 1 | 473.72 | 1147.00 |
| PUT_TEST | TEST | 2 | 601.43 | 1076.85 |
| GET_PROD | PROD | 1 | 42.26 | 96.90 |
| GET_TEST | TEST | 2 | 75.33 | 88.50 |
| MIXED_TEST | TEST | 1 | 858.38 | 25.90 |

## PROD vs TEST Detailed Comparisons

### GET Operation Comparison

#### Performance Metrics

| Metric | PROD | TEST | Difference |
|--------|------|------|------------|
| Throughput (MiB/s) | 42.26 | 75.33 | +78.2% |
| Latency (ms) | 96.90 | 88.50 | -8.7% |

#### Recommendations

- ✅ **No regressions detected** - Performance is within acceptable limits

### PUT Operation Comparison

#### Performance Metrics

| Metric | PROD | TEST | Difference |
|--------|------|------|------------|
| Throughput (MiB/s) | 473.72 | 601.43 | +27.0% |
| Latency (ms) | 1147.00 | 1076.85 | -6.1% |

#### Recommendations

- ✅ **No regressions detected** - Performance is within acceptable limits

## PUT_PROD Results

### Statistics

- **Total runs**: 1
- **Throughput (MiB/s)**: Mean=473.72, Min=473.72, Max=473.72
- **Average Latency (ms)**: Mean=1147.00, Min=1147.00, Max=1147.00

### Individual Results

| Job Type | Throughput (MiB/s) | Throughput (obj/s) | Avg Latency (ms) | P99 Latency (ms) |
|----------|-------------------|-------------------|-----------------|-----------------|
| WRITE | 473.72 | 496.73 | 1147.00 | 2661.10 |

### Client Throughput Distribution

| Client | Avg Throughput (MiB/s) | Avg Throughput (obj/s) |
|--------|------------------------|----------------------|
| Client 1 | 62.84 | 65.89 |
| Client 2 | 66.01 | 69.22 |
| Client 3 | 63.55 | 66.64 |
| Client 4 | 63.27 | 66.35 |
| Client 5 | 59.42 | 62.30 |
| Client 6 | 60.47 | 63.41 |
| Client 7 | 61.64 | 64.63 |
| Client 8 | 65.47 | 68.65 |

## PUT_TEST Results

### Statistics

- **Total runs**: 2
- **Throughput (MiB/s)**: Mean=601.43, Min=569.82, Max=633.05
- **Average Latency (ms)**: Mean=1076.85, Min=1048.20, Max=1105.50

### Individual Results

| Job Type | Throughput (MiB/s) | Throughput (obj/s) | Avg Latency (ms) | P99 Latency (ms) |
|----------|-------------------|-------------------|-----------------|-----------------|
| WRITE | 633.05 | 663.80 | 1105.50 | 2514.30 |
| WRITE | 569.82 | 597.50 | 1048.20 | 2000.30 |

### Client Throughput Distribution

| Client | Avg Throughput (MiB/s) | Avg Throughput (obj/s) |
|--------|------------------------|----------------------|
| Client 1 | 60.48 | 63.42 |
| Client 2 | 83.52 | 87.58 |
| Client 3 | 83.63 | 87.70 |
| Client 4 | 98.77 | 103.57 |
| Client 5 | 56.77 | 59.52 |
| Client 6 | 108.27 | 113.53 |
| Client 7 | 37.04 | 38.84 |
| Client 8 | 92.13 | 96.61 |

## GET_PROD Results

### Statistics

- **Total runs**: 1
- **Throughput (MiB/s)**: Mean=42.26, Min=42.26, Max=42.26
- **Average Latency (ms)**: Mean=96.90, Min=96.90, Max=96.90

### Individual Results

| Job Type | Throughput (MiB/s) | Throughput (obj/s) | Avg Latency (ms) | P99 Latency (ms) |
|----------|-------------------|-------------------|-----------------|-----------------|
| READ | 42.26 | 11079.28 | 96.90 | 641.80 |

### Client Throughput Distribution

| Client | Avg Throughput (MiB/s) | Avg Throughput (obj/s) |
|--------|------------------------|----------------------|
| Client 1 | 5.53 | 1449.65 |
| Client 2 | 5.51 | 1443.41 |
| Client 3 | 5.49 | 1439.65 |
| Client 4 | 5.45 | 1429.86 |
| Client 5 | 5.49 | 1439.79 |
| Client 6 | 5.50 | 1442.16 |
| Client 7 | 5.48 | 1437.79 |
| Client 8 | 5.52 | 1447.82 |

## GET_TEST Results

### Statistics

- **Total runs**: 2
- **Throughput (MiB/s)**: Mean=75.33, Min=0.05, Max=150.60
- **Average Latency (ms)**: Mean=88.50, Min=24.20, Max=152.80

### Individual Results

| Job Type | Throughput (MiB/s) | Throughput (obj/s) | Avg Latency (ms) | P99 Latency (ms) |
|----------|-------------------|-------------------|-----------------|-----------------|
| READ | 150.60 | 39479.23 | 24.20 | 141.90 |
| RPS | 0.05 | 53351.31 | 152.80 | 382.70 |

### Client Throughput Distribution

| Client | Avg Throughput (MiB/s) | Avg Throughput (obj/s) |
|--------|------------------------|----------------------|
| Client 1 | 13.55 | 5801.69 |
| Client 2 | 14.09 | 5942.46 |
| Client 3 | 13.89 | 5890.45 |
| Client 4 | 14.09 | 5935.80 |
| Client 5 | 13.36 | 5742.90 |
| Client 6 | 13.08 | 5644.19 |
| Client 7 | 13.47 | 5754.24 |
| Client 8 | 13.34 | 5713.44 |

## MIXED_TEST Results

### Statistics

- **Total runs**: 1
- **Throughput (MiB/s)**: Mean=858.38, Min=858.38, Max=858.38
- **Average Latency (ms)**: Mean=25.90, Min=25.90, Max=25.90

### Individual Results

| Job Type | Throughput (MiB/s) | Throughput (obj/s) | Avg Latency (ms) | P99 Latency (ms) |
|----------|-------------------|-------------------|-----------------|-----------------|
| MIXED | 858.38 | 900.08 | 25.90 | 249.90 |

### Client Throughput Distribution

| Client | Avg Throughput (MiB/s) | Avg Throughput (obj/s) |
|--------|------------------------|----------------------|
| Client 1 | 55.21 | 77.18 |
| Client 2 | 56.05 | 78.36 |
| Client 3 | 69.58 | 97.28 |
| Client 4 | 70.13 | 98.04 |
| Client 5 | 68.66 | 96.00 |
| Client 6 | 194.46 | 271.86 |
| Client 7 | 191.12 | 267.20 |
| Client 8 | 58.62 | 81.96 |

