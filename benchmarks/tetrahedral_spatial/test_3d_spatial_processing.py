"""
Tetrahedral 3D Spatial Processing Benchmarks

Tests the speed of 3D computational operations including point cloud processing,
volumetric calculations, and spatial transformations.
"""

import time
import random
import math
import sys
import os
from typing import List, Tuple
from dataclasses import dataclass

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.metrics_collector import MetricsCollector, Timer


@dataclass
class Point3D:
    """Represents a point in 3D space."""
    x: float
    y: float
    z: float
    
    def distance_to(self, other: 'Point3D') -> float:
        """Calculate Euclidean distance to another point."""
        return math.sqrt(
            (self.x - other.x) ** 2 +
            (self.y - other.y) ** 2 +
            (self.z - other.z) ** 2
        )
    
    def transform(self, matrix: List[List[float]]) -> 'Point3D':
        """Apply transformation matrix."""
        if len(matrix) != 3 or any(len(row) != 3 for row in matrix):
            return self
        
        new_x = matrix[0][0] * self.x + matrix[0][1] * self.y + matrix[0][2] * self.z
        new_y = matrix[1][0] * self.x + matrix[1][1] * self.y + matrix[1][2] * self.z
        new_z = matrix[2][0] * self.x + matrix[2][1] * self.y + matrix[2][2] * self.z
        
        return Point3D(new_x, new_y, new_z)


class PointCloud:
    """Represents a 3D point cloud."""
    
    def __init__(self, num_points: int):
        self.points: List[Point3D] = []
        self._generate_points(num_points)
    
    def _generate_points(self, num_points: int):
        """Generate random 3D points."""
        for _ in range(num_points):
            self.points.append(Point3D(
                random.uniform(-100, 100),
                random.uniform(-100, 100),
                random.uniform(-100, 100)
            ))
    
    def find_nearest_neighbor(self, query_point: Point3D) -> Tuple[Point3D, float]:
        """Find the nearest neighbor to a query point."""
        if not self.points:
            return query_point, float('inf')
        
        nearest = self.points[0]
        min_distance = query_point.distance_to(nearest)
        
        for point in self.points[1:]:
            distance = query_point.distance_to(point)
            if distance < min_distance:
                min_distance = distance
                nearest = point
        
        return nearest, min_distance
    
    def find_k_nearest(self, query_point: Point3D, k: int) -> List[Tuple[Point3D, float]]:
        """Find k nearest neighbors."""
        distances = [(point, query_point.distance_to(point)) for point in self.points]
        distances.sort(key=lambda x: x[1])
        return distances[:k]
    
    def compute_centroid(self) -> Point3D:
        """Compute the centroid of the point cloud."""
        if not self.points:
            return Point3D(0, 0, 0)
        
        sum_x = sum(p.x for p in self.points)
        sum_y = sum(p.y for p in self.points)
        sum_z = sum(p.z for p in self.points)
        
        n = len(self.points)
        return Point3D(sum_x / n, sum_y / n, sum_z / n)
    
    def apply_transformation(self, matrix: List[List[float]]):
        """Apply transformation to all points."""
        self.points = [point.transform(matrix) for point in self.points]
    
    def filter_by_distance(self, center: Point3D, max_distance: float) -> List[Point3D]:
        """Filter points within a certain distance from center."""
        return [p for p in self.points if p.distance_to(center) <= max_distance]


def create_rotation_matrix(angle_x: float, angle_y: float, angle_z: float) -> List[List[float]]:
    """Create a 3D rotation matrix."""
    # Simplified rotation matrix
    cos_x, sin_x = math.cos(angle_x), math.sin(angle_x)
    cos_y, sin_y = math.cos(angle_y), math.sin(angle_y)
    cos_z, sin_z = math.cos(angle_z), math.sin(angle_z)
    
    return [
        [cos_y * cos_z, -cos_y * sin_z, sin_y],
        [sin_x * sin_y * cos_z + cos_x * sin_z, -sin_x * sin_y * sin_z + cos_x * cos_z, -sin_x * cos_y],
        [-cos_x * sin_y * cos_z + sin_x * sin_z, cos_x * sin_y * sin_z + sin_x * cos_z, cos_x * cos_y]
    ]


def benchmark_point_cloud_generation(collector: MetricsCollector, iterations: int = 50):
    """Benchmark point cloud generation."""
    sizes = [100, 500, 1000]
    
    for size in sizes:
        for i in range(iterations):
            with Timer(collector, f"point_cloud_gen_{size}", "tetrahedral_spatial"):
                cloud = PointCloud(size)
                collector.record_custom_metric("points_generated", len(cloud.points))


def benchmark_nearest_neighbor_search(collector: MetricsCollector, iterations: int = 50):
    """Benchmark nearest neighbor search."""
    cloud = PointCloud(1000)
    
    for i in range(iterations):
        query = Point3D(random.uniform(-100, 100), random.uniform(-100, 100), random.uniform(-100, 100))
        
        with Timer(collector, "nearest_neighbor_search", "tetrahedral_spatial"):
            nearest, distance = cloud.find_nearest_neighbor(query)
            collector.record_custom_metric("search_distance", distance)


def benchmark_k_nearest_neighbors(collector: MetricsCollector, iterations: int = 30):
    """Benchmark k-nearest neighbors search."""
    cloud = PointCloud(1000)
    k_values = [5, 10, 20]
    
    for k in k_values:
        for i in range(iterations):
            query = Point3D(random.uniform(-100, 100), random.uniform(-100, 100), random.uniform(-100, 100))
            
            with Timer(collector, f"k_nearest_{k}", "tetrahedral_spatial"):
                neighbors = cloud.find_k_nearest(query, k)
                collector.record_custom_metric("k_value", k)
                collector.record_custom_metric("neighbors_found", len(neighbors))


def benchmark_centroid_calculation(collector: MetricsCollector, iterations: int = 100):
    """Benchmark centroid calculation."""
    clouds = [PointCloud(size) for size in [100, 500, 1000]]
    
    for cloud in clouds:
        for i in range(iterations):
            with Timer(collector, f"centroid_calc_{len(cloud.points)}", "tetrahedral_spatial"):
                centroid = cloud.compute_centroid()
                collector.record_custom_metric("cloud_size", len(cloud.points))


def benchmark_spatial_transformation(collector: MetricsCollector, iterations: int = 30):
    """Benchmark spatial transformations."""
    cloud = PointCloud(1000)
    
    for i in range(iterations):
        angle_x = random.uniform(0, 2 * math.pi)
        angle_y = random.uniform(0, 2 * math.pi)
        angle_z = random.uniform(0, 2 * math.pi)
        
        with Timer(collector, "spatial_transformation", "tetrahedral_spatial"):
            matrix = create_rotation_matrix(angle_x, angle_y, angle_z)
            # Create a copy to avoid modifying original
            temp_cloud = PointCloud(0)
            temp_cloud.points = [p.transform(matrix) for p in cloud.points]
            collector.record_custom_metric("points_transformed", len(temp_cloud.points))


def benchmark_volumetric_calculations(collector: MetricsCollector, iterations: int = 50):
    """Benchmark volumetric calculations."""
    cloud = PointCloud(1000)
    
    for i in range(iterations):
        with Timer(collector, "volumetric_calc", "tetrahedral_spatial"):
            centroid = cloud.compute_centroid()
            # Calculate bounding box volume
            min_x = min(p.x for p in cloud.points)
            max_x = max(p.x for p in cloud.points)
            min_y = min(p.y for p in cloud.points)
            max_y = max(p.y for p in cloud.points)
            min_z = min(p.z for p in cloud.points)
            max_z = max(p.z for p in cloud.points)
            
            volume = (max_x - min_x) * (max_y - min_y) * (max_z - min_z)
            collector.record_custom_metric("bounding_volume", volume)


def benchmark_spatial_filtering(collector: MetricsCollector, iterations: int = 50):
    """Benchmark spatial filtering operations."""
    cloud = PointCloud(1000)
    
    for i in range(iterations):
        center = Point3D(0, 0, 0)
        max_distance = random.uniform(20, 80)
        
        with Timer(collector, "spatial_filtering", "tetrahedral_spatial"):
            filtered = cloud.filter_by_distance(center, max_distance)
            collector.record_custom_metric("points_filtered", len(filtered))
            collector.record_custom_metric("filter_ratio", len(filtered) / len(cloud.points))


def run_all_benchmarks(mode: str = "comprehensive"):
    """Run all 3D spatial processing benchmarks."""
    collector = MetricsCollector()
    
    iterations = {
        "quick": {"gen": 10, "nn": 10, "knn": 5, "centroid": 20, "transform": 5, "volume": 10, "filter": 10},
        "comprehensive": {"gen": 50, "nn": 50, "knn": 30, "centroid": 100, "transform": 30, "volume": 50, "filter": 50}
    }
    
    iters = iterations.get(mode, iterations["comprehensive"])
    
    print(f"Running Tetrahedral 3D Spatial Processing Benchmarks (mode: {mode})...")
    
    print("  - Point cloud generation...")
    benchmark_point_cloud_generation(collector, iters["gen"])
    
    print("  - Nearest neighbor search...")
    benchmark_nearest_neighbor_search(collector, iters["nn"])
    
    print("  - K-nearest neighbors...")
    benchmark_k_nearest_neighbors(collector, iters["knn"])
    
    print("  - Centroid calculation...")
    benchmark_centroid_calculation(collector, iters["centroid"])
    
    print("  - Spatial transformation...")
    benchmark_spatial_transformation(collector, iters["transform"])
    
    print("  - Volumetric calculations...")
    benchmark_volumetric_calculations(collector, iters["volume"])
    
    print("  - Spatial filtering...")
    benchmark_spatial_filtering(collector, iters["filter"])
    
    return collector.get_all_results()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Tetrahedral 3D Spatial Processing Benchmarks")
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
