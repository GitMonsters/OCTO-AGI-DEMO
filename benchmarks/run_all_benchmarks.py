#!/usr/bin/env python3
"""
OCTO-AGI Benchmark Runner

Main benchmark runner script that executes all test categories,
collects and aggregates results, and generates comprehensive reports.
"""

import sys
import os
import argparse
import time
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

# Add benchmarks directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.metrics_collector import MetricsCollector
from utils.performance_profiler import PerformanceProfiler
from utils.result_formatter import ResultFormatter

# Import benchmark modules
from umg_reasoning import test_module_graph_traversal
from umg_reasoning import test_reasoning_depth
from umg_reasoning import test_memory_efficiency
from tetrahedral_spatial import test_3d_spatial_processing
from tetrahedral_spatial import test_multidimensional_mapping
from tetrahedral_spatial import test_geometric_inference
from deschooling_learning import test_learning_adaptation
from deschooling_learning import test_knowledge_retention
from deschooling_learning import test_creative_problem_solving
from unified_consciousness import test_cross_system_coherence
from unified_consciousness import test_integration_latency
from unified_consciousness import test_emergent_behavior


class BenchmarkRunner:
    """Main benchmark runner for OCTO-AGI system."""
    
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.formatter = ResultFormatter(self.config['general']['output_directory'])
        self.profiler = PerformanceProfiler(
            enable_memory_tracking=self.config['general']['enable_profiling']
        )
        self.results: Dict[str, Any] = {
            'categories': {},
            'summary': {},
            'metadata': {}
        }
        
    def _load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load benchmark configuration."""
        if config_path is None:
            config_path = os.path.join(
                os.path.dirname(__file__),
                'config',
                'benchmark_config.yaml'
            )
        
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _run_benchmark_category(self, category_name: str, benchmark_module, mode: str):
        """Run a single benchmark category."""
        print(f"\n{'=' * 70}")
        print(f"Running {category_name.replace('_', ' ').title()} Benchmarks")
        print('=' * 70)
        
        start_time = time.time()
        
        try:
            results = benchmark_module.run_all_benchmarks(mode=mode)
            duration = time.time() - start_time
            
            # Convert results to summary format
            category_results = {}
            for bench_name, bench_result in results.items():
                category_results[bench_name] = bench_result.get_summary()
            
            self.results['categories'][category_name] = category_results
            
            print(f"✓ Completed in {duration:.2f}s")
            return True
            
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            self.results['categories'][category_name] = {
                'error': str(e),
                'status': 'failed'
            }
            return False
    
    def run_category(self, category: str, mode: str = "comprehensive"):
        """Run a specific benchmark category."""
        categories = {
            'umg_reasoning': [
                ('module_graph_traversal', test_module_graph_traversal),
                ('reasoning_depth', test_reasoning_depth),
                ('memory_efficiency', test_memory_efficiency),
            ],
            'tetrahedral_spatial': [
                ('3d_spatial_processing', test_3d_spatial_processing),
                ('multidimensional_mapping', test_multidimensional_mapping),
                ('geometric_inference', test_geometric_inference),
            ],
            'deschooling_learning': [
                ('learning_adaptation', test_learning_adaptation),
                ('knowledge_retention', test_knowledge_retention),
                ('creative_problem_solving', test_creative_problem_solving),
            ],
            'unified_consciousness': [
                ('cross_system_coherence', test_cross_system_coherence),
                ('integration_latency', test_integration_latency),
                ('emergent_behavior', test_emergent_behavior),
            ],
        }
        
        if category not in categories:
            print(f"Error: Unknown category '{category}'")
            print(f"Available categories: {', '.join(categories.keys())}")
            return False
        
        success = True
        for bench_name, bench_module in categories[category]:
            full_name = f"{category}_{bench_name}"
            if not self._run_benchmark_category(full_name, bench_module, mode):
                success = False
        
        return success
    
    def run_all(self, mode: str = "comprehensive"):
        """Run all benchmark categories."""
        print("=" * 70)
        print("OCTO-AGI Comprehensive Benchmark Suite")
        print("=" * 70)
        print(f"Mode: {mode}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        overall_start = time.time()
        
        # Start profiling if enabled
        if self.config['general']['enable_profiling']:
            self.profiler.start()
        
        # Run all categories
        categories = ['umg_reasoning', 'tetrahedral_spatial', 
                     'deschooling_learning', 'unified_consciousness']
        
        total_benchmarks = 0
        successful_benchmarks = 0
        
        for category in categories:
            if self.run_category(category, mode):
                successful_benchmarks += len(self.results['categories'])
            total_benchmarks += 3  # Each category has 3 benchmark modules
        
        overall_duration = time.time() - overall_start
        
        # Stop profiling
        if self.config['general']['enable_profiling']:
            self.profiler.stop()
        
        # Compile summary
        self.results['summary'] = {
            'total_benchmarks': total_benchmarks,
            'successful_benchmarks': successful_benchmarks,
            'total_duration_seconds': overall_duration,
            'mode': mode,
            'timestamp': datetime.now().isoformat(),
        }
        
        # Add metadata
        self.results['metadata'] = {
            'config': self.config,
            'profiling': self.profiler.generate_report() if self.config['general']['enable_profiling'] else None,
        }
        
        return successful_benchmarks == total_benchmarks
    
    def analyze_thresholds(self):
        """Analyze results against performance thresholds."""
        thresholds = self.config['performance_thresholds']
        analysis = {
            'passed': [],
            'failed': [],
            'warnings': []
        }
        
        for category, category_results in self.results['categories'].items():
            if 'error' in category_results:
                analysis['failed'].append(f"{category}: {category_results['error']}")
                continue
            
            # Basic threshold checking (can be expanded)
            for bench_name, bench_data in category_results.items():
                if 'execution_time' in bench_data:
                    mean_time = bench_data['execution_time'].get('mean_ms', 0)
                    
                    # Simple threshold check - can be made more sophisticated
                    if mean_time > 1000:  # More than 1 second
                        analysis['warnings'].append(
                            f"{category}/{bench_name}: High execution time ({mean_time:.2f}ms)"
                        )
                    else:
                        analysis['passed'].append(f"{category}/{bench_name}")
        
        self.results['threshold_analysis'] = analysis
        return analysis
    
    def generate_reports(self):
        """Generate all output reports."""
        print("\n" + "=" * 70)
        print("Generating Reports")
        print("=" * 70)
        
        output_config = self.config['output']
        saved_files = {}
        
        # Analyze thresholds
        self.analyze_thresholds()
        
        # Generate reports based on configuration
        if output_config['json_report']:
            json_path = self.formatter.save_json(self.results)
            saved_files['json'] = json_path
            print(f"✓ JSON report: {json_path}")
        
        if output_config['markdown_report']:
            md_path = self.formatter.save_markdown(self.results)
            saved_files['markdown'] = md_path
            print(f"✓ Markdown report: {md_path}")
        
        if output_config['csv_export']:
            csv_path = self.formatter.save_csv(self.results)
            saved_files['csv'] = csv_path
            print(f"✓ CSV export: {csv_path}")
        
        if self.config['general']['save_visualizations']:
            viz_path = self.formatter.export_visualization_data(self.results)
            saved_files['visualization'] = viz_path
            print(f"✓ Visualization data: {viz_path}")
        
        # Console output
        verbosity = output_config['console_verbosity']
        if verbosity != 'silent':
            print("\n" + "=" * 70)
            self.formatter.print_console(self.results, verbosity)
        
        return saved_files


def main():
    """Main entry point for benchmark runner."""
    parser = argparse.ArgumentParser(
        description='OCTO-AGI Benchmark Suite Runner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run all benchmarks in comprehensive mode
  python run_all_benchmarks.py
  
  # Run all benchmarks in quick mode
  python run_all_benchmarks.py --mode quick
  
  # Run only UMG reasoning benchmarks
  python run_all_benchmarks.py --category umg_reasoning
  
  # Run with custom configuration
  python run_all_benchmarks.py --config my_config.yaml
        """
    )
    
    parser.add_argument(
        '--mode',
        choices=['quick', 'comprehensive'],
        default='comprehensive',
        help='Benchmark execution mode (default: comprehensive)'
    )
    
    parser.add_argument(
        '--category',
        choices=['umg_reasoning', 'tetrahedral_spatial', 
                'deschooling_learning', 'unified_consciousness'],
        help='Run only a specific category of benchmarks'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        help='Path to custom configuration file'
    )
    
    parser.add_argument(
        '--list-categories',
        action='store_true',
        help='List available benchmark categories'
    )
    
    args = parser.parse_args()
    
    if args.list_categories:
        print("Available benchmark categories:")
        print("  - umg_reasoning: Universal Module Graph reasoning benchmarks")
        print("  - tetrahedral_spatial: Tetrahedral spatial reasoning benchmarks")
        print("  - deschooling_learning: Deschooling learning benchmarks")
        print("  - unified_consciousness: Unified consciousness integration benchmarks")
        return 0
    
    # Create benchmark runner
    runner = BenchmarkRunner(config_path=args.config)
    
    # Run benchmarks
    if args.category:
        success = runner.run_category(args.category, mode=args.mode)
    else:
        success = runner.run_all(mode=args.mode)
    
    # Generate reports
    runner.generate_reports()
    
    # Print final summary
    print("\n" + "=" * 70)
    print("Benchmark Run Complete")
    print("=" * 70)
    
    summary = runner.results['summary']
    print(f"Total Duration: {summary.get('total_duration_seconds', 0):.2f}s")
    print(f"Benchmarks: {summary.get('successful_benchmarks', 0)}/{summary.get('total_benchmarks', 0)} successful")
    
    threshold_analysis = runner.results.get('threshold_analysis', {})
    passed = len(threshold_analysis.get('passed', []))
    failed = len(threshold_analysis.get('failed', []))
    warnings = len(threshold_analysis.get('warnings', []))
    
    if failed > 0:
        print(f"✗ {failed} benchmark(s) failed")
    if warnings > 0:
        print(f"⚠ {warnings} warning(s)")
    if passed > 0:
        print(f"✓ {passed} benchmark(s) passed")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
