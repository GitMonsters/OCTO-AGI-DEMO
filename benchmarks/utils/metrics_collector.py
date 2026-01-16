"""
Metrics Collector for OCTO-AGI Benchmarks

Collects and tracks performance metrics including time, memory, CPU usage,
and custom metrics.
"""

import time
import psutil
import os
from typing import Dict, List, Any, Optional
from contextlib import contextmanager
from dataclasses import dataclass, field
from statistics import mean, median, stdev


@dataclass
class Metric:
    """Represents a single metric measurement."""
    name: str
    value: float
    unit: str
    timestamp: float = field(default_factory=time.time)


@dataclass
class BenchmarkResult:
    """Stores results from a benchmark run."""
    name: str
    category: str
    execution_times: List[float] = field(default_factory=list)
    memory_usage: List[float] = field(default_factory=list)
    cpu_usage: List[float] = field(default_factory=list)
    custom_metrics: Dict[str, List[float]] = field(default_factory=dict)
    
    def add_execution_time(self, time_seconds: float):
        """Add an execution time measurement."""
        self.execution_times.append(time_seconds)
    
    def add_memory_usage(self, memory_mb: float):
        """Add a memory usage measurement."""
        self.memory_usage.append(memory_mb)
    
    def add_cpu_usage(self, cpu_percent: float):
        """Add a CPU usage measurement."""
        self.cpu_usage.append(cpu_percent)
    
    def add_custom_metric(self, name: str, value: float):
        """Add a custom metric measurement."""
        if name not in self.custom_metrics:
            self.custom_metrics[name] = []
        self.custom_metrics[name].append(value)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get statistical summary of all metrics."""
        summary = {
            'name': self.name,
            'category': self.category,
        }
        
        if self.execution_times:
            summary['execution_time'] = {
                'mean_ms': mean(self.execution_times) * 1000,
                'median_ms': median(self.execution_times) * 1000,
                'min_ms': min(self.execution_times) * 1000,
                'max_ms': max(self.execution_times) * 1000,
                'std_ms': stdev(self.execution_times) * 1000 if len(self.execution_times) > 1 else 0,
                'count': len(self.execution_times)
            }
        
        if self.memory_usage:
            summary['memory'] = {
                'peak_mb': max(self.memory_usage),
                'mean_mb': mean(self.memory_usage),
                'min_mb': min(self.memory_usage),
            }
        
        if self.cpu_usage:
            summary['cpu'] = {
                'mean_percent': mean(self.cpu_usage),
                'max_percent': max(self.cpu_usage),
            }
        
        if self.custom_metrics:
            summary['custom_metrics'] = {}
            for name, values in self.custom_metrics.items():
                summary['custom_metrics'][name] = {
                    'mean': mean(values),
                    'median': median(values),
                    'min': min(values),
                    'max': max(values),
                }
        
        return summary


class MetricsCollector:
    """
    Collects performance metrics during benchmark execution.
    
    Features:
    - Time measurements
    - Memory profiling
    - CPU usage tracking
    - Custom metrics support
    - Statistical aggregation
    """
    
    def __init__(self):
        self.results: Dict[str, BenchmarkResult] = {}
        self.current_benchmark: Optional[str] = None
        self._process = psutil.Process(os.getpid())
        self._start_time: Optional[float] = None
        self._start_memory: Optional[float] = None
    
    def start_benchmark(self, name: str, category: str = "general"):
        """Start tracking a new benchmark."""
        self.current_benchmark = name
        if name not in self.results:
            self.results[name] = BenchmarkResult(name=name, category=category)
        self._start_time = time.perf_counter()
        self._start_memory = self._get_memory_usage()
    
    def end_benchmark(self):
        """End the current benchmark and record metrics."""
        if self.current_benchmark is None:
            return
        
        if self._start_time is not None:
            elapsed = time.perf_counter() - self._start_time
            self.results[self.current_benchmark].add_execution_time(elapsed)
        
        if self._start_memory is not None:
            current_memory = self._get_memory_usage()
            self.results[self.current_benchmark].add_memory_usage(current_memory)
        
        cpu_percent = self._process.cpu_percent()
        self.results[self.current_benchmark].add_cpu_usage(cpu_percent)
        
        self.current_benchmark = None
        self._start_time = None
        self._start_memory = None
    
    def record_custom_metric(self, name: str, value: float, benchmark: Optional[str] = None):
        """Record a custom metric value."""
        target = benchmark or self.current_benchmark
        if target and target in self.results:
            self.results[target].add_custom_metric(name, value)
    
    def _get_memory_usage(self) -> float:
        """Get current memory usage in MB."""
        return self._process.memory_info().rss / (1024 * 1024)
    
    def get_result(self, benchmark_name: str) -> Optional[BenchmarkResult]:
        """Get results for a specific benchmark."""
        return self.results.get(benchmark_name)
    
    def get_all_results(self) -> Dict[str, BenchmarkResult]:
        """Get all benchmark results."""
        return self.results
    
    def get_summary(self, benchmark_name: Optional[str] = None) -> Dict[str, Any]:
        """Get summary statistics for one or all benchmarks."""
        if benchmark_name:
            result = self.results.get(benchmark_name)
            return result.get_summary() if result else {}
        
        return {
            name: result.get_summary()
            for name, result in self.results.items()
        }
    
    def reset(self, benchmark_name: Optional[str] = None):
        """Reset metrics for one or all benchmarks."""
        if benchmark_name:
            if benchmark_name in self.results:
                del self.results[benchmark_name]
        else:
            self.results.clear()
            self.current_benchmark = None


@contextmanager
def Timer(collector: MetricsCollector, benchmark_name: str, category: str = "general"):
    """
    Context manager for automatic benchmark timing.
    
    Usage:
        collector = MetricsCollector()
        with Timer(collector, "my_benchmark", "my_category"):
            # Code to benchmark
            pass
    """
    collector.start_benchmark(benchmark_name, category)
    try:
        yield collector
    finally:
        collector.end_benchmark()


def benchmark(category: str = "general"):
    """
    Decorator for benchmarking functions.
    
    Usage:
        @benchmark(category="umg_reasoning")
        def my_benchmark_function():
            # Code to benchmark
            pass
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            collector = MetricsCollector()
            collector.start_benchmark(func.__name__, category)
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                collector.end_benchmark()
                # Store collector in function for later access
                if not hasattr(wrapper, '_collectors'):
                    wrapper._collectors = []
                wrapper._collectors.append(collector)
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper
    return decorator
