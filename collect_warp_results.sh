#!/bin/bash

# Warp Results Collection and Analysis Script
# This script collects warp results from all containers and generates a comparison report

set -e

# Configuration
NAMESPACE="timesheet"
WARP_POD_PREFIX="warp-"
RESULTS_DIR="./warp_results"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if kubectl is available
check_kubectl() {
    if ! command -v kubectl &> /dev/null; then
        print_error "kubectl is not installed or not in PATH"
        exit 1
    fi
    
    if ! kubectl cluster-info &> /dev/null; then
        print_error "Cannot connect to Kubernetes cluster"
        exit 1
    fi
}

# Function to check if Python is available
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed or not in PATH"
        exit 1
    fi
}

# Function to get warp pod names
get_warp_pods() {
    print_status "Getting warp pod names..."
    kubectl get pods -n "$NAMESPACE" --no-headers -o custom-columns=":metadata.name" | grep "^$WARP_POD_PREFIX" || {
        print_error "No warp pods found in namespace $NAMESPACE"
        exit 1
    }
}

# Function to collect results from a single pod
collect_from_pod() {
    local pod_name="$1"
    local pod_results_dir="$RESULTS_DIR/$pod_name"
    
    print_status "Collecting results from pod: $pod_name"
    
    # Create directory for this pod's results
    mkdir -p "$pod_results_dir"
    
    # Find all warp result files in the pod
    local result_files
    result_files=$(kubectl exec -n "$NAMESPACE" "$pod_name" -- find /tmp -name "warp-*.json.zst" 2>/dev/null || true)
    
    if [ -z "$result_files" ]; then
        print_warning "No warp result files found in pod $pod_name"
        return
    fi
    
    # Copy each result file
    local file_count=0
    while IFS= read -r file; do
        if [ -n "$file" ]; then
            local filename=$(basename "$file")
            print_status "  Copying: $filename"
            kubectl cp "$NAMESPACE/$pod_name:$file" "$pod_results_dir/$filename" >/dev/null 2>&1 || {
                print_warning "Failed to copy $filename from $pod_name"
            }
            ((file_count++))
        fi
    done <<< "$result_files"
    
    print_success "Collected $file_count files from $pod_name"
}

# Function to collect all results
collect_all_results() {
    print_status "Starting warp results collection..."
    
    # Create results directory
    mkdir -p "$RESULTS_DIR"
    
    # Get all warp pods
    local pods
    pods=$(get_warp_pods)
    
    if [ -z "$pods" ]; then
        print_error "No warp pods found"
        exit 1
    fi
    
    print_status "Found warp pods:"
    echo "$pods" | while read -r pod; do
        echo "  - $pod"
    done
    
    # Collect from each pod
    local total_files=0
    while IFS= read -r pod; do
        if [ -n "$pod" ]; then
            collect_from_pod "$pod"
            local pod_file_count=$(find "$RESULTS_DIR/$pod" -name "*.json.zst" 2>/dev/null | wc -l)
            total_files=$((total_files + pod_file_count))
        fi
    done <<< "$pods"
    
    print_success "Collection complete. Total files collected: $total_files"
}

# Function to run the parser
run_parser() {
    print_status "Running warp results parser..."
    
    if [ ! -f "$SCRIPT_DIR/parse_warp_results.py" ]; then
        print_error "Parser script not found: $SCRIPT_DIR/parse_warp_results.py"
        exit 1
    fi
    
    # Run the parser
    cd "$SCRIPT_DIR"
    python3 parse_warp_results.py --results-dir "$RESULTS_DIR" --output "warp_comparison_report.md" --verbose
    
    if [ $? -eq 0 ]; then
        print_success "Report generated: warp_comparison_report.md"
    else
        print_error "Failed to generate report"
        exit 1
    fi
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -c, --collect    Collect results from all warp pods"
    echo "  -p, --parse      Parse collected results and generate report"
    echo "  -a, --all        Collect and parse (default)"
    echo "  -d, --dir DIR    Results directory (default: ./warp_results)"
    echo "  -n, --namespace  Kubernetes namespace (default: timesheet)"
    echo "  -h, --help       Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                    # Collect and parse all results"
    echo "  $0 --collect          # Only collect results"
    echo "  $0 --parse            # Only parse existing results"
    echo "  $0 --dir /tmp/results # Use custom results directory"
}

# Main function
main() {
    local action="all"
    local custom_results_dir=""
    local custom_namespace=""
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -c|--collect)
                action="collect"
                shift
                ;;
            -p|--parse)
                action="parse"
                shift
                ;;
            -a|--all)
                action="all"
                shift
                ;;
            -d|--dir)
                custom_results_dir="$2"
                shift 2
                ;;
            -n|--namespace)
                custom_namespace="$2"
                shift 2
                ;;
            -h|--help)
                show_usage
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done
    
    # Update configuration if custom values provided
    if [ -n "$custom_results_dir" ]; then
        RESULTS_DIR="$custom_results_dir"
    fi
    
    if [ -n "$custom_namespace" ]; then
        NAMESPACE="$custom_namespace"
    fi
    
    print_status "Configuration:"
    echo "  Namespace: $NAMESPACE"
    echo "  Results directory: $RESULTS_DIR"
    echo "  Action: $action"
    echo ""
    
    # Check prerequisites
    check_kubectl
    check_python
    
    # Execute requested action
    case $action in
        "collect")
            collect_all_results
            ;;
        "parse")
            if [ ! -d "$RESULTS_DIR" ]; then
                print_error "Results directory not found: $RESULTS_DIR"
                print_error "Run with --collect first to gather results"
                exit 1
            fi
            run_parser
            ;;
        "all")
            collect_all_results
            run_parser
            ;;
    esac
    
    print_success "Script completed successfully!"
}

# Run main function with all arguments
main "$@" 