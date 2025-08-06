#!/usr/bin/env python3
"""
Simple script to run PROD vs TEST comparison analysis
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path to import our modules
sys.path.insert(0, str(Path(__file__).parent))

from parse_warp_results import WarpResultsParser


def main():
    """Run PROD vs TEST comparison analysis"""
    
    print("🔍 Warp PROD vs TEST Comparison Analysis")
    print("=" * 50)
    
    # Check if we have results to analyze
    results_dir = Path(".")
    warp_files = list(results_dir.glob("**/warp-*-*.json.zst"))
    
    if not warp_files:
        print("❌ No warp result files found!")
        print("   Please ensure you have collected results first.")
        print("   Run: ./collect_warp_results.ps1 --collect")
        print(f"   Searched in: {results_dir}")
        return
    
    print(f"📁 Found {len(warp_files)} warp result files")
    
    # Create parser and analyze results
    parser = WarpResultsParser(".")
    results = parser.find_and_parse_results()
    
    if not results:
        print("❌ No results could be parsed!")
        return
    
    print(f"✅ Successfully parsed {len(results)} results")
    
    # Group results by environment
    prod_results = [r for r in results if r.environment == "PROD"]
    test_results = [r for r in results if r.environment == "TEST"]
    
    print(f"📊 PROD results: {len(prod_results)}")
    print(f"🧪 TEST results: {len(test_results)}")
    
    # Run comparison analysis
    comparisons = parser.compare_prod_vs_test()
    
    if not comparisons:
        print("\n⚠️  No PROD vs TEST comparisons available")
        print("   Make sure you have both PROD and TEST results for the same operations")
        return
    
    print(f"\n🔍 Found {len(comparisons)} operation comparisons")
    
    # Display comparison summary
    print("\n📈 Comparison Summary:")
    print("-" * 80)
    print(f"{'Operation':<12} {'Throughput':<15} {'Latency':<15} {'Status':<12} {'Significance':<12}")
    print("-" * 80)
    
    regressions_found = 0
    
    for comp in comparisons:
        status = "⚠️ REGRESSION" if comp.throughput_regression or comp.latency_regression else "✅ PASS"
        significance_emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}[comp.significance_level]
        
        print(f"{comp.operation:<12} {comp.throughput_diff_percent:+.1f}%{'':<8} "
              f"{comp.latency_diff_percent:+.1f}%{'':<8} {status:<12} {significance_emoji} {comp.significance_level}")
        
        if comp.throughput_regression or comp.latency_regression:
            regressions_found += 1
    
    print("-" * 80)
    
    # Summary
    if regressions_found > 0:
        print(f"\n⚠️  {regressions_found} regression(s) detected!")
        print("   Check the detailed report for more information.")
    else:
        print(f"\n✅ No regressions detected - all tests passed!")
    
    # Generate detailed report
    print(f"\n📄 Generating detailed report...")
    parser.generate_comparison_report("warp_comparison_report.md")
    print(f"✅ Report generated: warp_comparison_report.md")
    
    # Show quick recommendations
    if regressions_found > 0:
        print(f"\n💡 Quick Recommendations:")
        for comp in comparisons:
            if comp.throughput_regression or comp.latency_regression:
                print(f"   • {comp.operation}: Investigate performance changes")
                if comp.throughput_regression:
                    print(f"     - Throughput decreased by {abs(comp.throughput_diff_percent):.1f}%")
                if comp.latency_regression:
                    print(f"     - Latency increased by {comp.latency_diff_percent:.1f}%")
    
    print(f"\n🎯 Analysis complete!")


if __name__ == "__main__":
    main() 