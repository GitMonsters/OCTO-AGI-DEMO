"""
Tetrahedral Geometric Inference Benchmarks

Tests spatial reasoning quality including shape recognition, spatial relationship
inference, and geometric problem solving capabilities.
"""

import time
import random
import math
import sys
import os
from typing import List, Tuple, Dict, Set
from dataclasses import dataclass
from enum import Enum

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.metrics_collector import MetricsCollector, Timer


class ShapeType(Enum):
    """Enumeration of geometric shapes."""
    CIRCLE = "circle"
    SQUARE = "square"
    TRIANGLE = "triangle"
    RECTANGLE = "rectangle"
    POLYGON = "polygon"


@dataclass
class Point:
    """Represents a point in 2D/3D space."""
    x: float
    y: float
    z: float = 0.0
    
    def distance_to(self, other: 'Point') -> float:
        """Calculate Euclidean distance."""
        return math.sqrt(
            (self.x - other.x) ** 2 +
            (self.y - other.y) ** 2 +
            (self.z - other.z) ** 2
        )


@dataclass
class Shape:
    """Represents a geometric shape."""
    shape_type: ShapeType
    points: List[Point]
    center: Point = None
    
    def __post_init__(self):
        if self.center is None and self.points:
            self.center = Point(
                sum(p.x for p in self.points) / len(self.points),
                sum(p.y for p in self.points) / len(self.points),
                sum(p.z for p in self.points) / len(self.points)
            )


class ShapeRecognizer:
    """Recognizes geometric shapes from point sets."""
    
    @staticmethod
    def recognize_shape(points: List[Point]) -> ShapeType:
        """Recognize shape type from points."""
        if len(points) < 3:
            return ShapeType.POLYGON
        
        # Calculate centroid
        cx = sum(p.x for p in points) / len(points)
        cy = sum(p.y for p in points) / len(points)
        center = Point(cx, cy)
        
        # Check if points form a circle (equal distances from center)
        distances = [p.distance_to(center) for p in points]
        avg_dist = sum(distances) / len(distances)
        variance = sum((d - avg_dist) ** 2 for d in distances) / len(distances)
        
        if variance < 0.1 * avg_dist:
            return ShapeType.CIRCLE
        
        # Check for square/rectangle (4 points with right angles)
        if len(points) == 4:
            # Compute angles between consecutive sides
            angles = []
            for i in range(4):
                p1 = points[i]
                p2 = points[(i + 1) % 4]
                p3 = points[(i + 2) % 4]
                
                v1 = (p2.x - p1.x, p2.y - p1.y)
                v2 = (p3.x - p2.x, p3.y - p2.y)
                
                dot = v1[0] * v2[0] + v1[1] * v2[1]
                mag1 = math.sqrt(v1[0]**2 + v1[1]**2)
                mag2 = math.sqrt(v2[0]**2 + v2[1]**2)
                
                if mag1 > 0 and mag2 > 0:
                    angle = math.acos(max(-1, min(1, dot / (mag1 * mag2))))
                    angles.append(angle)
            
            # Check if all angles are approximately 90 degrees
            if angles and all(abs(a - math.pi/2) < 0.2 for a in angles):
                # Check if all sides are equal (square) or opposite sides equal (rectangle)
                sides = [points[i].distance_to(points[(i+1)%4]) for i in range(4)]
                if max(sides) - min(sides) < 0.1 * sum(sides) / 4:
                    return ShapeType.SQUARE
                return ShapeType.RECTANGLE
        
        # Check for triangle
        if len(points) == 3:
            return ShapeType.TRIANGLE
        
        return ShapeType.POLYGON
    
    @staticmethod
    def compute_shape_features(shape: Shape) -> Dict[str, float]:
        """Compute geometric features of a shape."""
        features = {}
        
        # Area (simplified)
        if len(shape.points) >= 3:
            area = 0.0
            for i in range(len(shape.points)):
                j = (i + 1) % len(shape.points)
                area += shape.points[i].x * shape.points[j].y
                area -= shape.points[j].x * shape.points[i].y
            features['area'] = abs(area) / 2.0
        
        # Perimeter
        perimeter = 0.0
        for i in range(len(shape.points)):
            j = (i + 1) % len(shape.points)
            perimeter += shape.points[i].distance_to(shape.points[j])
        features['perimeter'] = perimeter
        
        # Compactness
        if perimeter > 0:
            features['compactness'] = (4 * math.pi * features.get('area', 0)) / (perimeter ** 2)
        
        return features


class SpatialRelationshipInference:
    """Infers spatial relationships between shapes."""
    
    @staticmethod
    def is_inside(point: Point, shape: Shape) -> bool:
        """Check if point is inside shape using ray casting."""
        if len(shape.points) < 3:
            return False
        
        count = 0
        n = len(shape.points)
        
        for i in range(n):
            j = (i + 1) % n
            p1, p2 = shape.points[i], shape.points[j]
            
            if ((p1.y > point.y) != (p2.y > point.y)) and \
               (point.x < (p2.x - p1.x) * (point.y - p1.y) / (p2.y - p1.y) + p1.x):
                count += 1
        
        return count % 2 == 1
    
    @staticmethod
    def compute_overlap(shape1: Shape, shape2: Shape) -> float:
        """Compute overlap ratio between two shapes."""
        # Sample points in bounding box
        all_x = [p.x for p in shape1.points + shape2.points]
        all_y = [p.y for p in shape1.points + shape2.points]
        
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)
        
        samples = 100
        overlap_count = 0
        
        for _ in range(samples):
            test_point = Point(
                random.uniform(min_x, max_x),
                random.uniform(min_y, max_y)
            )
            
            in_shape1 = SpatialRelationshipInference.is_inside(test_point, shape1)
            in_shape2 = SpatialRelationshipInference.is_inside(test_point, shape2)
            
            if in_shape1 and in_shape2:
                overlap_count += 1
        
        return overlap_count / samples
    
    @staticmethod
    def are_adjacent(shape1: Shape, shape2: Shape, threshold: float = 5.0) -> bool:
        """Check if two shapes are adjacent."""
        min_distance = float('inf')
        
        for p1 in shape1.points:
            for p2 in shape2.points:
                dist = p1.distance_to(p2)
                min_distance = min(min_distance, dist)
        
        return min_distance < threshold
    
    @staticmethod
    def compute_relative_position(shape1: Shape, shape2: Shape) -> str:
        """Determine relative position (left, right, above, below)."""
        dx = shape2.center.x - shape1.center.x
        dy = shape2.center.y - shape1.center.y
        
        if abs(dx) > abs(dy):
            return "right" if dx > 0 else "left"
        else:
            return "above" if dy > 0 else "below"


class GeometricProblemSolver:
    """Solves geometric reasoning problems."""
    
    @staticmethod
    def find_closest_pair(shapes: List[Shape]) -> Tuple[int, int, float]:
        """Find the closest pair of shapes."""
        min_distance = float('inf')
        closest_pair = (0, 0)
        
        for i in range(len(shapes)):
            for j in range(i + 1, len(shapes)):
                dist = shapes[i].center.distance_to(shapes[j].center)
                if dist < min_distance:
                    min_distance = dist
                    closest_pair = (i, j)
        
        return closest_pair[0], closest_pair[1], min_distance
    
    @staticmethod
    def find_convex_hull(points: List[Point]) -> List[Point]:
        """Find convex hull using Graham scan (simplified)."""
        if len(points) < 3:
            return points
        
        # Find point with lowest y-coordinate
        start = min(points, key=lambda p: (p.y, p.x))
        
        # Sort points by polar angle
        def polar_angle(p):
            dx = p.x - start.x
            dy = p.y - start.y
            return math.atan2(dy, dx)
        
        sorted_points = sorted([p for p in points if p != start], key=polar_angle)
        
        # Build hull
        hull = [start]
        for p in sorted_points:
            while len(hull) > 1:
                # Check if we turn right or left
                o = hull[-2]
                a = hull[-1]
                cross = (a.x - o.x) * (p.y - o.y) - (a.y - o.y) * (p.x - o.x)
                if cross > 0:
                    break
                hull.pop()
            hull.append(p)
        
        return hull
    
    @staticmethod
    def compute_minimum_bounding_box(points: List[Point]) -> Tuple[Point, Point]:
        """Compute axis-aligned minimum bounding box."""
        if not points:
            return Point(0, 0), Point(0, 0)
        
        min_x = min(p.x for p in points)
        max_x = max(p.x for p in points)
        min_y = min(p.y for p in points)
        max_y = max(p.y for p in points)
        
        return Point(min_x, min_y), Point(max_x, max_y)


def generate_random_shape(shape_type: ShapeType = None, size: float = 20.0) -> Shape:
    """Generate a random geometric shape."""
    if shape_type is None:
        shape_type = random.choice(list(ShapeType))
    
    center_x = random.uniform(-50, 50)
    center_y = random.uniform(-50, 50)
    
    if shape_type == ShapeType.CIRCLE:
        # Generate points on a circle
        num_points = 12
        points = []
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            points.append(Point(
                center_x + size * math.cos(angle),
                center_y + size * math.sin(angle)
            ))
    elif shape_type == ShapeType.SQUARE:
        half = size / 2
        points = [
            Point(center_x - half, center_y - half),
            Point(center_x + half, center_y - half),
            Point(center_x + half, center_y + half),
            Point(center_x - half, center_y + half)
        ]
    elif shape_type == ShapeType.TRIANGLE:
        points = [
            Point(center_x, center_y + size),
            Point(center_x - size, center_y - size),
            Point(center_x + size, center_y - size)
        ]
    else:
        # Random polygon
        num_points = random.randint(5, 8)
        points = []
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points + random.uniform(-0.3, 0.3)
            r = size * random.uniform(0.8, 1.2)
            points.append(Point(
                center_x + r * math.cos(angle),
                center_y + r * math.sin(angle)
            ))
    
    return Shape(shape_type, points)


def benchmark_shape_recognition(collector: MetricsCollector, iterations: int = 100):
    """Benchmark shape recognition accuracy and speed."""
    shape_types = [ShapeType.CIRCLE, ShapeType.SQUARE, ShapeType.TRIANGLE]
    
    for _ in range(iterations):
        # Generate a shape
        expected_type = random.choice(shape_types)
        shape = generate_random_shape(expected_type)
        
        with Timer(collector, "shape_recognition", "tetrahedral_spatial"):
            recognized_type = ShapeRecognizer.recognize_shape(shape.points)
            correct = (recognized_type == expected_type)
            
            collector.record_custom_metric("recognition_accuracy", 1.0 if correct else 0.0)
            collector.record_custom_metric("shape_complexity", len(shape.points))


def benchmark_spatial_relationship_inference(collector: MetricsCollector, iterations: int = 50):
    """Benchmark spatial relationship inference."""
    
    for _ in range(iterations):
        shape1 = generate_random_shape()
        shape2 = generate_random_shape()
        
        with Timer(collector, "spatial_relationship", "tetrahedral_spatial"):
            overlap = SpatialRelationshipInference.compute_overlap(shape1, shape2)
            adjacent = SpatialRelationshipInference.are_adjacent(shape1, shape2)
            position = SpatialRelationshipInference.compute_relative_position(shape1, shape2)
            
            collector.record_custom_metric("overlap_ratio", overlap)
            collector.record_custom_metric("adjacency_detected", 1.0 if adjacent else 0.0)


def benchmark_containment_testing(collector: MetricsCollector, iterations: int = 100):
    """Benchmark point-in-polygon containment testing."""
    
    for _ in range(iterations):
        shape = generate_random_shape()
        test_point = Point(random.uniform(-100, 100), random.uniform(-100, 100))
        
        with Timer(collector, "containment_test", "tetrahedral_spatial"):
            is_inside = SpatialRelationshipInference.is_inside(test_point, shape)
            
            collector.record_custom_metric("containment_result", 1.0 if is_inside else 0.0)
            collector.record_custom_metric("polygon_vertices", len(shape.points))


def benchmark_feature_extraction(collector: MetricsCollector, iterations: int = 100):
    """Benchmark geometric feature extraction."""
    
    for _ in range(iterations):
        shape = generate_random_shape()
        
        with Timer(collector, "feature_extraction", "tetrahedral_spatial"):
            features = ShapeRecognizer.compute_shape_features(shape)
            
            collector.record_custom_metric("features_extracted", len(features))
            if 'area' in features:
                collector.record_custom_metric("shape_area", features['area'])


def benchmark_closest_pair_finding(collector: MetricsCollector, iterations: int = 30):
    """Benchmark finding closest pair of shapes."""
    shape_counts = [5, 10, 20]
    
    for count in shape_counts:
        for _ in range(iterations):
            shapes = [generate_random_shape() for _ in range(count)]
            
            with Timer(collector, f"closest_pair_{count}", "tetrahedral_spatial"):
                i, j, distance = GeometricProblemSolver.find_closest_pair(shapes)
                
                collector.record_custom_metric("shape_count", count)
                collector.record_custom_metric("min_distance", distance)


def benchmark_convex_hull(collector: MetricsCollector, iterations: int = 50):
    """Benchmark convex hull computation."""
    point_counts = [10, 50, 100]
    
    for count in point_counts:
        for _ in range(iterations):
            points = [Point(random.uniform(-100, 100), random.uniform(-100, 100))
                     for _ in range(count)]
            
            with Timer(collector, f"convex_hull_{count}", "tetrahedral_spatial"):
                hull = GeometricProblemSolver.find_convex_hull(points)
                
                collector.record_custom_metric("input_points", count)
                collector.record_custom_metric("hull_vertices", len(hull))


def benchmark_bounding_box(collector: MetricsCollector, iterations: int = 100):
    """Benchmark minimum bounding box computation."""
    
    for _ in range(iterations):
        num_points = random.randint(10, 100)
        points = [Point(random.uniform(-100, 100), random.uniform(-100, 100))
                 for _ in range(num_points)]
        
        with Timer(collector, "bounding_box", "tetrahedral_spatial"):
            min_corner, max_corner = GeometricProblemSolver.compute_minimum_bounding_box(points)
            area = (max_corner.x - min_corner.x) * (max_corner.y - min_corner.y)
            
            collector.record_custom_metric("box_area", area)
            collector.record_custom_metric("points_bounded", num_points)


def run_all_benchmarks(mode: str = "comprehensive"):
    """Run all geometric inference benchmarks."""
    collector = MetricsCollector()
    
    iterations = {
        "quick": {
            "recognition": 20, "relationship": 10, "containment": 20,
            "features": 20, "closest_pair": 5, "convex_hull": 10, "bbox": 20
        },
        "comprehensive": {
            "recognition": 100, "relationship": 50, "containment": 100,
            "features": 100, "closest_pair": 30, "convex_hull": 50, "bbox": 100
        }
    }
    
    iters = iterations.get(mode, iterations["comprehensive"])
    
    print(f"Running Tetrahedral Geometric Inference Benchmarks (mode: {mode})...")
    
    print("  - Shape recognition...")
    benchmark_shape_recognition(collector, iters["recognition"])
    
    print("  - Spatial relationship inference...")
    benchmark_spatial_relationship_inference(collector, iters["relationship"])
    
    print("  - Containment testing...")
    benchmark_containment_testing(collector, iters["containment"])
    
    print("  - Feature extraction...")
    benchmark_feature_extraction(collector, iters["features"])
    
    print("  - Closest pair finding...")
    benchmark_closest_pair_finding(collector, iters["closest_pair"])
    
    print("  - Convex hull computation...")
    benchmark_convex_hull(collector, iters["convex_hull"])
    
    print("  - Bounding box computation...")
    benchmark_bounding_box(collector, iters["bbox"])
    
    return collector.get_all_results()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Tetrahedral Geometric Inference Benchmarks")
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
                if 'accuracy' in metric_name:
                    print(f"  {metric_name}: {metric_data['mean']:.4f}")
