"""
UMG Memory Efficiency Benchmarks

Evaluates RAM usage and optimization during operations.
Tests memory scaling, cleanup, and concurrent operation memory usage.
"""

import time
import random
import sys
import os
from typing import List, Dict, Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.metrics_collector import MetricsCollector, Timer


class MemoryIntensiveStructure:
    """Simulates a memory-intensive data structure."""
    
    def __init__(self, size: int):
        self.data = [random.random() for _ in range(size)]
        self.metadata = {f"key_{i}": f"value_{i}" for i in range(min(size // 10, 1000))}
        self.references: List['MemoryIntensiveStructure'] = []
    
    def add_reference(self, ref: 'MemoryIntensiveStructure'):
        """Add a reference to another structure."""
        self.references.append(ref)
    
    def process(self):
        """Simulate data processing."""
        result = sum(self.data) / len(self.data) if self.data else 0
        return result
    
    def clear(self):
        """Clear internal data."""
        self.data.clear()
        self.metadata.clear()
        self.references.clear()


class ModuleGraph:
    """Simulated module graph with memory tracking."""
    
    def __init__(self, num_modules: int):
        self.modules: Dict[int, MemoryIntensiveStructure] = {}
        self.num_modules = num_modules
        self._initialize_modules()
    
    def _initialize_modules(self):
        """Initialize all modules."""
        for i in range(self.num_modules):
            # Variable size modules
            size = random.randint(100, 1000)
            self.modules[i] = MemoryIntensiveStructure(size)
    
    def add_connections(self, connections_per_module: int = 5):
        """Add inter-module connections."""
        for module_id, module in self.modules.items():
            available = [mid for mid in self.modules.keys() if mid != module_id]
            num_connections = min(connections_per_module, len(available))
            
            for target_id in random.sample(available, num_connections):
                module.add_reference(self.modules[target_id])
    
    def process_all_modules(self):
        """Process all modules."""
        results = []
        for module in self.modules.values():
            results.append(module.process())
        return results
    
    def cleanup(self):
        """Clean up all modules."""
        for module in self.modules.values():
            module.clear()
        self.modules.clear()


def benchmark_memory_scaling_small(collector: MetricsCollector, iterations: int = 10):
    """Benchmark memory usage with small graphs (100 nodes)."""
    for i in range(iterations):
        with Timer(collector, "memory_scaling_small", "umg_reasoning"):
            graph = ModuleGraph(100)
            graph.add_connections(5)
            results = graph.process_all_modules()
            
            # Record metrics
            collector.record_custom_metric("modules_processed", len(results))
            
            # Cleanup
            graph.cleanup()
            del graph


def benchmark_memory_scaling_medium(collector: MetricsCollector, iterations: int = 5):
    """Benchmark memory usage with medium graphs (500 nodes)."""
    for i in range(iterations):
        with Timer(collector, "memory_scaling_medium", "umg_reasoning"):
            graph = ModuleGraph(500)
            graph.add_connections(8)
            results = graph.process_all_modules()
            
            collector.record_custom_metric("modules_processed", len(results))
            
            graph.cleanup()
            del graph


def benchmark_memory_scaling_large(collector: MetricsCollector, iterations: int = 3):
    """Benchmark memory usage with large graphs (1000 nodes)."""
    for i in range(iterations):
        with Timer(collector, "memory_scaling_large", "umg_reasoning"):
            graph = ModuleGraph(1000)
            graph.add_connections(10)
            results = graph.process_all_modules()
            
            collector.record_custom_metric("modules_processed", len(results))
            
            graph.cleanup()
            del graph


def benchmark_memory_cleanup(collector: MetricsCollector, iterations: int = 20):
    """Benchmark memory cleanup after operations."""
    for i in range(iterations):
        # Create and populate graph
        graph = ModuleGraph(200)
        graph.add_connections(5)
        
        # Measure cleanup time
        with Timer(collector, "memory_cleanup", "umg_reasoning"):
            graph.cleanup()
            del graph


def benchmark_concurrent_operations(collector: MetricsCollector, iterations: int = 10):
    """Benchmark memory usage during concurrent operations."""
    for i in range(iterations):
        with Timer(collector, "concurrent_operations", "umg_reasoning"):
            # Create multiple graphs simultaneously
            graphs = []
            for j in range(5):
                graph = ModuleGraph(100)
                graph.add_connections(5)
                graphs.append(graph)
            
            # Process all
            all_results = []
            for graph in graphs:
                all_results.extend(graph.process_all_modules())
            
            collector.record_custom_metric("total_operations", len(all_results))
            
            # Cleanup
            for graph in graphs:
                graph.cleanup()
            graphs.clear()


def benchmark_memory_growth_rate(collector: MetricsCollector, iterations: int = 10):
    """Benchmark memory growth rate with increasing data."""
    sizes = [100, 200, 400, 800]
    
    for size in sizes:
        for i in range(iterations):
            with Timer(collector, f"memory_growth_{size}", "umg_reasoning"):
                graph = ModuleGraph(size)
                graph.add_connections(5)
                graph.process_all_modules()
                
                collector.record_custom_metric("graph_size", size)
                
                graph.cleanup()
                del graph


def benchmark_iterative_growth(collector: MetricsCollector, iterations: int = 5):
    """Benchmark memory during iterative graph growth."""
    for i in range(iterations):
        with Timer(collector, "iterative_growth", "umg_reasoning"):
            graph = ModuleGraph(50)
            
            # Iteratively add modules
            for growth_step in range(10):
                new_modules = {}
                for j in range(10):  # Add 10 modules at a time
                    module_id = graph.num_modules + j
                    new_modules[module_id] = MemoryIntensiveStructure(500)
                
                graph.modules.update(new_modules)
                graph.num_modules += 10
                graph.add_connections(5)
            
            results = graph.process_all_modules()
            collector.record_custom_metric("final_size", graph.num_modules)
            
            graph.cleanup()
            del graph


def run_all_benchmarks(mode: str = "comprehensive"):
    """Run all memory efficiency benchmarks."""
    collector = MetricsCollector()
    
    iterations = {
        "quick": {"small": 3, "medium": 2, "large": 1, "cleanup": 5, "concurrent": 3, "growth": 3, "iterative": 2},
        "comprehensive": {"small": 10, "medium": 5, "large": 3, "cleanup": 20, "concurrent": 10, "growth": 10, "iterative": 5}
    }
    
    iters = iterations.get(mode, iterations["comprehensive"])
    
    print(f"Running UMG Memory Efficiency Benchmarks (mode: {mode})...")
    
    print("  - Memory scaling (small)...")
    benchmark_memory_scaling_small(collector, iters["small"])
    
    print("  - Memory scaling (medium)...")
    benchmark_memory_scaling_medium(collector, iters["medium"])
    
    print("  - Memory scaling (large)...")
    benchmark_memory_scaling_large(collector, iters["large"])
    
    print("  - Memory cleanup...")
    benchmark_memory_cleanup(collector, iters["cleanup"])
    
    print("  - Concurrent operations...")
    benchmark_concurrent_operations(collector, iters["concurrent"])
    
    print("  - Memory growth rate...")
    benchmark_memory_growth_rate(collector, iters["growth"])
    
    print("  - Iterative growth...")
    benchmark_iterative_growth(collector, iters["iterative"])
    
    return collector.get_all_results()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="UMG Memory Efficiency Benchmarks")
    parser.add_argument("--mode", choices=["quick", "comprehensive"], default="comprehensive",
                        help="Benchmark mode")
    args = parser.parse_args()
    
    results = run_all_benchmarks(args.mode)
    
    print("\n" + "=" * 70)
    print("Results Summary:")
    print("=" * 70)
    
    for name, result in results.items():
        summary = result.get_summary()
        print(f"\n{name}:")
        if 'execution_time' in summary:
            exec_time = summary['execution_time']
            print(f"  Mean time: {exec_time['mean_ms']:.2f}ms")
        if 'memory' in summary:
            print(f"  Peak memory: {summary['memory']['peak_mb']:.2f}MB")
            print(f"  Mean memory: {summary['memory']['mean_mb']:.2f}MB")
