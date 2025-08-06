#!/usr/bin/env python3
"""
Warp Results Parser and Reporter

This script parses warp benchmark results from all containers and generates
a comprehensive comparison report across different job types and environments.
"""

import json
import gzip
import zstandard as zstd
import os
import glob
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import argparse


@dataclass
class WarpResult:
    """Data class to store parsed warp result metrics"""
    job_name: str
    container_id: str
    timestamp: str
    operation: str  # PUT, GET, MIXED, etc.
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
    ttfb_avg_ms: Optional[float] = None
    ttfb_best_ms: Optional[float] = None
    ttfb_median_ms: Optional[float] = None
    ttfb_99th_ms: Optional[float] = None
    client_throughputs: List[Dict[str, float]] = None
    throughput_per_second: List[Dict[str, float]] = None
    environment: str = ""  # PROD, TEST
    obj_size: str = ""
    concurrent_requests: int = 0
    # Test parameters for proper grouping
    test_params: Dict[str, Any] = None


@dataclass
class ComparisonResult:
    """Data class to store comparison results between PROD and TEST"""
    operation: str
    prod_stats: Dict[str, Any]
    test_stats: Dict[str, Any]
    throughput_diff_percent: float
    latency_diff_percent: float
    throughput_regression: bool
    latency_regression: bool
    significance_level: str  # HIGH, MEDIUM, LOW


class WarpResultsParser:
    """Parser for warp benchmark results"""
    
    def __init__(self, results_dir: str = "."):
        self.results_dir = Path(results_dir)
        self.results: List[WarpResult] = []
        
    def parse_json_zst_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Parse a compressed JSON file from warp"""
        try:
            # Try zstd first (most likely for .json.zst files)
            try:
                with open(file_path, 'rb') as f:
                    dctx = zstd.ZstdDecompressor()
                    with dctx.stream_reader(f) as reader:
                        data = reader.read()
                        return json.loads(data.decode('utf-8'))
            except Exception as zstd_error:
                # Fallback to gzip if zstd fails
                try:
                    with gzip.open(file_path, 'rt', encoding='utf-8') as f:
                        return json.load(f)
                except Exception as gzip_error:
                    # If both fail, try reading as plain JSON
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            return json.load(f)
                    except Exception as json_error:
                        print(f"Error parsing {file_path}: zstd={zstd_error}, gzip={gzip_error}, json={json_error}")
                        return None
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return None
    
    def extract_metrics_from_report(self, report_data: Dict[str, Any], job_name: str, 
                                  container_id: str, timestamp: str) -> Optional[WarpResult]:
        """Extract metrics from a warp report"""
        try:
            # Extract basic info
            # Try to get operation from commandline first
            commandline = report_data.get('commandline', '')
            if 'get' in commandline.lower():
                operation = 'GET'
            elif 'put' in commandline.lower():
                operation = 'PUT'
            elif 'mixed' in commandline.lower():
                operation = 'MIXED'
            elif 'delete' in commandline.lower():
                operation = 'DELETE'
            elif 'stat' in commandline.lower():
                operation = 'STAT'
            else:
                operation = report_data.get('operation', 'UNKNOWN')
            
            concurrency = report_data.get('concurrency', 0)
            duration = report_data.get('duration', '')
            
            # Extract metrics from the correct location (by_op_type section)
            # First, determine the operation type to get the right section
            op_type = operation.upper()
            op_data = report_data.get('by_op_type', {}).get(op_type, {})
            
            # Extract throughput from the operation-specific section
            throughput_data = op_data.get('throughput', {})
            # Calculate throughput in MiB/s from bytes and duration
            total_bytes = throughput_data.get('bytes', 0)
            duration_ms = throughput_data.get('measure_duration_millis', 1)  # Avoid division by zero
            avg_throughput_mib = (total_bytes / (1024 * 1024)) / (duration_ms / 1000) if duration_ms > 0 else 0
            avg_throughput_obj = throughput_data.get('objects', 0) / (duration_ms / 1000) if duration_ms > 0 else 0
            
            # Extract latency metrics from requests_by_client
            # The structure is: requests_by_client -> client_id -> list of request periods -> single_sized_requests
            requests_by_client = op_data.get('requests_by_client', {})
            
            # Collect latency statistics from all clients
            all_avg_latencies = []
            all_p50_latencies = []
            all_p90_latencies = []
            all_p99_latencies = []
            all_fastest_latencies = []
            all_slowest_latencies = []
            all_stddev_latencies = []
            
            for client_requests in requests_by_client.values():
                if isinstance(client_requests, list):
                    for req_period in client_requests:
                        if isinstance(req_period, dict) and 'single_sized_requests' in req_period:
                            single_requests = req_period['single_sized_requests']
                            
                            # Extract latency statistics - different structure for GET vs PUT operations
                            if 'first_byte' in single_requests:
                                # GET operations have first_byte latency data
                                fb_stats = single_requests['first_byte']
                                all_avg_latencies.append(fb_stats.get('average_millis', 0))
                                all_p50_latencies.append(fb_stats.get('median_millis', 0))
                                all_p90_latencies.append(fb_stats.get('p90_millis', 0))
                                all_p99_latencies.append(fb_stats.get('p99_millis', 0))
                                all_fastest_latencies.append(fb_stats.get('fastest_millis', 0))
                                all_slowest_latencies.append(fb_stats.get('slowest_millis', 0))
                                all_stddev_latencies.append(fb_stats.get('std_dev_millis', 0))
                            elif 'dur_avg_millis' in single_requests:
                                # PUT operations have direct duration fields
                                all_avg_latencies.append(single_requests.get('dur_avg_millis', 0))
                                all_p50_latencies.append(single_requests.get('dur_median_millis', 0))
                                all_p90_latencies.append(single_requests.get('dur_90_millis', 0))
                                all_p99_latencies.append(single_requests.get('dur_99_millis', 0))
                                all_fastest_latencies.append(single_requests.get('fastest_millis', 0))
                                all_slowest_latencies.append(single_requests.get('slowest_millis', 0))
                                all_stddev_latencies.append(single_requests.get('std_dev_millis', 0))
            
            # Calculate overall latency statistics
            if all_avg_latencies:
                avg_latency_ms = sum(all_avg_latencies) / len(all_avg_latencies)
                p50_latency_ms = sum(all_p50_latencies) / len(all_p50_latencies)
                p90_latency_ms = sum(all_p90_latencies) / len(all_p90_latencies)
                p99_latency_ms = sum(all_p99_latencies) / len(all_p99_latencies)
                fastest_req_ms = min(all_fastest_latencies) if all_fastest_latencies else 0
                slowest_req_ms = max(all_slowest_latencies) if all_slowest_latencies else 0
                stddev_ms = sum(all_stddev_latencies) / len(all_stddev_latencies) if all_stddev_latencies else 0
            else:
                avg_latency_ms = p50_latency_ms = p90_latency_ms = p99_latency_ms = fastest_req_ms = slowest_req_ms = stddev_ms = 0
            
            # Extract TTFB if available
            ttfb_stats = report_data.get('ttfb', {})
            ttfb_avg_ms = ttfb_stats.get('average', None)
            ttfb_best_ms = ttfb_stats.get('best', None)
            ttfb_median_ms = ttfb_stats.get('median', None)
            ttfb_99th_ms = ttfb_stats.get('p99', None)
            
            # Extract client throughputs from throughput_by_client
            client_throughputs = []
            throughput_by_client = op_data.get('throughput_by_client', {})
            for client_id, client_data in throughput_by_client.items():
                if isinstance(client_data, dict):
                    client_bytes = client_data.get('bytes', 0)
                    client_duration_ms = client_data.get('measure_duration_millis', 1)
                    client_mib_per_sec = (client_bytes / (1024 * 1024)) / (client_duration_ms / 1000) if client_duration_ms > 0 else 0
                    client_obj_per_sec = client_data.get('objects', 0) / (client_duration_ms / 1000) if client_duration_ms > 0 else 0
                    
                    client_throughputs.append({
                        'mib_per_sec': client_mib_per_sec,
                        'obj_per_sec': client_obj_per_sec
                    })
            
            # Extract per-second throughput from segmented data
            throughput_per_second = []
            segmented_data = throughput_data.get('segmented', [])
            for segment in segmented_data:
                if isinstance(segment, dict):
                    segment_bytes = segment.get('bytes', 0)
                    segment_duration_ms = segment.get('duration_millis', 1)
                    segment_mib_per_sec = (segment_bytes / (1024 * 1024)) / (segment_duration_ms / 1000) if segment_duration_ms > 0 else 0
                    segment_obj_per_sec = segment.get('objects', 0) / (segment_duration_ms / 1000) if segment_duration_ms > 0 else 0
                    
                    throughput_per_second.append({
                        'mib_per_sec': segment_mib_per_sec,
                        'obj_per_sec': segment_obj_per_sec
                    })
            
            # Determine environment based on the host in commandline
            if "s3-onprem.storage.yandex.net" in commandline:
                environment = "TEST"
            elif "storage.yandexcloud.net" in commandline:
                environment = "PROD"
            else:
                # Fallback: look for environment indicators in the job name or operation
                if "test" in job_name.lower() or "test" in operation.lower():
                    environment = "TEST"
                elif "prod" in job_name.lower() or "prod" in operation.lower():
                    environment = "PROD"
                else:
                    # Default to PROD if no clear indicator
                    environment = "PROD"
            
            # Extract test parameters from commandline for proper grouping
            test_params = {}
            if commandline:
                # Extract object size (handle both --obj.size= and --obj.size formats)
                obj_size_match = re.search(r'--obj\.size[=\s]+(\S+)', commandline)
                if obj_size_match:
                    test_params['obj_size'] = obj_size_match.group(1)
                
                # Extract concurrency (handle both --concurrent= and --concurrent formats)
                concurrency_match = re.search(r'--concurrent[=\s]+(\d+)', commandline)
                if concurrency_match:
                    test_params['concurrency'] = int(concurrency_match.group(1))
                
                # Extract host (handle both --host= and --host formats)
                host_match = re.search(r'--host[=\s]+(\S+)', commandline)
                if host_match:
                    test_params['host'] = host_match.group(1)
                
                # Extract bucket (handle both --bucket= and --bucket formats)
                bucket_match = re.search(r'--bucket[=\s]+(\S+)', commandline)
                if bucket_match:
                    test_params['bucket'] = bucket_match.group(1)
            
            return WarpResult(
                job_name=job_name,
                container_id=container_id,
                timestamp=timestamp,
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
                client_throughputs=client_throughputs,
                throughput_per_second=throughput_per_second,
                environment=environment,
                test_params=test_params
            )
            
        except Exception as e:
            print(f"Error extracting metrics from {job_name}: {e}")
            return None
    
    def parse_filename(self, filename: str) -> tuple:
        """Parse warp result filename to extract job info"""
        # Example: warp-get-2025-08-05[213436]-e5bywi.json.zst
        pattern = r'warp-(\w+)-(\d{4}-\d{2}-\d{2})\[(\d{6})\]-([a-zA-Z0-9]+)\.json\.zst'
        match = re.match(pattern, filename)
        
        if match:
            operation = match.group(1)  # get, put, mixed, etc.
            date = match.group(2)
            time = match.group(3)
            container_id = match.group(4)
            timestamp = f"{date} {time[:2]}:{time[2:4]}:{time[4:6]}"
            return operation, timestamp, container_id
        
        return None, None, None
    
    def find_and_parse_results(self) -> List[WarpResult]:
        """Find all warp result files and parse them"""
        # Look for warp result files recursively in the results directory and subdirectories
        pattern = "**/warp-*-*.json.zst"
        result_files = list(self.results_dir.glob(pattern))
        
        if not result_files:
            print(f"No warp result files found matching pattern: {pattern}")
            print(f"Searched in: {self.results_dir}")
            return []
        
        print(f"Found {len(result_files)} warp result files")
        
        for file_path in result_files:
            operation, timestamp, container_id = self.parse_filename(file_path.name)
            
            if not all([operation, timestamp, container_id]):
                print(f"Could not parse filename: {file_path.name}")
                continue
            
            # Parse the JSON data
            json_data = self.parse_json_zst_file(file_path)
            if not json_data:
                continue
            
            # Extract metrics
            result = self.extract_metrics_from_report(
                json_data, operation, container_id, timestamp
            )
            
            if result:
                self.results.append(result)
                print(f"Parsed: {file_path.name}")
        
        return self.results
    
    def group_results_by_job(self) -> Dict[str, List[WarpResult]]:
        """Group results by job type, parameters, and timestamp (merge concurrent containers)"""
        # First, group by operation, environment, and test parameters
        temp_grouped = {}
        for result in self.results:
            # Create a key that includes operation, environment, and key parameters
            param_key = self._create_param_key(result)
            if param_key not in temp_grouped:
                temp_grouped[param_key] = []
            temp_grouped[param_key].append(result)
        
        # Now merge results by timestamp within each group
        merged_grouped = {}
        for param_key, results in temp_grouped.items():
            # Group by timestamp
            timestamp_groups = {}
            for result in results:
                if result.timestamp not in timestamp_groups:
                    timestamp_groups[result.timestamp] = []
                timestamp_groups[result.timestamp].append(result)
            
            # Merge results for each timestamp
            merged_results = []
            for timestamp, timestamp_results in timestamp_groups.items():
                if len(timestamp_results) > 1:
                    # Merge multiple containers for the same timestamp
                    merged_result = self._merge_container_results(timestamp_results)
                    merged_results.append(merged_result)
                else:
                    # Single container result
                    merged_results.append(timestamp_results[0])
            
            merged_grouped[param_key] = merged_results
        
        return merged_grouped
    
    def _create_param_key(self, result: WarpResult) -> str:
        """Create a key for grouping results by operation, environment, and test parameters"""
        params = result.test_params or {}
        obj_size = params.get('obj_size', 'unknown')
        concurrency = params.get('concurrency', 'unknown')
        
        # Create a descriptive key
        key_parts = [
            result.operation,
            result.environment,
            f"obj{obj_size}",
            f"concurrent{concurrency}"
        ]
        
        return "_".join(key_parts)
    
    def _merge_container_results(self, results: List[WarpResult]) -> WarpResult:
        """Merge results from multiple containers for the same timestamp"""
        if not results:
            return None
        
        # Use the first result as base
        base_result = results[0]
        
        # Sum throughput values (total capacity across all containers)
        total_throughput_mib = sum(r.avg_throughput_mib for r in results)
        total_throughput_obj = sum(r.avg_throughput_obj for r in results)
        
        # For latency, calculate weighted average based on throughput (requests per second)
        # Use throughput as weight since higher throughput means more requests contributing to latency
        total_weight = sum(r.avg_throughput_obj for r in results if r.avg_throughput_obj > 0)
        if total_weight > 0:
            # Weight by object throughput (requests per second) - more requests = more weight
            weighted_avg_latency = sum(r.avg_latency_ms * r.avg_throughput_obj for r in results if r.avg_throughput_obj > 0) / total_weight
            weighted_p50_latency = sum(r.p50_latency_ms * r.avg_throughput_obj for r in results if r.avg_throughput_obj > 0) / total_weight
            weighted_p90_latency = sum(r.p90_latency_ms * r.avg_throughput_obj for r in results if r.avg_throughput_obj > 0) / total_weight
            weighted_p99_latency = sum(r.p99_latency_ms * r.avg_throughput_obj for r in results if r.avg_throughput_obj > 0) / total_weight
        else:
            # Fallback to simple average if no throughput
            weighted_avg_latency = sum(r.avg_latency_ms for r in results) / len(results)
            weighted_p50_latency = sum(r.p50_latency_ms for r in results) / len(results)
            weighted_p90_latency = sum(r.p90_latency_ms for r in results) / len(results)
            weighted_p99_latency = sum(r.p99_latency_ms for r in results) / len(results)
        
        # For min/max values, take the extremes across all containers
        valid_fastest = [r.fastest_req_ms for r in results if r.fastest_req_ms > 0]
        valid_slowest = [r.slowest_req_ms for r in results if r.slowest_req_ms > 0]
        
        fastest_req_ms = min(valid_fastest) if valid_fastest else 0
        slowest_req_ms = max(valid_slowest) if valid_slowest else 0
        
        # Merge client throughputs
        merged_client_throughputs = []
        if results[0].client_throughputs:
            # Combine client throughputs from all containers
            max_clients = max(len(r.client_throughputs) for r in results if r.client_throughputs)
            for client_idx in range(max_clients):
                total_mib = sum(r.client_throughputs[client_idx]['mib_per_sec'] 
                              for r in results if r.client_throughputs and len(r.client_throughputs) > client_idx)
                total_obj = sum(r.client_throughputs[client_idx]['obj_per_sec'] 
                              for r in results if r.client_throughputs and len(r.client_throughputs) > client_idx)
                merged_client_throughputs.append({
                    'mib_per_sec': total_mib,
                    'obj_per_sec': total_obj
                })
        
        # Create merged container ID
        merged_container_id = "+".join(r.container_id for r in results)
        
        return WarpResult(
            job_name=base_result.job_name,
            container_id=merged_container_id,
            timestamp=base_result.timestamp,
            operation=base_result.operation,
            concurrency=base_result.concurrency,
            duration=base_result.duration,
            avg_throughput_mib=total_throughput_mib,
            avg_throughput_obj=total_throughput_obj,
            avg_latency_ms=weighted_avg_latency,
            p50_latency_ms=weighted_p50_latency,
            p90_latency_ms=weighted_p90_latency,
            p99_latency_ms=weighted_p99_latency,
            fastest_req_ms=fastest_req_ms,
            slowest_req_ms=slowest_req_ms,
            stddev_ms=base_result.stddev_ms,  # Keep from base result
            ttfb_avg_ms=base_result.ttfb_avg_ms,
            ttfb_best_ms=base_result.ttfb_best_ms,
            ttfb_median_ms=base_result.ttfb_median_ms,
            ttfb_99th_ms=base_result.ttfb_99th_ms,
            client_throughputs=merged_client_throughputs,
            throughput_per_second=base_result.throughput_per_second,
            environment=base_result.environment
        )
    
    def calculate_statistics(self, results: List[WarpResult]) -> Dict[str, Any]:
        """Calculate statistics for a group of results"""
        if not results:
            return {}
        
        throughputs_mib = [r.avg_throughput_mib for r in results]
        throughputs_obj = [r.avg_throughput_obj for r in results]
        latencies_avg = [r.avg_latency_ms for r in results]
        latencies_p99 = [r.p99_latency_ms for r in results]
        
        return {
            'count': len(results),
            'throughput_mib': {
                'mean': sum(throughputs_mib) / len(throughputs_mib),
                'min': min(throughputs_mib),
                'max': max(throughputs_mib),
                'stddev': self._calculate_stddev(throughputs_mib)
            },
            'throughput_obj': {
                'mean': sum(throughputs_obj) / len(throughputs_obj),
                'min': min(throughputs_obj),
                'max': max(throughputs_obj),
                'stddev': self._calculate_stddev(throughputs_obj)
            },
            'latency_avg': {
                'mean': sum(latencies_avg) / len(latencies_avg),
                'min': min(latencies_avg),
                'max': max(latencies_avg),
                'stddev': self._calculate_stddev(latencies_avg)
            },
            'latency_p99': {
                'mean': sum(latencies_p99) / len(latencies_p99),
                'min': min(latencies_p99),
                'max': max(latencies_p99),
                'stddev': self._calculate_stddev(latencies_p99)
            }
        }
    
    def _calculate_stddev(self, values: List[float]) -> float:
        """Calculate standard deviation"""
        if len(values) < 2:
            return 0.0
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
        return variance ** 0.5
    
    def compare_prod_vs_test(self) -> List[ComparisonResult]:
        """Compare PROD vs TEST results for each operation with matching parameters"""
        comparisons = []
        grouped_results = self.group_results_by_job()
        
        # Find parameter combinations that have both PROD and TEST results
        param_combinations = set()
        for param_key in grouped_results.keys():
            # Extract the parameter combination (everything except environment)
            parts = param_key.split('_')
            if len(parts) >= 4:  # operation_env_objX_concurrentY
                operation = parts[0]
                obj_size = parts[2] if len(parts) > 2 else 'unknown'
                concurrency = parts[3] if len(parts) > 3 else 'unknown'
                param_combo = f"{operation}_{obj_size}_{concurrency}"
                param_combinations.add(param_combo)
        
        for param_combo in param_combinations:
            # Find PROD and TEST keys for this parameter combination
            prod_key = None
            test_key = None
            
            for param_key in grouped_results.keys():
                if param_key.startswith(f"{param_combo.split('_')[0]}_PROD_") and param_key.endswith(f"_{param_combo.split('_')[1]}_{param_combo.split('_')[2]}"):
                    prod_key = param_key
                elif param_key.startswith(f"{param_combo.split('_')[0]}_TEST_") and param_key.endswith(f"_{param_combo.split('_')[1]}_{param_combo.split('_')[2]}"):
                    test_key = param_key
            
            if prod_key and test_key and prod_key in grouped_results and test_key in grouped_results:
                prod_stats = self.calculate_statistics(grouped_results[prod_key])
                test_stats = self.calculate_statistics(grouped_results[test_key])
                
                if prod_stats and test_stats:
                    # Calculate differences (handle zero values)
                    prod_throughput = prod_stats['throughput_mib']['mean']
                    test_throughput = test_stats['throughput_mib']['mean']
                    prod_latency = prod_stats['latency_avg']['mean']
                    test_latency = test_stats['latency_avg']['mean']
                    
                    if prod_throughput > 0:
                        throughput_diff = ((test_throughput - prod_throughput) / prod_throughput) * 100
                    else:
                        throughput_diff = 0.0  # Can't calculate percentage if PROD is 0
                    
                    if prod_latency > 0:
                        latency_diff = ((test_latency - prod_latency) / prod_latency) * 100
                    else:
                        latency_diff = 0.0  # Can't calculate percentage if PROD is 0
                    
                    # Determine if there are regressions (thresholds can be adjusted)
                    throughput_regression = throughput_diff < -5.0  # 5% degradation
                    latency_regression = latency_diff > 10.0  # 10% increase
                    
                    # Determine significance level
                    significance = self._determine_significance(prod_stats, test_stats)
                    
                    # Extract operation and parameters for display
                    operation = param_combo.split('_')[0]
                    obj_size = param_combo.split('_')[1]
                    concurrency = param_combo.split('_')[2]
                    
                    comparison = ComparisonResult(
                        operation=f"{operation} (obj:{obj_size}, concurrent:{concurrency})",
                        prod_stats=prod_stats,
                        test_stats=test_stats,
                        throughput_diff_percent=throughput_diff,
                        latency_diff_percent=latency_diff,
                        throughput_regression=throughput_regression,
                        latency_regression=latency_regression,
                        significance_level=significance
                    )
                    comparisons.append(comparison)
        
        return comparisons
    
    def _determine_significance(self, prod_stats: Dict[str, Any], test_stats: Dict[str, Any]) -> str:
        """Determine significance level of differences"""
        # Calculate coefficient of variation for both datasets
        prod_cv = prod_stats['throughput_mib']['stddev'] / prod_stats['throughput_mib']['mean'] if prod_stats['throughput_mib']['mean'] > 0 else 0
        test_cv = test_stats['throughput_mib']['stddev'] / test_stats['throughput_mib']['mean'] if test_stats['throughput_mib']['mean'] > 0 else 0
        
        # Calculate relative difference (handle zero values)
        prod_throughput = prod_stats['throughput_mib']['mean']
        test_throughput = test_stats['throughput_mib']['mean']
        
        if prod_throughput > 0:
            throughput_diff = abs((test_throughput - prod_throughput) / prod_throughput)
        else:
            throughput_diff = 0.0  # Can't calculate relative difference if PROD is 0
        
        # Determine significance based on difference magnitude and variability
        if throughput_diff > 0.2 or (prod_cv + test_cv) > 0.3:  # 20% difference or high variability
            return "HIGH"
        elif throughput_diff > 0.1 or (prod_cv + test_cv) > 0.15:  # 10% difference or moderate variability
            return "MEDIUM"
        else:
            return "LOW"
    
    def generate_comparison_report(self, output_file: str = "warp_comparison_report.md"):
        """Generate a comprehensive comparison report with PROD vs TEST analysis"""
        if not self.results:
            print("No results to report")
            return
        
        grouped_results = self.group_results_by_job()
        comparisons = self.compare_prod_vs_test()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Warp Benchmark Results Comparison Report\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total results parsed: {len(self.results)}\n\n")
            
            # Executive Summary
            f.write("## Executive Summary\n\n")
            
            if comparisons:
                f.write("### PROD vs TEST Comparison Summary\n\n")
                f.write("| Operation | Throughput Change | Latency Change | Status | Significance |\n")
                f.write("|-----------|-------------------|----------------|--------|--------------|\n")
                
                for comp in comparisons:
                    status = "⚠️ REGRESSION" if comp.throughput_regression or comp.latency_regression else "✅ PASS"
                    significance_emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}[comp.significance_level]
                    
                    f.write(f"| {comp.operation} | {comp.throughput_diff_percent:+.1f}% | "
                           f"{comp.latency_diff_percent:+.1f}% | {status} | {significance_emoji} {comp.significance_level} |\n")
                
                f.write("\n")
                
                # Regression Analysis
                regressions = [c for c in comparisons if c.throughput_regression or c.latency_regression]
                if regressions:
                    f.write("### ⚠️ Detected Regressions\n\n")
                    for reg in regressions:
                        f.write(f"**{reg.operation}**:\n")
                        if reg.throughput_regression:
                            f.write(f"- Throughput decreased by {abs(reg.throughput_diff_percent):.1f}%\n")
                        if reg.latency_regression:
                            f.write(f"- Latency increased by {reg.latency_diff_percent:.1f}%\n")
                        f.write(f"- Significance: {reg.significance_level}\n\n")
            else:
                f.write("No PROD vs TEST comparisons available (missing either PROD or TEST data)\n\n")
            
            # Summary table
            f.write("## Detailed Results Summary\n\n")
            f.write("| Job Type | Environment | Results Count | Avg Throughput (MiB/s) | Avg Latency (ms) |\n")
            f.write("|----------|-------------|---------------|------------------------|------------------|\n")
            
            for job_key, results in grouped_results.items():
                stats = self.calculate_statistics(results)
                if stats:
                    f.write(f"| {job_key} | {results[0].environment} | {stats['count']} | "
                           f"{stats['throughput_mib']['mean']:.2f} | "
                           f"{stats['latency_avg']['mean']:.2f} |\n")
            
            f.write("\n")
            
            # PROD vs TEST Detailed Comparisons
            if comparisons:
                f.write("## PROD vs TEST Detailed Comparisons\n\n")
                
                for comp in comparisons:
                    f.write(f"### {comp.operation} Operation Comparison\n\n")
                    
                    # Performance metrics comparison
                    f.write("#### Performance Metrics\n\n")
                    f.write("| Metric | PROD | TEST | Difference |\n")
                    f.write("|--------|------|------|------------|\n")
                    
                    prod_throughput = comp.prod_stats['throughput_mib']['mean']
                    test_throughput = comp.test_stats['throughput_mib']['mean']
                    prod_latency = comp.prod_stats['latency_avg']['mean']
                    test_latency = comp.test_stats['latency_avg']['mean']
                    
                    f.write(f"| Throughput (MiB/s) | {prod_throughput:.2f} | {test_throughput:.2f} | "
                           f"{comp.throughput_diff_percent:+.1f}% |\n")
                    f.write(f"| Latency (ms) | {prod_latency:.2f} | {test_latency:.2f} | "
                           f"{comp.latency_diff_percent:+.1f}% |\n")
                    
                    f.write("\n")
                    
                    # Statistical analysis
                    f.write("#### Statistical Analysis\n\n")
                    f.write(f"- **Significance Level**: {comp.significance_level}\n")
                    f.write(f"- **PROD Sample Size**: {comp.prod_stats['count']} runs\n")
                    f.write(f"- **TEST Sample Size**: {comp.test_stats['count']} runs\n")
                    f.write(f"- **PROD Throughput StdDev**: {comp.prod_stats['throughput_mib']['stddev']:.2f}\n")
                    f.write(f"- **TEST Throughput StdDev**: {comp.test_stats['throughput_mib']['stddev']:.2f}\n")
                    
                    # Recommendations
                    f.write("\n#### Recommendations\n\n")
                    if comp.throughput_regression:
                        f.write("- ⚠️ **Throughput regression detected** - Investigate performance degradation\n")
                    if comp.latency_regression:
                        f.write("- ⚠️ **Latency regression detected** - Check for bottlenecks or configuration issues\n")
                    if comp.significance_level == "HIGH":
                        f.write("- 🔴 **High significance** - Changes are statistically significant\n")
                    elif comp.significance_level == "MEDIUM":
                        f.write("- 🟡 **Medium significance** - Monitor for trends\n")
                    else:
                        f.write("- 🟢 **Low significance** - Changes are within normal variation\n")
                    
                    f.write("\n")
            
            # Detailed results by job type
            for job_key, results in grouped_results.items():
                f.write(f"## {job_key.upper()} Results\n\n")
                
                # Sort by timestamp
                results.sort(key=lambda x: x.timestamp)
                
                # Statistics
                stats = self.calculate_statistics(results)
                if stats:
                    f.write("### Statistics\n\n")
                    f.write(f"- **Total runs**: {stats['count']}\n")
                    f.write(f"- **Throughput (MiB/s)**: Mean={stats['throughput_mib']['mean']:.2f}, "
                           f"Min={stats['throughput_mib']['min']:.2f}, "
                           f"Max={stats['throughput_mib']['max']:.2f}, "
                           f"StdDev={stats['throughput_mib']['stddev']:.2f}\n")
                    f.write(f"- **Throughput (obj/s)**: Mean={stats['throughput_obj']['mean']:.2f}, "
                           f"Min={stats['throughput_obj']['min']:.2f}, "
                           f"Max={stats['throughput_obj']['max']:.2f}, "
                           f"StdDev={stats['throughput_obj']['stddev']:.2f}\n")
                    f.write(f"- **Average Latency (ms)**: Mean={stats['latency_avg']['mean']:.2f}, "
                           f"Min={stats['latency_avg']['min']:.2f}, "
                           f"Max={stats['latency_avg']['max']:.2f}, "
                           f"StdDev={stats['latency_avg']['stddev']:.2f}\n")
                    f.write(f"- **P99 Latency (ms)**: Mean={stats['latency_p99']['mean']:.2f}, "
                           f"Min={stats['latency_p99']['min']:.2f}, "
                           f"Max={stats['latency_p99']['max']:.2f}, "
                           f"StdDev={stats['latency_p99']['stddev']:.2f}\n\n")
                
                # Individual results table
                f.write("### Individual Results\n\n")
                f.write("| Timestamp | Container | Throughput (MiB/s) | Throughput (obj/s) | Avg Latency (ms) | P99 Latency (ms) |\n")
                f.write("|-----------|-----------|-------------------|-------------------|-----------------|-----------------|\n")
                
                for result in results:
                    f.write(f"| {result.timestamp} | {result.container_id} | "
                           f"{result.avg_throughput_mib:.2f} | "
                           f"{result.avg_throughput_obj:.2f} | "
                           f"{result.avg_latency_ms:.2f} | "
                           f"{result.p99_latency_ms:.2f} |\n")
                
                f.write("\n")
                
                # Client distribution (if available)
                if results and results[0].client_throughputs:
                    f.write("### Client Throughput Distribution\n\n")
                    f.write("| Client | Avg Throughput (MiB/s) | Avg Throughput (obj/s) |\n")
                    f.write("|--------|------------------------|----------------------|\n")
                    
                    # Calculate average across all runs for each client
                    client_count = len(results[0].client_throughputs)
                    for client_idx in range(client_count):
                        total_mib = sum(r.client_throughputs[client_idx]['mib_per_sec'] 
                                      for r in results if r.client_throughputs)
                        total_obj = sum(r.client_throughputs[client_idx]['obj_per_sec'] 
                                      for r in results if r.client_throughputs)
                        avg_mib = total_mib / len(results)
                        avg_obj = total_obj / len(results)
                        
                        f.write(f"| Client {client_idx + 1} | {avg_mib:.2f} | {avg_obj:.2f} |\n")
                    
                    f.write("\n")
        
        print(f"Report generated: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Parse warp benchmark results and generate comparison report')
    parser.add_argument('--results-dir', default='.', help='Directory containing warp result files')
    parser.add_argument('--output', default='warp_comparison_report.md', help='Output report file')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Create parser and parse results
    warp_parser = WarpResultsParser(args.results_dir)
    results = warp_parser.find_and_parse_results()
    
    if args.verbose:
        print(f"\nParsed {len(results)} results:")
        for result in results:
            print(f"  {result.job_name} - {result.operation} - {result.environment} - "
                  f"Throughput: {result.avg_throughput_mib:.2f} MiB/s")
    
    # Generate report
    warp_parser.generate_comparison_report(args.output)


if __name__ == "__main__":
    main() 