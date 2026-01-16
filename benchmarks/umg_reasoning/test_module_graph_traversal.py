"""
UMG Module Graph Traversal Benchmarks

Tests the speed and efficiency of navigating the Universal Module Graph.
Measures traversal time, memory usage, and path accuracy.
"""

import time
import random
from typing import List, Dict, Set, Tuple
from dataclasses import dataclass
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.metrics_collector import MetricsCollector, Timer


@dataclass
class GraphNode:
    """Represents a node in the Universal Module Graph."""
    id: int
    connections: List[int]
    data: Dict[str, any]
    
    def __hash__(self):
        return hash(self.id)


class UniversalModuleGraph:
    """Simulated Universal Module Graph for benchmarking."""
    
    def __init__(self, num_nodes: int, connections_per_node: int = 5):
        self.nodes: Dict[int, GraphNode] = {}
        self.num_nodes = num_nodes
        self._build_graph(num_nodes, connections_per_node)
    
    def _build_graph(self, num_nodes: int, connections_per_node: int):
        """Build a random graph structure."""
        # Create nodes
        for i in range(num_nodes):
            self.nodes[i] = GraphNode(
                id=i,
                connections=[],
                data={'value': random.random(), 'type': f'module_{i % 10}'}
            )
        
        # Create connections
        for node_id, node in self.nodes.items():
            available = [n for n in range(num_nodes) if n != node_id]
            num_connections = min(connections_per_node, len(available))
            node.connections = random.sample(available, num_connections)
    
    def breadth_first_search(self, start_id: int, target_id: int) -> List[int]:
        """Perform BFS to find path from start to target."""
        if start_id not in self.nodes or target_id not in self.nodes:
            return []
        
        visited: Set[int] = set()
        queue: List[Tuple[int, List[int]]] = [(start_id, [start_id])]
        
        while queue:
            current_id, path = queue.pop(0)
            
            if current_id == target_id:
                return path
            
            if current_id in visited:
                continue
            
            visited.add(current_id)
            
            for neighbor_id in self.nodes[current_id].connections:
                if neighbor_id not in visited:
                    queue.append((neighbor_id, path + [neighbor_id]))
        
        return []
    
    def depth_first_search(self, start_id: int, max_depth: int = 10) -> List[int]:
        """Perform DFS to explore graph."""
        if start_id not in self.nodes:
            return []
        
        visited: Set[int] = set()
        result: List[int] = []
        
        def dfs_recursive(node_id: int, depth: int):
            if depth >= max_depth or node_id in visited:
                return
            
            visited.add(node_id)
            result.append(node_id)
            
            for neighbor_id in self.nodes[node_id].connections:
                dfs_recursive(neighbor_id, depth + 1)
        
        dfs_recursive(start_id, 0)
        return result
    
    def get_all_paths(self, start_id: int, end_id: int, max_length: int = 5) -> List[List[int]]:
        """Find all paths between two nodes up to max_length."""
        if start_id not in self.nodes or end_id not in self.nodes:
            return []
        
        paths: List[List[int]] = []
        
        def find_paths_recursive(current_id: int, path: List[int]):
            if len(path) > max_length:
                return
            
            if current_id == end_id:
                paths.append(path[:])
                return
            
            for neighbor_id in self.nodes[current_id].connections:
                if neighbor_id not in path:  # Avoid cycles
                    path.append(neighbor_id)
                    find_paths_recursive(neighbor_id, path)
                    path.pop()
        
        find_paths_recursive(start_id, [start_id])
        return paths


def benchmark_small_graph_traversal(collector: MetricsCollector, iterations: int = 100):
    """Benchmark traversal on small graphs (100 nodes)."""
    graph = UniversalModuleGraph(100, connections_per_node=5)
    
    for i in range(iterations):
        with Timer(collector, "small_graph_bfs", "umg_reasoning"):
            start = random.randint(0, 99)
            target = random.randint(0, 99)
            path = graph.breadth_first_search(start, target)
            collector.record_custom_metric("path_length", len(path))


def benchmark_medium_graph_traversal(collector: MetricsCollector, iterations: int = 50):
    """Benchmark traversal on medium graphs (1,000 nodes)."""
    graph = UniversalModuleGraph(1000, connections_per_node=8)
    
    for i in range(iterations):
        with Timer(collector, "medium_graph_bfs", "umg_reasoning"):
            start = random.randint(0, 999)
            target = random.randint(0, 999)
            path = graph.breadth_first_search(start, target)
            collector.record_custom_metric("path_length", len(path))


def benchmark_large_graph_traversal(collector: MetricsCollector, iterations: int = 10):
    """Benchmark traversal on large graphs (10,000 nodes)."""
    graph = UniversalModuleGraph(10000, connections_per_node=10)
    
    for i in range(iterations):
        with Timer(collector, "large_graph_bfs", "umg_reasoning"):
            start = random.randint(0, 9999)
            target = random.randint(0, 9999)
            path = graph.breadth_first_search(start, target)
            collector.record_custom_metric("path_length", len(path))


def benchmark_depth_first_search(collector: MetricsCollector, iterations: int = 50):
    """Benchmark depth-first search performance."""
    graph = UniversalModuleGraph(1000, connections_per_node=8)
    
    for i in range(iterations):
        with Timer(collector, "dfs_exploration", "umg_reasoning"):
            start = random.randint(0, 999)
            visited = graph.depth_first_search(start, max_depth=15)
            collector.record_custom_metric("nodes_visited", len(visited))


def benchmark_all_paths_finding(collector: MetricsCollector, iterations: int = 20):
    """Benchmark finding all paths between nodes."""
    graph = UniversalModuleGraph(100, connections_per_node=5)
    
    for i in range(iterations):
        with Timer(collector, "all_paths", "umg_reasoning"):
            start = random.randint(0, 99)
            end = random.randint(0, 99)
            paths = graph.get_all_paths(start, end, max_length=5)
            collector.record_custom_metric("paths_found", len(paths))


def run_all_benchmarks(mode: str = "comprehensive"):
    """Run all module graph traversal benchmarks."""
    collector = MetricsCollector()
    
    iterations = {
        "quick": {"small": 10, "medium": 5, "large": 2, "dfs": 10, "paths": 5},
        "comprehensive": {"small": 100, "medium": 50, "large": 10, "dfs": 50, "paths": 20}
    }
    
    iters = iterations.get(mode, iterations["comprehensive"])
    
    print(f"Running UMG Graph Traversal Benchmarks (mode: {mode})...")
    
    print("  - Small graph BFS...")
    benchmark_small_graph_traversal(collector, iters["small"])
    
    print("  - Medium graph BFS...")
    benchmark_medium_graph_traversal(collector, iters["medium"])
    
    print("  - Large graph BFS...")
    benchmark_large_graph_traversal(collector, iters["large"])
    
    print("  - Depth-first search...")
    benchmark_depth_first_search(collector, iters["dfs"])
    
    print("  - All paths finding...")
    benchmark_all_paths_finding(collector, iters["paths"])
    
    return collector.get_all_results()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="UMG Graph Traversal Benchmarks")
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
            print(f"  Median time: {exec_time['median_ms']:.2f}ms")
        if 'memory' in summary:
            print(f"  Peak memory: {summary['memory']['peak_mb']:.2f}MB")
