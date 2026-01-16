"""
Result Formatter for OCTO-AGI Benchmarks

Formats benchmark results for display, generates reports in multiple formats,
and supports visualization data export.
"""

import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path


class ResultFormatter:
    """
    Formats and exports benchmark results in multiple formats.
    
    Supported formats:
    - JSON (detailed machine-readable results)
    - Markdown (human-readable reports)
    - CSV (data analysis)
    - Console output (real-time feedback)
    """
    
    def __init__(self, output_dir: str = "benchmarks/results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def format_json(self, results: Dict[str, Any], indent: int = 2) -> str:
        """Format results as JSON string."""
        return json.dumps(results, indent=indent, default=str)
    
    def save_json(self, results: Dict[str, Any], filename: str = None) -> str:
        """Save results as JSON file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"benchmark_results_{timestamp}.json"
        
        filepath = self.output_dir / filename
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        return str(filepath)
    
    def format_markdown(self, results: Dict[str, Any]) -> str:
        """Format results as Markdown report."""
        lines = []
        lines.append("# OCTO-AGI Benchmark Results\n")
        lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Overall summary
        if 'summary' in results:
            lines.append("## Overall Summary\n")
            summary = results['summary']
            lines.append(f"- **Total Benchmarks:** {summary.get('total_benchmarks', 0)}")
            lines.append(f"- **Total Duration:** {summary.get('total_duration_seconds', 0):.2f}s")
            lines.append(f"- **Mode:** {summary.get('mode', 'unknown')}\n")
        
        # Results by category
        if 'categories' in results:
            lines.append("## Results by Category\n")
            
            for category, category_results in results['categories'].items():
                lines.append(f"### {category.replace('_', ' ').title()}\n")
                
                for benchmark_name, benchmark_data in category_results.items():
                    lines.append(f"#### {benchmark_name}\n")
                    
                    # Execution time
                    if 'execution_time' in benchmark_data:
                        exec_time = benchmark_data['execution_time']
                        lines.append("**Execution Time:**")
                        lines.append(f"- Mean: {exec_time.get('mean_ms', 0):.2f}ms")
                        lines.append(f"- Median: {exec_time.get('median_ms', 0):.2f}ms")
                        lines.append(f"- Min: {exec_time.get('min_ms', 0):.2f}ms")
                        lines.append(f"- Max: {exec_time.get('max_ms', 0):.2f}ms")
                        if exec_time.get('std_ms', 0) > 0:
                            lines.append(f"- Std Dev: {exec_time.get('std_ms', 0):.2f}ms")
                        lines.append("")
                    
                    # Memory
                    if 'memory' in benchmark_data:
                        memory = benchmark_data['memory']
                        lines.append("**Memory Usage:**")
                        lines.append(f"- Peak: {memory.get('peak_mb', 0):.2f}MB")
                        lines.append(f"- Mean: {memory.get('mean_mb', 0):.2f}MB")
                        lines.append("")
                    
                    # CPU
                    if 'cpu' in benchmark_data:
                        cpu = benchmark_data['cpu']
                        lines.append("**CPU Usage:**")
                        lines.append(f"- Mean: {cpu.get('mean_percent', 0):.1f}%")
                        lines.append(f"- Max: {cpu.get('max_percent', 0):.1f}%")
                        lines.append("")
                    
                    # Custom metrics
                    if 'custom_metrics' in benchmark_data:
                        lines.append("**Custom Metrics:**")
                        for metric_name, metric_data in benchmark_data['custom_metrics'].items():
                            lines.append(f"- {metric_name}:")
                            lines.append(f"  - Mean: {metric_data.get('mean', 0):.2f}")
                            lines.append(f"  - Min: {metric_data.get('min', 0):.2f}")
                            lines.append(f"  - Max: {metric_data.get('max', 0):.2f}")
                        lines.append("")
        
        # Performance thresholds
        if 'threshold_analysis' in results:
            lines.append("## Threshold Analysis\n")
            analysis = results['threshold_analysis']
            
            passed = analysis.get('passed', [])
            failed = analysis.get('failed', [])
            
            if passed:
                lines.append(f"✅ **Passed:** {len(passed)} benchmarks")
            if failed:
                lines.append(f"❌ **Failed:** {len(failed)} benchmarks")
                for failure in failed:
                    lines.append(f"  - {failure}")
            lines.append("")
        
        return "\n".join(lines)
    
    def save_markdown(self, results: Dict[str, Any], filename: str = None) -> str:
        """Save results as Markdown file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"benchmark_report_{timestamp}.md"
        
        filepath = self.output_dir / filename
        markdown = self.format_markdown(results)
        
        with open(filepath, 'w') as f:
            f.write(markdown)
        
        return str(filepath)
    
    def format_csv(self, results: Dict[str, Any]) -> str:
        """Format results as CSV data."""
        lines = []
        header = [
            "Category", "Benchmark", "Mean Time (ms)", "Median Time (ms)",
            "Min Time (ms)", "Max Time (ms)", "Peak Memory (MB)",
            "Mean CPU (%)"
        ]
        lines.append(",".join(header))
        
        if 'categories' in results:
            for category, category_results in results['categories'].items():
                for benchmark_name, benchmark_data in category_results.items():
                    row = [
                        category,
                        benchmark_name,
                        f"{benchmark_data.get('execution_time', {}).get('mean_ms', 0):.2f}",
                        f"{benchmark_data.get('execution_time', {}).get('median_ms', 0):.2f}",
                        f"{benchmark_data.get('execution_time', {}).get('min_ms', 0):.2f}",
                        f"{benchmark_data.get('execution_time', {}).get('max_ms', 0):.2f}",
                        f"{benchmark_data.get('memory', {}).get('peak_mb', 0):.2f}",
                        f"{benchmark_data.get('cpu', {}).get('mean_percent', 0):.1f}",
                    ]
                    lines.append(",".join(row))
        
        return "\n".join(lines)
    
    def save_csv(self, results: Dict[str, Any], filename: str = None) -> str:
        """Save results as CSV file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"benchmark_data_{timestamp}.csv"
        
        filepath = self.output_dir / filename
        csv_data = self.format_csv(results)
        
        with open(filepath, 'w') as f:
            f.write(csv_data)
        
        return str(filepath)
    
    def format_console(self, results: Dict[str, Any], verbosity: str = "normal") -> str:
        """Format results for console output."""
        lines = []
        
        if verbosity == "silent":
            return ""
        
        lines.append("=" * 70)
        lines.append("OCTO-AGI Benchmark Results")
        lines.append("=" * 70)
        
        if 'summary' in results:
            summary = results['summary']
            lines.append(f"\nTotal Benchmarks: {summary.get('total_benchmarks', 0)}")
            lines.append(f"Total Duration: {summary.get('total_duration_seconds', 0):.2f}s")
            lines.append(f"Mode: {summary.get('mode', 'unknown')}")
        
        if 'categories' in results:
            for category, category_results in results['categories'].items():
                lines.append(f"\n{'─' * 70}")
                lines.append(f"{category.replace('_', ' ').title()}")
                lines.append('─' * 70)
                
                for benchmark_name, benchmark_data in category_results.items():
                    lines.append(f"\n  {benchmark_name}:")
                    
                    if 'execution_time' in benchmark_data:
                        exec_time = benchmark_data['execution_time']
                        lines.append(f"    Time: {exec_time.get('mean_ms', 0):.2f}ms (mean)")
                    
                    if verbosity == "verbose":
                        if 'memory' in benchmark_data:
                            memory = benchmark_data['memory']
                            lines.append(f"    Memory: {memory.get('peak_mb', 0):.2f}MB (peak)")
                        
                        if 'cpu' in benchmark_data:
                            cpu = benchmark_data['cpu']
                            lines.append(f"    CPU: {cpu.get('mean_percent', 0):.1f}% (mean)")
        
        lines.append("\n" + "=" * 70)
        return "\n".join(lines)
    
    def print_console(self, results: Dict[str, Any], verbosity: str = "normal"):
        """Print results to console."""
        output = self.format_console(results, verbosity)
        print(output)
    
    def export_visualization_data(self, results: Dict[str, Any], filename: str = None) -> str:
        """
        Export data formatted for visualization tools.
        
        Returns path to the exported file.
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"visualization_data_{timestamp}.json"
        
        viz_dir = self.output_dir / "visualizations"
        viz_dir.mkdir(parents=True, exist_ok=True)
        filepath = viz_dir / filename
        
        # Transform data for visualization
        viz_data = {
            'timestamp': datetime.now().isoformat(),
            'charts': self._prepare_chart_data(results)
        }
        
        with open(filepath, 'w') as f:
            json.dump(viz_data, f, indent=2, default=str)
        
        return str(filepath)
    
    def _prepare_chart_data(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare data structures for charts."""
        charts = {
            'execution_times': [],
            'memory_usage': [],
            'cpu_usage': [],
        }
        
        if 'categories' in results:
            for category, category_results in results['categories'].items():
                for benchmark_name, benchmark_data in category_results.items():
                    label = f"{category}/{benchmark_name}"
                    
                    if 'execution_time' in benchmark_data:
                        charts['execution_times'].append({
                            'label': label,
                            'mean': benchmark_data['execution_time'].get('mean_ms', 0),
                            'min': benchmark_data['execution_time'].get('min_ms', 0),
                            'max': benchmark_data['execution_time'].get('max_ms', 0),
                        })
                    
                    if 'memory' in benchmark_data:
                        charts['memory_usage'].append({
                            'label': label,
                            'peak': benchmark_data['memory'].get('peak_mb', 0),
                            'mean': benchmark_data['memory'].get('mean_mb', 0),
                        })
                    
                    if 'cpu' in benchmark_data:
                        charts['cpu_usage'].append({
                            'label': label,
                            'mean': benchmark_data['cpu'].get('mean_percent', 0),
                            'max': benchmark_data['cpu'].get('max_percent', 0),
                        })
        
        return charts
    
    def save_all_formats(self, results: Dict[str, Any], base_filename: str = None) -> Dict[str, str]:
        """
        Save results in all supported formats.
        
        Returns dictionary mapping format names to file paths.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base = base_filename or f"benchmark_{timestamp}"
        
        saved_files = {
            'json': self.save_json(results, f"{base}.json"),
            'markdown': self.save_markdown(results, f"{base}.md"),
            'csv': self.save_csv(results, f"{base}.csv"),
            'visualization': self.export_visualization_data(results, f"{base}_viz.json"),
        }
        
        return saved_files
