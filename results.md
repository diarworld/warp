# WRITE PROD
# PARAMS : "put", "--host", "storage.yandexcloud.net", "--obj.size", "1M", "--concurrent", "64", "--duration", "1m"
Report: PUT. Concurrency: 512. Ran: 1m2s
 * Average: 473.72 MiB/s, 496.73 obj/s
 * Reqs: Avg: 1147.0ms, 50%: 1100.7ms, 90%: 1835.5ms, 99%: 2661.1ms, Fastest: 48.6ms, Slowest: 5431.3ms, StdDev: 528.4ms

Throughput by client:
Client 1 throughput: 62.84 MiB/s, 65.89 obj/s
Client 2 throughput: 66.01 MiB/s, 69.22 obj/s
Client 3 throughput: 63.55 MiB/s, 66.64 obj/s
Client 4 throughput: 63.27 MiB/s, 66.35 obj/s
Client 5 throughput: 59.42 MiB/s, 62.30 obj/s
Client 6 throughput: 60.47 MiB/s, 63.41 obj/s
Client 7 throughput: 61.64 MiB/s, 64.63 obj/s
Client 8 throughput: 65.47 MiB/s, 68.65 obj/s

Throughput, split into 58 x 1s:
 * Fastest: 844.6MiB/s, 885.67 obj/s
 * 50% Median: 486.1MiB/s, 509.74 obj/s
 * Slowest: 281.6MiB/s, 295.25 obj/s


# WRITE TEST
# PARAMS : "put", "--host", "s3-onprem.storage.yandex.net", "--obj.size", "1M", "--concurrent", "64", "--duration", "1m"
Report: PUT. Concurrency: 512. Ran: 1m3s
 * Average: 633.05 MiB/s, 663.80 obj/s
 * Reqs: Avg: 1105.5ms, 50%: 954.6ms, 90%: 1971.6ms, 99%: 2514.3ms, Fastest: 21.6ms, Slowest: 3694.1ms, StdDev: 506.6ms

Throughput by client:
Client 1 throughput: 30.55 MiB/s, 32.04 obj/s
Client 2 throughput: 123.64 MiB/s, 129.65 obj/s
Client 3 throughput: 124.23 MiB/s, 130.27 obj/s
Client 4 throughput: 105.46 MiB/s, 110.58 obj/s
Client 5 throughput: 30.75 MiB/s, 32.24 obj/s
Client 6 throughput: 124.43 MiB/s, 130.47 obj/s
Client 7 throughput: 30.55 MiB/s, 32.03 obj/s
Client 8 throughput: 97.79 MiB/s, 102.54 obj/s

Throughput, split into 59 x 1s:
 * Fastest: 749.3MiB/s, 785.66 obj/s
 * 50% Median: 677.2MiB/s, 710.12 obj/s
 * Slowest: 551.2MiB/s, 577.96 obj/s

# WRITE TEST
# PARAMS : "put", "--host", "s3-onprem.storage.yandex.net", "--obj.size", "1M", "--concurrent", "64", "--duration", "10m"
Report: PUT. Concurrency: 512. Ran: 10m3s
 * Average: 569.82 MiB/s, 597.50 obj/s
 * Reqs: Avg: 1048.2ms, 50%: 949.5ms, 90%: 1657.8ms, 99%: 2000.3ms, Fastest: 14.7ms, Slowest: 3636.5ms, StdDev: 431.2ms

Throughput by client:
Client 1 throughput: 90.41 MiB/s, 94.81 obj/s
Client 2 throughput: 43.40 MiB/s, 45.51 obj/s
Client 3 throughput: 43.03 MiB/s, 45.12 obj/s
Client 4 throughput: 92.08 MiB/s, 96.56 obj/s
Client 5 throughput: 82.78 MiB/s, 86.80 obj/s
Client 6 throughput: 92.11 MiB/s, 96.58 obj/s
Client 7 throughput: 43.53 MiB/s, 45.65 obj/s
Client 8 throughput: 86.47 MiB/s, 90.67 obj/s

Throughput, split into 599 x 1s:
 * Fastest: 759.1MiB/s, 796.00 obj/s
 * 50% Median: 599.1MiB/s, 628.25 obj/s
 * Slowest: 76.7MiB/s, 80.39 obj/s

# READ PROD
# PARAMS : "get", "--host", "storage.yandexcloud.net", "--obj.size", "4K", "--concurrent", "128", "--duration", "1m"
Report: GET. Concurrency: 1024. Ran: 1m1s
 * Average: 42.26 MiB/s, 11079.28 obj/s
 * Reqs: Avg: 96.9ms, 50%: 48.3ms, 90%: 237.1ms, 99%: 641.8ms, Fastest: 9.5ms, Slowest: 3730.4ms, StdDev: 129.7ms
 * TTFB: Avg: 97ms, Best: 10ms, 25th: 25ms, Median: 48ms, 75th: 109ms, 90th: 237ms, 99th: 642ms, Worst: 3.73s StdDev: 130ms

Throughput by client:
Client 1 throughput: 5.53 MiB/s, 1449.65 obj/s
Client 2 throughput: 5.51 MiB/s, 1443.41 obj/s
Client 3 throughput: 5.49 MiB/s, 1439.65 obj/s
Client 4 throughput: 5.45 MiB/s, 1429.86 obj/s
Client 5 throughput: 5.49 MiB/s, 1439.79 obj/s
Client 6 throughput: 5.50 MiB/s, 1442.16 obj/s
Client 7 throughput: 5.48 MiB/s, 1437.79 obj/s
Client 8 throughput: 5.52 MiB/s, 1447.82 obj/s

Throughput, split into 57 x 1s:
 * Fastest: 53.5MiB/s, 14033.52 obj/s
 * 50% Median: 49.4MiB/s, 12947.91 obj/s
 * Slowest: 5.3MiB/s, 1386.57 obj/s

# READ TEST
# PARAMS : "get", "--host", "s3-onprem.storage.yandex.net", "--obj.size", "4K", "--concurrent", "128", "--duration", "1m"
Report: GET. Concurrency: 1024. Ran: 1m1s
 * Average: 150.60 MiB/s, 39479.23 obj/s
 * Reqs: Avg: 24.2ms, 50%: 18.4ms, 90%: 38.8ms, 99%: 141.9ms, Fastest: 7.9ms, Slowest: 1044.4ms, StdDev: 26.9ms
 * TTFB: Avg: 24ms, Best: 8ms, 25th: 13ms, Median: 18ms, 75th: 28ms, 90th: 39ms, 99th: 139ms, Worst: 1.044s StdDev: 27ms

Throughput by client:
Client 1 throughput: 20.79 MiB/s, 5449.36 obj/s
Client 2 throughput: 20.90 MiB/s, 5477.84 obj/s
Client 3 throughput: 20.27 MiB/s, 5314.26 obj/s
Client 4 throughput: 20.82 MiB/s, 5458.42 obj/s
Client 5 throughput: 19.08 MiB/s, 5000.91 obj/s
Client 6 throughput: 19.37 MiB/s, 5077.96 obj/s
Client 7 throughput: 20.45 MiB/s, 5359.86 obj/s
Client 8 throughput: 18.97 MiB/s, 4973.72 obj/s

Throughput, split into 57 x 1s:
 * Fastest: 179.6MiB/s, 47089.52 obj/s
 * 50% Median: 162.9MiB/s, 42711.87 obj/s
 * Slowest: 103.6MiB/s, 27161.55 obj/s

#READ TEST 10m
Report: GET. Concurrency: 1024. Ran: 10m2s
 * Average: 164.82 MiB/s, 43206.41 obj/s
 * Reqs: Avg: 23.6ms, 50%: 18.2ms, 90%: 37.7ms, 99%: 129.7ms, Fastest: 7.6ms, Slowest: 1811.5ms, StdDev: 24.5ms
 * TTFB: Avg: 23ms, Best: 8ms, 25th: 13ms, Median: 18ms, 75th: 28ms, 90th: 38ms, 99th: 129ms, Worst: 1.811s StdDev: 25ms

Throughput by client:
Client 1 throughput: 19.85 MiB/s, 5204.30 obj/s
Client 2 throughput: 21.35 MiB/s, 5596.04 obj/s
Client 3 throughput: 21.39 MiB/s, 5606.68 obj/s
Client 4 throughput: 21.43 MiB/s, 5616.54 obj/s
Client 5 throughput: 20.98 MiB/s, 5498.83 obj/s
Client 6 throughput: 19.85 MiB/s, 5202.79 obj/s
Client 7 throughput: 19.94 MiB/s, 5228.43 obj/s
Client 8 throughput: 21.04 MiB/s, 5514.41 obj/s

Throughput, split into 598 x 1s:
 * Fastest: 185.9MiB/s, 48723.70 obj/s
 * 50% Median: 166.5MiB/s, 43640.84 obj/s
 * Slowest: 115.9MiB/s, 30370.04 obj/s

# RPS TEST 10m
# PARAMS : "get", "--host", "s3-onprem.storage.yandex.net", "--obj.size", "1B", "--concurrent", "1024", "--duration", "10m"
Report: GET. Concurrency: 8192. Ran: 10m1s
 * Average: 0.05 MiB/s, 53351.31 obj/s
 * Reqs: Avg: 152.8ms, 50%: 146.6ms, 90%: 245.7ms, 99%: 382.7ms, Fastest: 8.2ms, Slowest: 15051.4ms, StdDev: 86.6ms
 * TTFB: Avg: 153ms, Best: 8ms, 25th: 99ms, Median: 147ms, 75th: 195ms, 90th: 246ms, 99th: 383ms, Worst: 15.051s StdDev: 87ms

Throughput by client:
Client 1 throughput: 0.01 MiB/s, 6751.40 obj/s
Client 2 throughput: 0.01 MiB/s, 6753.49 obj/s
Client 3 throughput: 0.01 MiB/s, 6750.40 obj/s
Client 4 throughput: 0.01 MiB/s, 6732.43 obj/s
Client 5 throughput: 0.01 MiB/s, 6728.97 obj/s
Client 6 throughput: 0.01 MiB/s, 6651.83 obj/s
Client 7 throughput: 0.01 MiB/s, 6674.43 obj/s
Client 8 throughput: 0.01 MiB/s, 6652.20 obj/s

Throughput, split into 597 x 1s:
 * Fastest: 56.4KiB/s, 57761.36 obj/s
 * 50% Median: 52.9KiB/s, 54210.89 obj/s
 * Slowest: 33.6KiB/s, 34449.99 obj/s

# MIXED TEST
# PARAMS : "mixed", "--host", "s3-onprem.storage.yandex.net", "--obj.size", "1M", "--concurrent", "128", "--duration", "60m"
Report: DELETE. Concurrency: 1024. Ran: 1h0m1s
 * Average: 200.04 obj/s
 * Reqs: Avg: 25.9ms, 50%: 18.4ms, 90%: 21.6ms, 99%: 249.9ms, Fastest: 10.6ms, Slowest: 5252.5ms, StdDev: 39.5ms

Throughput by client:
Client 1 throughput: 14.48 obj/s
Client 2 throughput: 14.70 obj/s
Client 3 throughput: 18.25 obj/s
Client 4 throughput: 18.39 obj/s
Client 5 throughput: 18.00 obj/s
Client 6 throughput: 50.99 obj/s
Client 7 throughput: 50.11 obj/s
Client 8 throughput: 15.38 obj/s

Throughput, split into 3597 x 1s:
 * Fastest: 253.41 obj/s
 * 50% Median: 200.05 obj/s
 * Slowest: 125.81 obj/s

──────────────────────────────────

Report: GET. Concurrency: 1024. Ran: 1h0m2s
 * Average: 858.38 MiB/s, 900.08 obj/s
 * Reqs: Avg: 793.2ms, 50%: 793.6ms, 90%: 1167.8ms, 99%: 1539.6ms, Fastest: 16.2ms, Slowest: 6859.1ms, StdDev: 303.4ms
 * TTFB: Avg: 32ms, Best: 11ms, 25th: 19ms, Median: 22ms, 75th: 34ms, 90th: 46ms, 99th: 249ms, Worst: 5.125s StdDev: 36ms

Throughput by client:
Client 1 throughput: 62.12 MiB/s, 65.13 obj/s
Client 2 throughput: 63.06 MiB/s, 66.13 obj/s
Client 3 throughput: 78.29 MiB/s, 82.10 obj/s
Client 4 throughput: 78.90 MiB/s, 82.73 obj/s
Client 5 throughput: 77.25 MiB/s, 81.01 obj/s
Client 6 throughput: 218.83 MiB/s, 229.46 obj/s
Client 7 throughput: 215.06 MiB/s, 225.51 obj/s
Client 8 throughput: 65.96 MiB/s, 69.17 obj/s

Throughput, split into 3598 x 1s:
 * Fastest: 972.3MiB/s, 1019.54 obj/s
 * 50% Median: 862.2MiB/s, 904.12 obj/s
 * Slowest: 450.3MiB/s, 472.16 obj/s

──────────────────────────────────

Report: PUT. Concurrency: 1024. Ran: 1h0m3s
 * Average: 286.10 MiB/s, 300.00 obj/s
 * Reqs: Avg: 1901.0ms, 50%: 1822.5ms, 90%: 2831.8ms, 99%: 3408.9ms, Fastest: 74.1ms, Slowest: 9843.9ms, StdDev: 720.4ms

Throughput by client:
Client 1 throughput: 20.70 MiB/s, 21.71 obj/s
Client 2 throughput: 21.02 MiB/s, 22.04 obj/s
Client 3 throughput: 26.09 MiB/s, 27.36 obj/s
Client 4 throughput: 26.30 MiB/s, 27.57 obj/s
Client 5 throughput: 25.75 MiB/s, 27.00 obj/s
Client 6 throughput: 72.91 MiB/s, 76.45 obj/s
Client 7 throughput: 71.66 MiB/s, 75.14 obj/s
Client 8 throughput: 21.98 MiB/s, 23.05 obj/s

Throughput, split into 3598 x 1s:
 * Fastest: 319.5MiB/s, 334.97 obj/s
 * 50% Median: 287.1MiB/s, 301.04 obj/s
 * Slowest: 215.5MiB/s, 225.94 obj/s

──────────────────────────────────

Report: STAT. Concurrency: 1024. Ran: 1h0m1s
 * Average: 600.13 obj/s
 * Reqs: Avg: 23.1ms, 50%: 15.7ms, 90%: 18.3ms, 99%: 240.5ms, Fastest: 8.1ms, Slowest: 5035.3ms, StdDev: 40.4ms

Throughput by client:
Client 1 throughput: 43.43 obj/s
Client 2 throughput: 44.10 obj/s
Client 3 throughput: 54.74 obj/s
Client 4 throughput: 55.17 obj/s
Client 5 throughput: 54.02 obj/s
Client 6 throughput: 152.96 obj/s
Client 7 throughput: 150.34 obj/s
Client 8 throughput: 46.12 obj/s

Throughput, split into 3597 x 1s:
 * Fastest: 696.88 obj/s
 * 50% Median: 601.35 obj/s
 * Slowest: 372.98 obj/s


──────────────────────────────────

Report: Total. Concurrency: 1024. Ran: 1h0m3s
 * Average: 1144.40 MiB/s, 1999.98 obj/s

Throughput by client:
Client 1 throughput: 82.80 MiB/s, 144.71 obj/s
Client 2 throughput: 84.07 MiB/s, 146.92 obj/s
Client 3 throughput: 104.36 MiB/s, 182.39 obj/s
Client 4 throughput: 105.18 MiB/s, 183.82 obj/s
Client 5 throughput: 102.98 MiB/s, 179.98 obj/s
Client 6 throughput: 291.64 MiB/s, 509.68 obj/s
Client 7 throughput: 286.64 MiB/s, 500.94 obj/s
Client 8 throughput: 87.93 MiB/s, 153.67 obj/s

Throughput, split into 3598 x 1s:
 * Fastest: 1282.8MiB/s, 2267.80 obj/s
 * 50% Median: 1149.9MiB/s, 2006.44 obj/s
 * Slowest: 807.8MiB/s, 1345.86 obj/s