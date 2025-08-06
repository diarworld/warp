# Warp Benchmark Results Comparison Report

Generated: 2025-08-07 02:36:09
Total results parsed: 76

## Executive Summary

### PROD vs TEST Comparison Summary

| Operation | Throughput Change | Latency Change | Status | Significance |
|-----------|-------------------|----------------|--------|--------------|
| PUT (obj:obj1M, concurrent:concurrent64) | -10.6% | +8.5% | ⚠️ REGRESSION | 🔴 HIGH |
| GET (obj:obj4K, concurrent:concurrent128) | +141.1% | -75.8% | ✅ PASS | 🔴 HIGH |

### ⚠️ Detected Regressions

**PUT (obj:obj1M, concurrent:concurrent64)**:
- Throughput decreased by 10.6%
- Significance: HIGH

## Detailed Results Summary

| Job Type | Environment | Results Count | Avg Throughput (MiB/s) | Avg Latency (ms) |
|----------|-------------|---------------|------------------------|------------------|
| GET_PROD_obj4K_concurrent128 | PROD | 1 | 45.23 | 96.84 |
| GET_TEST_obj4K_concurrent128 | TEST | 3 | 109.03 | 23.47 |
| GET_TEST_obj1B_concurrent1024 | TEST | 4 | 0.01 | 152.93 |
| MIXED_TEST_obj1M_concurrent128 | TEST | 3 | 0.00 | 0.00 |
| PUT_PROD_obj1M_concurrent64 | PROD | 2 | 700.14 | 803.46 |
| PUT_TEST_obj1M_concurrent64 | TEST | 2 | 626.11 | 871.45 |
| PUT_TEST_obj512B_concurrent128 | TEST | 1 | 2.09 | 88701.27 |

## PROD vs TEST Detailed Comparisons

### PUT (obj:obj1M, concurrent:concurrent64) Operation Comparison

#### Performance Metrics

| Metric | PROD | TEST | Difference |
|--------|------|------|------------|
| Throughput (MiB/s) | 700.14 | 626.11 | -10.6% |
| Latency (ms) | 803.46 | 871.45 | +8.5% |

#### Statistical Analysis

- **Significance Level**: HIGH
- **PROD Sample Size**: 2 runs
- **TEST Sample Size**: 2 runs
- **PROD Throughput StdDev**: 274.00
- **TEST Throughput StdDev**: 73.07

#### Recommendations

- ⚠️ **Throughput regression detected** - Investigate performance degradation
- 🔴 **High significance** - Changes are statistically significant

### GET (obj:obj4K, concurrent:concurrent128) Operation Comparison

#### Performance Metrics

| Metric | PROD | TEST | Difference |
|--------|------|------|------------|
| Throughput (MiB/s) | 45.23 | 109.03 | +141.1% |
| Latency (ms) | 96.84 | 23.47 | -75.8% |

#### Statistical Analysis

- **Significance Level**: HIGH
- **PROD Sample Size**: 1 runs
- **TEST Sample Size**: 3 runs
- **PROD Throughput StdDev**: 0.00
- **TEST Throughput StdDev**: 60.73

#### Recommendations

- 🔴 **High significance** - Changes are statistically significant

## GET_PROD_OBJ4K_CONCURRENT128 Results

### Statistics

- **Total runs**: 1
- **Throughput (MiB/s)**: Mean=45.23, Min=45.23, Max=45.23, StdDev=0.00
- **Throughput (obj/s)**: Mean=11856.78, Min=11856.78, Max=11856.78, StdDev=0.00
- **Average Latency (ms)**: Mean=96.84, Min=96.84, Max=96.84, StdDev=0.00
- **P99 Latency (ms)**: Mean=641.81, Min=641.81, Max=641.81, StdDev=0.00

### Individual Results

| Timestamp | Container | Throughput (MiB/s) | Throughput (obj/s) | Avg Latency (ms) | P99 Latency (ms) |
|-----------|-----------|-------------------|-------------------|-----------------|-----------------|
| 2025-08-05 21:34:36 | e5bywi+OwD3hz+77MBU3+xzyOvc+c4MTWr+ny3jWa+I3ToY8+npIiW3 | 45.23 | 11856.78 | 96.84 | 641.81 |

### Client Throughput Distribution

| Client | Avg Throughput (MiB/s) | Avg Throughput (obj/s) |
|--------|------------------------|----------------------|
| Client 1 | 43.98 | 11530.13 |

## GET_TEST_OBJ4K_CONCURRENT128 Results

### Statistics

- **Total runs**: 3
- **Throughput (MiB/s)**: Mean=109.03, Min=42.35, Max=161.17, StdDev=60.73
- **Throughput (obj/s)**: Mean=28581.71, Min=11101.11, Max=42249.71, StdDev=15920.45
- **Average Latency (ms)**: Mean=23.47, Min=22.90, Max=23.98, StdDev=0.55
- **P99 Latency (ms)**: Mean=116.18, Min=63.94, Max=148.00, StdDev=45.60

### Individual Results

| Timestamp | Container | Throughput (MiB/s) | Throughput (obj/s) | Avg Latency (ms) | P99 Latency (ms) |
|-----------|-----------|-------------------|-------------------|-----------------|-----------------|
| 2025-08-05 21:37:57 | 8F7a1D+8PuQR5+hdm8fQ+790Qvc+nTzjrB+E09GxE+VZNa4p+EgkCvS | 161.17 | 42249.71 | 23.98 | 136.61 |
| 2025-08-05 21:40:19 | Sl6Hdd+Bgn6Y8+tXNopc+E3TsbX+UjhlZA+ndDfwd | 123.57 | 32394.30 | 23.55 | 148.00 |
| 2025-08-05 21:40:20 | atUaqa+BNb1wU | 42.35 | 11101.11 | 22.90 | 63.94 |

### Client Throughput Distribution

| Client | Avg Throughput (MiB/s) | Avg Throughput (obj/s) |
|--------|------------------------|----------------------|
| Client 1 | 108.82 | 28526.78 |

## GET_TEST_OBJ1B_CONCURRENT1024 Results

### Statistics

- **Total runs**: 4
- **Throughput (MiB/s)**: Mean=0.01, Min=0.01, Max=0.03, StdDev=0.01
- **Throughput (obj/s)**: Mean=13427.19, Min=6654.31, Max=26913.07, StdDev=9531.47
- **Average Latency (ms)**: Mean=152.93, Min=152.36, Max=153.96, StdDev=0.74
- **P99 Latency (ms)**: Mean=384.11, Min=375.86, Max=395.08, StdDev=8.36

### Individual Results

| Timestamp | Container | Throughput (MiB/s) | Throughput (obj/s) | Avg Latency (ms) | P99 Latency (ms) |
|-----------|-----------|-------------------|-------------------|-----------------|-----------------|
| 2025-08-05 22:01:06 | x7Cz9z+8vmpXz+oIB7NA+yWa1lC | 0.03 | 26913.07 | 152.41 | 379.80 |
| 2025-08-05 22:01:07 | pZPjHv+knHcCc | 0.01 | 13407.87 | 153.00 | 385.68 |
| 2025-08-05 22:01:08 | Yagn6w | 0.01 | 6654.31 | 153.96 | 395.08 |
| 2025-08-05 22:01:11 | hfhxUV | 0.01 | 6733.52 | 152.36 | 375.86 |

### Client Throughput Distribution

| Client | Avg Throughput (MiB/s) | Avg Throughput (obj/s) |
|--------|------------------------|----------------------|
| Client 1 | 0.01 | 13423.79 |

## MIXED_TEST_OBJ1M_CONCURRENT128 Results

### Statistics

- **Total runs**: 3
- **Throughput (MiB/s)**: Mean=0.00, Min=0.00, Max=0.00, StdDev=0.00
- **Throughput (obj/s)**: Mean=0.00, Min=0.00, Max=0.00, StdDev=0.00
- **Average Latency (ms)**: Mean=0.00, Min=0.00, Max=0.00, StdDev=0.00
- **P99 Latency (ms)**: Mean=0.00, Min=0.00, Max=0.00, StdDev=0.00

### Individual Results

| Timestamp | Container | Throughput (MiB/s) | Throughput (obj/s) | Avg Latency (ms) | P99 Latency (ms) |
|-----------|-----------|-------------------|-------------------|-----------------|-----------------|
| 2025-08-05 22:20:41 | FgLf6l+SqF83n | 0.00 | 0.00 | 0.00 | 0.00 |
| 2025-08-05 22:20:43 | dzlPSJ+AQ9SSW+80Y0La+2SBBx7+0xsLGO | 0.00 | 0.00 | 0.00 | 0.00 |
| 2025-08-05 22:20:44 | b9Lwol | 0.00 | 0.00 | 0.00 | 0.00 |

## PUT_PROD_OBJ1M_CONCURRENT64 Results

### Statistics

- **Total runs**: 2
- **Throughput (MiB/s)**: Mean=700.14, Min=506.39, Max=893.88, StdDev=274.00
- **Throughput (obj/s)**: Mean=734.15, Min=530.99, Max=937.30, StdDev=287.31
- **Average Latency (ms)**: Mean=803.46, Min=460.31, Max=1146.62, StdDev=485.29
- **P99 Latency (ms)**: Mean=3375.28, Min=2659.58, Max=4090.97, StdDev=1012.15

### Individual Results

| Timestamp | Container | Throughput (MiB/s) | Throughput (obj/s) | Avg Latency (ms) | P99 Latency (ms) |
|-----------|-----------|-------------------|-------------------|-----------------|-----------------|
| 2025-08-05 21:08:37 | 9YXefe+gXn1xt+yQFwJ0+hW4svV | 893.88 | 937.30 | 460.31 | 4090.97 |
| 2025-08-05 21:14:10 | LnuK4Q+R9GdAd+LPTBNq+XzhRkw+QA5XR5+abNvwZ+3D5ae3+bKktxo | 506.39 | 530.99 | 1146.62 | 2659.58 |

### Client Throughput Distribution

| Client | Avg Throughput (MiB/s) | Avg Throughput (obj/s) |
|--------|------------------------|----------------------|
| Client 1 | 696.27 | 730.09 |

## PUT_TEST_OBJ1M_CONCURRENT64 Results

### Statistics

- **Total runs**: 2
- **Throughput (MiB/s)**: Mean=626.11, Min=574.45, Max=677.78, StdDev=73.07
- **Throughput (obj/s)**: Mean=656.53, Min=602.35, Max=710.71, StdDev=76.62
- **Average Latency (ms)**: Mean=871.45, Min=793.01, Max=949.88, StdDev=110.93
- **P99 Latency (ms)**: Mean=2181.22, Min=1979.96, Max=2382.49, StdDev=284.63

### Individual Results

| Timestamp | Container | Throughput (MiB/s) | Throughput (obj/s) | Avg Latency (ms) | P99 Latency (ms) |
|-----------|-----------|-------------------|-------------------|-----------------|-----------------|
| 2025-08-05 21:17:54 | yAU3Go+30A3J1+myZFFb+PScHAn+DXakxS+Ef6B5c+cgL0dL+8YGs9b | 677.78 | 710.71 | 793.01 | 2382.49 |
| 2025-08-05 21:20:44 | xiPDbl+REvUrC+LLkqYm+cJdaus+Q6itKN+IzlP2P+g1upKb+Va8KgY | 574.45 | 602.35 | 949.88 | 1979.96 |

### Client Throughput Distribution

| Client | Avg Throughput (MiB/s) | Avg Throughput (obj/s) |
|--------|------------------------|----------------------|
| Client 1 | 620.61 | 650.75 |

## PUT_TEST_OBJ512B_CONCURRENT128 Results

### Statistics

- **Total runs**: 1
- **Throughput (MiB/s)**: Mean=2.09, Min=2.09, Max=2.09, StdDev=0.00
- **Throughput (obj/s)**: Mean=4286.91, Min=4286.91, Max=4286.91, StdDev=0.00
- **Average Latency (ms)**: Mean=88701.27, Min=88701.27, Max=88701.27, StdDev=0.00
- **P99 Latency (ms)**: Mean=169294.33, Min=169294.33, Max=169294.33, StdDev=0.00

### Individual Results

| Timestamp | Container | Throughput (MiB/s) | Throughput (obj/s) | Avg Latency (ms) | P99 Latency (ms) |
|-----------|-----------|-------------------|-------------------|-----------------|-----------------|
| 2025-08-05 23:27:14 | TmtlDl+wzhssU+QUBMTU+5RXtyx+VeD0r8+tmU3cC+lNmB5G+ffyfNB | 2.09 | 4286.91 | 88701.27 | 169294.33 |

### Client Throughput Distribution

| Client | Avg Throughput (MiB/s) | Avg Throughput (obj/s) |
|--------|------------------------|----------------------|
| Client 1 | 2.09 | 4288.53 |

