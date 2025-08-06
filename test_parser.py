#!/usr/bin/env python3
"""
Test script to demonstrate warp results parser functionality
"""

import re
from datetime import datetime
from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class ParsedResult:
    """Data class for parsed results from results.md"""
    job_type: str
    environment: str
    operation: str
    concurrency: int
    duration: str
    avg_throughput_mib: float
    avg_throughput_obj: float
    avg_latency_ms: float
    p50_latency_ms: float
    p90_latency_ms: float
    p99_latency_ms: float
    fastest_req_ms: float
    slowest_req_ms: float
    stddev_ms: float
    ttfb_avg_ms: float = None
    ttfb_best_ms: float = None
    ttfb_median_ms: float = None
    ttfb_99th_ms: float = None
    client_throughputs: List[Dict[str, float]] = None


def parse_results_md(filename: str = "results.md") -> List[ParsedResult]:
    """Parse the results.md file and extract metrics"""
    results = []
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split content by job sections (look for # followed by job names)
    sections = re.split(r'# (WRITE|READ|RPS|MIXED|SCALE)', content)
    
    for i in range(1, len(sections), 2):  # Skip first empty section, then take pairs
        if i + 1 >= len(sections):
            break
            
        job_type = sections[i]
        job_content = sections[i + 1]
        
        # Parse job type and environment
        if 'PROD' in job_content:
            environment = 'PROD'
        elif 'TEST' in job_content:
            environment = 'TEST'
        else:
            environment = 'UNKNOWN'
        
        # Determine operation type
        if 'WRITE' in job_type:
            operation = 'PUT'
        elif 'READ' in job_type:
            operation = 'GET'
        elif 'MIXED' in job_type:
            operation = 'MIXED'
        elif 'RPS' in job_type:
            operation = 'GET'  # RPS test is GET operation
        elif 'SCALE' in job_type:
            operation = 'PUT'  # Scale test is PUT operation
        else:
            operation = 'UNKNOWN'
        
        # Extract metrics using regex
        try:
            # Throughput
            throughput_match = re.search(r'Average: ([\d.]+) MiB/s, ([\d.]+) obj/s', job_content)
            if throughput_match:
                avg_throughput_mib = float(throughput_match.group(1))
                avg_throughput_obj = float(throughput_match.group(2))
            else:
                continue  # Skip if no throughput data
            
            # Latency
            latency_match = re.search(r'Reqs: Avg: ([\d.]+)ms, 50%: ([\d.]+)ms, 90%: ([\d.]+)ms, 99%: ([\d.]+)ms, Fastest: ([\d.]+)ms, Slowest: ([\d.]+)ms, StdDev: ([\d.]+)ms', job_content)
            if latency_match:
                avg_latency_ms = float(latency_match.group(1))
                p50_latency_ms = float(latency_match.group(2))
                p90_latency_ms = float(latency_match.group(3))
                p99_latency_ms = float(latency_match.group(4))
                fastest_req_ms = float(latency_match.group(5))
                slowest_req_ms = float(latency_match.group(6))
                stddev_ms = float(latency_match.group(7))
            else:
                continue  # Skip if no latency data
            
            # TTFB (if available)
            ttfb_match = re.search(r'TTFB: Avg: ([\d.]+)ms, Best: ([\d.]+)ms, 25th: ([\d.]+)ms, Median: ([\d.]+)ms, 75th: ([\d.]+)ms, 90th: ([\d.]+)ms, 99th: ([\d.]+)ms, Worst: ([\d.]+)s StdDev: ([\d.]+)ms', job_content)
            ttfb_avg_ms = None
            ttfb_best_ms = None
            ttfb_median_ms = None
            ttfb_99th_ms = None
            
            if ttfb_match:
                ttfb_avg_ms = float(ttfb_match.group(1))
                ttfb_best_ms = float(ttfb_match.group(2))
                ttfb_median_ms = float(ttfb_match.group(4))
                ttfb_99th_ms = float(ttfb_match.group(7))
            
            # Concurrency
            concurrency_match = re.search(r'Concurrency: ([\d.]+)', job_content)
            concurrency = int(float(concurrency_match.group(1))) if concurrency_match else 0
            
            # Duration
            duration_match = re.search(r'Ran: ([\dhms]+)', job_content)
            duration = duration_match.group(1) if duration_match else ""
            
            # Parse client throughputs
            client_throughputs = []
            client_lines = re.findall(r'Client (\d+) throughput: ([\d.]+) MiB/s, ([\d.]+) obj/s', job_content)
            for client_num, mib_per_sec, obj_per_sec in client_lines:
                client_throughputs.append({
                    'client_id': int(client_num),
                    'mib_per_sec': float(mib_per_sec),
                    'obj_per_sec': float(obj_per_sec)
                })
            
            # Create result object
            result = ParsedResult(
                job_type=job_type,
                environment=environment,
                operation=operation,
                concurrency=concurrency,
                duration=duration,
                avg_throughput_mib=avg_throughput_mib,
                avg_throughput_obj=avg_throughput_obj,
                avg_latency_ms=avg_latency_ms,
                p50_latency_ms=p50_latency_ms,
                p90_latency_ms=p90_latency_ms,
                p99_latency_ms=p99_latency_ms,
                fastest_req_ms=fastest_req_ms,
                slowest_req_ms=slowest_req_ms,
                stddev_ms=stddev_ms,
                ttfb_avg_ms=ttfb_avg_ms,
                ttfb_best_ms=ttfb_best_ms,
                ttfb_median_ms=ttfb_median_ms,
                ttfb_99th_ms=ttfb_99th_ms,
                client_throughputs=client_throughputs
            )
            
            results.append(result)
            
        except Exception as e:
            print(f"Error parsing section '{job_type}': {e}")
            continue
    
    return results


def generate_comparison_report(results: List[ParsedResult], output_file: str = "comparison_report.md"):
    """Generate a comparison report from parsed results with PROD vs TEST analysis"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Warp Benchmark Results Comparison Report\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total results parsed: {len(results)}\n\n")
        
        # Group results by operation and environment
        grouped = {}
        for result in results:
            key = f"{result.operation}_{result.environment}"
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(result)
        
        # Executive Summary with PROD vs TEST comparison
        f.write("## Executive Summary\n\n")
        
        # Find operations that have both PROD and TEST results
        operations = set()
        for job_key in grouped.keys():
            operation = job_key.split('_')[0]
            operations.add(operation)
        
        comparisons = []
        for operation in operations:
            prod_key = f"{operation}_PROD"
            test_key = f"{operation}_TEST"
            
            if prod_key in grouped and test_key in grouped:
                prod_results = grouped[prod_key]
                test_results = grouped[test_key]
                
                # Calculate averages
                prod_throughput = sum(r.avg_throughput_mib for r in prod_results) / len(prod_results)
                test_throughput = sum(r.avg_throughput_mib for r in test_results) / len(test_results)
                prod_latency = sum(r.avg_latency_ms for r in prod_results) / len(prod_results)
                test_latency = sum(r.avg_latency_ms for r in test_results) / len(test_results)
                
                # Calculate differences
                throughput_diff = ((test_throughput - prod_throughput) / prod_throughput) * 100
                latency_diff = ((test_latency - prod_latency) / prod_latency) * 100
                
                # Determine regressions
                throughput_regression = throughput_diff < -5.0  # 5% degradation
                latency_regression = latency_diff > 10.0  # 10% increase
                
                comparisons.append({
                    'operation': operation,
                    'throughput_diff': throughput_diff,
                    'latency_diff': latency_diff,
                    'throughput_regression': throughput_regression,
                    'latency_regression': latency_regression
                })
        
        if comparisons:
            f.write("### PROD vs TEST Comparison Summary\n\n")
            f.write("| Operation | Throughput Change | Latency Change | Status |\n")
            f.write("|-----------|-------------------|----------------|--------|\n")
            
            for comp in comparisons:
                status = "⚠️ REGRESSION" if comp['throughput_regression'] or comp['latency_regression'] else "✅ PASS"
                f.write(f"| {comp['operation']} | {comp['throughput_diff']:+.1f}% | "
                       f"{comp['latency_diff']:+.1f}% | {status} |\n")
            
            f.write("\n")
            
            # Regression Analysis
            regressions = [c for c in comparisons if c['throughput_regression'] or c['latency_regression']]
            if regressions:
                f.write("### ⚠️ Detected Regressions\n\n")
                for reg in regressions:
                    f.write(f"**{reg['operation']}**:\n")
                    if reg['throughput_regression']:
                        f.write(f"- Throughput decreased by {abs(reg['throughput_diff']):.1f}%\n")
                    if reg['latency_regression']:
                        f.write(f"- Latency increased by {reg['latency_diff']:.1f}%\n")
                    f.write("\n")
        else:
            f.write("No PROD vs TEST comparisons available (missing either PROD or TEST data)\n\n")
        
        # Summary table
        f.write("## Detailed Results Summary\n\n")
        f.write("| Job Type | Environment | Results Count | Avg Throughput (MiB/s) | Avg Latency (ms) |\n")
        f.write("|----------|-------------|---------------|------------------------|------------------|\n")
        
        for job_key, job_results in grouped.items():
            avg_throughput = sum(r.avg_throughput_mib for r in job_results) / len(job_results)
            avg_latency = sum(r.avg_latency_ms for r in job_results) / len(job_results)
            f.write(f"| {job_key} | {job_results[0].environment} | {len(job_results)} | "
                   f"{avg_throughput:.2f} | {avg_latency:.2f} |\n")
        
        f.write("\n")
        
        # PROD vs TEST Detailed Comparisons
        if comparisons:
            f.write("## PROD vs TEST Detailed Comparisons\n\n")
            
            for comp in comparisons:
                f.write(f"### {comp['operation']} Operation Comparison\n\n")
                
                prod_key = f"{comp['operation']}_PROD"
                test_key = f"{comp['operation']}_TEST"
                prod_results = grouped[prod_key]
                test_results = grouped[test_key]
                
                # Performance metrics comparison
                f.write("#### Performance Metrics\n\n")
                f.write("| Metric | PROD | TEST | Difference |\n")
                f.write("|--------|------|------|------------|\n")
                
                prod_throughput = sum(r.avg_throughput_mib for r in prod_results) / len(prod_results)
                test_throughput = sum(r.avg_throughput_mib for r in test_results) / len(test_results)
                prod_latency = sum(r.avg_latency_ms for r in prod_results) / len(prod_results)
                test_latency = sum(r.avg_latency_ms for r in test_results) / len(test_results)
                
                f.write(f"| Throughput (MiB/s) | {prod_throughput:.2f} | {test_throughput:.2f} | "
                       f"{comp['throughput_diff']:+.1f}% |\n")
                f.write(f"| Latency (ms) | {prod_latency:.2f} | {test_latency:.2f} | "
                       f"{comp['latency_diff']:+.1f}% |\n")
                
                f.write("\n")
                
                # Recommendations
                f.write("#### Recommendations\n\n")
                if comp['throughput_regression']:
                    f.write("- ⚠️ **Throughput regression detected** - Investigate performance degradation\n")
                if comp['latency_regression']:
                    f.write("- ⚠️ **Latency regression detected** - Check for bottlenecks or configuration issues\n")
                if not comp['throughput_regression'] and not comp['latency_regression']:
                    f.write("- ✅ **No regressions detected** - Performance is within acceptable limits\n")
                
                f.write("\n")
        
        # Detailed results by job type
        for job_key, job_results in grouped.items():
            f.write(f"## {job_key.upper()} Results\n\n")
            
            # Statistics
            throughputs = [r.avg_throughput_mib for r in job_results]
            latencies = [r.avg_latency_ms for r in job_results]
            
            f.write("### Statistics\n\n")
            f.write(f"- **Total runs**: {len(job_results)}\n")
            f.write(f"- **Throughput (MiB/s)**: Mean={sum(throughputs)/len(throughputs):.2f}, "
                   f"Min={min(throughputs):.2f}, Max={max(throughputs):.2f}\n")
            f.write(f"- **Average Latency (ms)**: Mean={sum(latencies)/len(latencies):.2f}, "
                   f"Min={min(latencies):.2f}, Max={max(latencies):.2f}\n\n")
            
            # Individual results table
            f.write("### Individual Results\n\n")
            f.write("| Job Type | Throughput (MiB/s) | Throughput (obj/s) | Avg Latency (ms) | P99 Latency (ms) |\n")
            f.write("|----------|-------------------|-------------------|-----------------|-----------------|\n")
            
            for result in job_results:
                f.write(f"| {result.job_type} | {result.avg_throughput_mib:.2f} | "
                       f"{result.avg_throughput_obj:.2f} | {result.avg_latency_ms:.2f} | "
                       f"{result.p99_latency_ms:.2f} |\n")
            
            f.write("\n")
            
            # Client distribution (if available)
            if job_results and job_results[0].client_throughputs:
                f.write("### Client Throughput Distribution\n\n")
                f.write("| Client | Avg Throughput (MiB/s) | Avg Throughput (obj/s) |\n")
                f.write("|--------|------------------------|----------------------|\n")
                
                # Calculate average across all runs for each client
                client_data = {}
                for result in job_results:
                    for client in result.client_throughputs:
                        client_id = client['client_id']
                        if client_id not in client_data:
                            client_data[client_id] = {'mib': [], 'obj': []}
                        client_data[client_id]['mib'].append(client['mib_per_sec'])
                        client_data[client_id]['obj'].append(client['obj_per_sec'])
                
                for client_id in sorted(client_data.keys()):
                    avg_mib = sum(client_data[client_id]['mib']) / len(client_data[client_id]['mib'])
                    avg_obj = sum(client_data[client_id]['obj']) / len(client_data[client_id]['obj'])
                    f.write(f"| Client {client_id} | {avg_mib:.2f} | {avg_obj:.2f} |\n")
                
                f.write("\n")
    
    print(f"Report generated: {output_file}")


def main():
    """Main function to test the parser"""
    print("Testing warp results parser with results.md...")
    
    # Parse results
    results = parse_results_md("results.md")
    
    if not results:
        print("No results found in results.md")
        return
    
    print(f"Parsed {len(results)} results:")
    for result in results:
        print(f"  {result.job_type} - {result.operation} - {result.environment} - "
              f"Throughput: {result.avg_throughput_mib:.2f} MiB/s")
    
    # Generate report
    generate_comparison_report(results, "test_comparison_report.md")
    
    print("\nTest completed successfully!")


if __name__ == "__main__":
    main() 