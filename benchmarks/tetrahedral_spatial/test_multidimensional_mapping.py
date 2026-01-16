"""
Tetrahedral Multidimensional Mapping Benchmarks

Tests the accuracy and performance of relationship mapping across dimensions,
including 2D to 3D, 3D to 4D transformations, and relationship preservation.
"""

import time
import random
import math
import sys
import os
from typing import List, Tuple, Dict
from dataclasses import dataclass

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.metrics_collector import MetricsCollector, Timer


@dataclass
class Point2D:
    """Represents a point in 2D space."""
    x: float
    y: float
    
    def to_3d(self, z: float = 0.0) -> 'Point3D':
        """Map 2D point to 3D space."""
        return Point3D(self.x, self.y, z)


@dataclass
class Point3D:
    """Represents a point in 3D space."""
    x: float
    y: float
    z: float
    
    def distance_to(self, other: 'Point3D') -> float:
        """Calculate Euclidean distance."""
        return math.sqrt(
            (self.x - other.x) ** 2 +
            (self.y - other.y) ** 2 +
            (self.z - other.z) ** 2
        )
    
    def to_4d(self, w: float = 0.0) -> 'Point4D':
        """Map 3D point to 4D space."""
        return Point4D(self.x, self.y, self.z, w)


@dataclass
class Point4D:
    """Represents a point in 4D space."""
    x: float
    y: float
    z: float
    w: float
    
    def distance_to(self, other: 'Point4D') -> float:
        """Calculate Euclidean distance in 4D."""
        return math.sqrt(
            (self.x - other.x) ** 2 +
            (self.y - other.y) ** 2 +
            (self.z - other.z) ** 2 +
            (self.w - other.w) ** 2
        )


class DimensionalMapper:
    """Handles mapping between different dimensional spaces."""
    
    @staticmethod
    def map_2d_to_3d(points_2d: List[Point2D], elevation_func=None) -> List[Point3D]:
        """Map 2D points to 3D space with optional elevation function."""
        if elevation_func is None:
            elevation_func = lambda p: math.sin(p.x * 0.1) * math.cos(p.y * 0.1) * 10
        
        return [p.to_3d(elevation_func(p)) for p in points_2d]
    
    @staticmethod
    def map_3d_to_4d(points_3d: List[Point3D], temporal_func=None) -> List[Point4D]:
        """Map 3D points to 4D space with optional temporal dimension."""
        if temporal_func is None:
            temporal_func = lambda p: (p.x + p.y + p.z) / 3.0
        
        return [p.to_4d(temporal_func(p)) for p in points_3d]
    
    @staticmethod
    def preserve_distances_2d_to_3d(points_2d: List[Point2D], points_3d: List[Point3D]) -> float:
        """Calculate distance preservation ratio in 2D to 3D mapping."""
        if len(points_2d) < 2 or len(points_3d) < 2:
            return 0.0
        
        # Sample pairs for efficiency
        num_samples = min(100, len(points_2d) * (len(points_2d) - 1) // 2)
        total_ratio = 0.0
        
        for _ in range(num_samples):
            i, j = random.sample(range(len(points_2d)), 2)
            
            # 2D distance
            dist_2d = math.sqrt(
                (points_2d[i].x - points_2d[j].x) ** 2 +
                (points_2d[i].y - points_2d[j].y) ** 2
            )
            
            # 3D distance (only xy plane)
            dist_3d_xy = math.sqrt(
                (points_3d[i].x - points_3d[j].x) ** 2 +
                (points_3d[i].y - points_3d[j].y) ** 2
            )
            
            if dist_2d > 0:
                total_ratio += abs(dist_3d_xy - dist_2d) / dist_2d
        
        return 1.0 - (total_ratio / num_samples)
    
    @staticmethod
    def preserve_distances_3d_to_4d(points_3d: List[Point3D], points_4d: List[Point4D]) -> float:
        """Calculate distance preservation ratio in 3D to 4D mapping."""
        if len(points_3d) < 2 or len(points_4d) < 2:
            return 0.0
        
        num_samples = min(100, len(points_3d) * (len(points_3d) - 1) // 2)
        total_ratio = 0.0
        
        for _ in range(num_samples):
            i, j = random.sample(range(len(points_3d)), 2)
            
            dist_3d = points_3d[i].distance_to(points_3d[j])
            
            # 4D distance (only xyz subspace)
            dist_4d_xyz = math.sqrt(
                (points_4d[i].x - points_4d[j].x) ** 2 +
                (points_4d[i].y - points_4d[j].y) ** 2 +
                (points_4d[i].z - points_4d[j].z) ** 2
            )
            
            if dist_3d > 0:
                total_ratio += abs(dist_4d_xyz - dist_3d) / dist_3d
        
        return 1.0 - (total_ratio / num_samples)


class RelationshipAnalyzer:
    """Analyzes spatial relationships across dimensions."""
    
    @staticmethod
    def compute_topology_preservation(source_points, mapped_points, dim: str) -> float:
        """Compute how well topology is preserved during mapping."""
        if len(source_points) < 3:
            return 0.0
        
        # Check if nearest neighbors are preserved
        preserved_count = 0
        total_checks = min(50, len(source_points))
        
        for _ in range(total_checks):
            idx = random.randint(0, len(source_points) - 1)
            
            # Find nearest in source
            if dim == "2d":
                distances = [(i, math.sqrt((source_points[idx].x - p.x)**2 + 
                                          (source_points[idx].y - p.y)**2))
                            for i, p in enumerate(source_points) if i != idx]
            else:
                distances = [(i, source_points[idx].distance_to(p))
                            for i, p in enumerate(source_points) if i != idx]
            
            distances.sort(key=lambda x: x[1])
            source_nearest = distances[0][0]
            
            # Find nearest in mapped
            mapped_distances = [(i, mapped_points[idx].distance_to(p))
                               for i, p in enumerate(mapped_points) if i != idx]
            mapped_distances.sort(key=lambda x: x[1])
            mapped_nearest = mapped_distances[0][0]
            
            if source_nearest == mapped_nearest:
                preserved_count += 1
        
        return preserved_count / total_checks if total_checks > 0 else 0.0


def benchmark_2d_to_3d_mapping(collector: MetricsCollector, iterations: int = 50):
    """Benchmark 2D to 3D mapping accuracy and performance."""
    sizes = [100, 500, 1000]
    
    for size in sizes:
        for i in range(iterations):
            # Generate 2D points
            points_2d = [Point2D(random.uniform(-100, 100), random.uniform(-100, 100))
                        for _ in range(size)]
            
            with Timer(collector, f"2d_to_3d_mapping_{size}", "tetrahedral_spatial"):
                points_3d = DimensionalMapper.map_2d_to_3d(points_2d)
                accuracy = DimensionalMapper.preserve_distances_2d_to_3d(points_2d, points_3d)
                
                collector.record_custom_metric("mapping_accuracy", accuracy)
                collector.record_custom_metric("points_mapped", size)


def benchmark_3d_to_4d_mapping(collector: MetricsCollector, iterations: int = 50):
    """Benchmark 3D to 4D mapping accuracy and performance."""
    sizes = [100, 500, 1000]
    
    for size in sizes:
        for i in range(iterations):
            # Generate 3D points
            points_3d = [Point3D(random.uniform(-100, 100), 
                                random.uniform(-100, 100),
                                random.uniform(-100, 100))
                        for _ in range(size)]
            
            with Timer(collector, f"3d_to_4d_mapping_{size}", "tetrahedral_spatial"):
                points_4d = DimensionalMapper.map_3d_to_4d(points_3d)
                accuracy = DimensionalMapper.preserve_distances_3d_to_4d(points_3d, points_4d)
                
                collector.record_custom_metric("mapping_accuracy", accuracy)
                collector.record_custom_metric("points_mapped", size)


def benchmark_relationship_preservation_2d_3d(collector: MetricsCollector, iterations: int = 30):
    """Benchmark relationship preservation in 2D to 3D mapping."""
    size = 500
    
    for i in range(iterations):
        points_2d = [Point2D(random.uniform(-100, 100), random.uniform(-100, 100))
                    for _ in range(size)]
        
        with Timer(collector, "relationship_preservation_2d_3d", "tetrahedral_spatial"):
            points_3d = DimensionalMapper.map_2d_to_3d(points_2d)
            topology_score = RelationshipAnalyzer.compute_topology_preservation(
                points_2d, points_3d, "2d"
            )
            
            collector.record_custom_metric("topology_preservation", topology_score)
            collector.record_custom_metric("relationship_count", size)


def benchmark_relationship_preservation_3d_4d(collector: MetricsCollector, iterations: int = 30):
    """Benchmark relationship preservation in 3D to 4D mapping."""
    size = 500
    
    for i in range(iterations):
        points_3d = [Point3D(random.uniform(-100, 100),
                            random.uniform(-100, 100),
                            random.uniform(-100, 100))
                    for _ in range(size)]
        
        with Timer(collector, "relationship_preservation_3d_4d", "tetrahedral_spatial"):
            points_4d = DimensionalMapper.map_3d_to_4d(points_3d)
            topology_score = RelationshipAnalyzer.compute_topology_preservation(
                points_3d, points_4d, "3d"
            )
            
            collector.record_custom_metric("topology_preservation", topology_score)
            collector.record_custom_metric("relationship_count", size)


def benchmark_bidirectional_consistency(collector: MetricsCollector, iterations: int = 30):
    """Benchmark consistency of forward and inverse mappings."""
    size = 200
    
    for i in range(iterations):
        points_2d = [Point2D(random.uniform(-100, 100), random.uniform(-100, 100))
                    for _ in range(size)]
        
        with Timer(collector, "bidirectional_consistency", "tetrahedral_spatial"):
            # Forward: 2D -> 3D
            points_3d = DimensionalMapper.map_2d_to_3d(points_2d)
            
            # Simple inverse: project back to 2D
            points_2d_recovered = [Point2D(p.x, p.y) for p in points_3d]
            
            # Measure reconstruction error
            total_error = 0.0
            for orig, recovered in zip(points_2d, points_2d_recovered):
                error = math.sqrt((orig.x - recovered.x)**2 + (orig.y - recovered.y)**2)
                total_error += error
            
            avg_error = total_error / size
            consistency = 1.0 / (1.0 + avg_error)
            
            collector.record_custom_metric("consistency_score", consistency)
            collector.record_custom_metric("reconstruction_error", avg_error)


def benchmark_multiscale_mapping(collector: MetricsCollector, iterations: int = 20):
    """Benchmark mapping at multiple scales."""
    scales = [10, 50, 100, 500, 1000]
    
    for scale in scales:
        for i in range(iterations):
            points_2d = [Point2D(random.uniform(-100, 100), random.uniform(-100, 100))
                        for _ in range(scale)]
            
            with Timer(collector, f"multiscale_mapping_{scale}", "tetrahedral_spatial"):
                points_3d = DimensionalMapper.map_2d_to_3d(points_2d)
                points_4d = DimensionalMapper.map_3d_to_4d(points_3d)
                
                collector.record_custom_metric("scale", scale)
                collector.record_custom_metric("dimensions_traversed", 2)


def benchmark_adaptive_mapping(collector: MetricsCollector, iterations: int = 30):
    """Benchmark adaptive mapping with dynamic elevation functions."""
    size = 500
    
    elevation_functions = [
        lambda p: math.sin(p.x * 0.1) * math.cos(p.y * 0.1) * 10,
        lambda p: (p.x ** 2 + p.y ** 2) ** 0.5 * 0.1,
        lambda p: math.atan2(p.y, p.x) * 5,
    ]
    
    for i in range(iterations):
        points_2d = [Point2D(random.uniform(-100, 100), random.uniform(-100, 100))
                    for _ in range(size)]
        
        func = elevation_functions[i % len(elevation_functions)]
        
        with Timer(collector, "adaptive_mapping", "tetrahedral_spatial"):
            points_3d = DimensionalMapper.map_2d_to_3d(points_2d, func)
            accuracy = DimensionalMapper.preserve_distances_2d_to_3d(points_2d, points_3d)
            
            collector.record_custom_metric("adaptive_accuracy", accuracy)
            collector.record_custom_metric("function_type", i % len(elevation_functions))


def run_all_benchmarks(mode: str = "comprehensive"):
    """Run all multidimensional mapping benchmarks."""
    collector = MetricsCollector()
    
    iterations = {
        "quick": {
            "2d_3d": 10, "3d_4d": 10, "rel_2d_3d": 5, "rel_3d_4d": 5,
            "bidir": 5, "multiscale": 5, "adaptive": 10
        },
        "comprehensive": {
            "2d_3d": 50, "3d_4d": 50, "rel_2d_3d": 30, "rel_3d_4d": 30,
            "bidir": 30, "multiscale": 20, "adaptive": 30
        }
    }
    
    iters = iterations.get(mode, iterations["comprehensive"])
    
    print(f"Running Tetrahedral Multidimensional Mapping Benchmarks (mode: {mode})...")
    
    print("  - 2D to 3D mapping...")
    benchmark_2d_to_3d_mapping(collector, iters["2d_3d"])
    
    print("  - 3D to 4D mapping...")
    benchmark_3d_to_4d_mapping(collector, iters["3d_4d"])
    
    print("  - Relationship preservation (2D-3D)...")
    benchmark_relationship_preservation_2d_3d(collector, iters["rel_2d_3d"])
    
    print("  - Relationship preservation (3D-4D)...")
    benchmark_relationship_preservation_3d_4d(collector, iters["rel_3d_4d"])
    
    print("  - Bidirectional consistency...")
    benchmark_bidirectional_consistency(collector, iters["bidir"])
    
    print("  - Multiscale mapping...")
    benchmark_multiscale_mapping(collector, iters["multiscale"])
    
    print("  - Adaptive mapping...")
    benchmark_adaptive_mapping(collector, iters["adaptive"])
    
    return collector.get_all_results()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Tetrahedral Multidimensional Mapping Benchmarks")
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
        if 'custom_metrics' in summary:
            for metric_name, metric_data in summary['custom_metrics'].items():
                if 'accuracy' in metric_name or 'preservation' in metric_name or 'consistency' in metric_name:
                    print(f"  {metric_name}: {metric_data['mean']:.4f}")
