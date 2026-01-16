"""
Deschooling Creative Problem Solving Benchmarks

Tests novel solution generation including solution count, novelty score,
and quality metrics for open-ended problems, constraint-based problems,
and multi-solution problems.
"""

import time
import random
import math
import sys
import os
from typing import List, Dict, Set, Tuple, Any, Optional
from dataclasses import dataclass, field

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.metrics_collector import MetricsCollector, Timer


@dataclass
class Problem:
    """Represents a problem to be solved."""
    problem_id: str
    description: str
    constraints: List[str]
    target_solutions: int
    complexity: float


@dataclass
class Solution:
    """Represents a solution to a problem."""
    solution_id: str
    problem_id: str
    approach: str
    components: List[Any]
    quality_score: float = 0.0
    novelty_score: float = 0.0
    
    def calculate_quality(self, problem: Problem) -> float:
        """Calculate solution quality based on problem constraints."""
        base_quality = len(self.components) / (len(self.components) + 1)
        
        # Check constraint satisfaction
        constraint_score = 1.0
        for constraint in problem.constraints:
            if random.random() > 0.7:  # Simulate constraint checking
                constraint_score *= 0.9
        
        self.quality_score = base_quality * constraint_score
        return self.quality_score
    
    def calculate_novelty(self, existing_solutions: List['Solution']) -> float:
        """Calculate novelty compared to existing solutions."""
        if not existing_solutions:
            self.novelty_score = 1.0
            return 1.0
        
        # Calculate similarity to existing solutions
        total_similarity = 0.0
        for existing in existing_solutions:
            if existing.approach == self.approach:
                total_similarity += 0.5
            
            # Component overlap
            overlap = len(set(map(str, self.components)) & set(map(str, existing.components)))
            total_similarity += overlap / max(len(self.components), len(existing.components))
        
        avg_similarity = total_similarity / len(existing_solutions)
        self.novelty_score = 1.0 - min(1.0, avg_similarity)
        return self.novelty_score


class CreativeProblemSolver:
    """Simulates a creative problem-solving system."""
    
    def __init__(self):
        self.solution_history: Dict[str, List[Solution]] = {}
        self.approaches = [
            'analytical', 'creative', 'systematic', 'intuitive', 
            'experimental', 'combinatorial', 'reductive', 'expansive'
        ]
        self.component_library = self._build_component_library()
    
    def _build_component_library(self) -> Dict[str, List[Any]]:
        """Build a library of solution components."""
        return {
            'numeric': list(range(1, 100)),
            'logical': ['AND', 'OR', 'NOT', 'XOR', 'IMPLIES'],
            'structural': ['sequence', 'tree', 'graph', 'matrix', 'stack', 'queue'],
            'algorithmic': ['divide_conquer', 'dynamic_prog', 'greedy', 'backtrack'],
            'patterns': ['singleton', 'factory', 'observer', 'strategy', 'composite']
        }
    
    def generate_solution(self, problem: Problem, approach: Optional[str] = None) -> Solution:
        """Generate a single solution for a problem."""
        if approach is None:
            approach = random.choice(self.approaches)
        
        # Select components based on approach and complexity
        num_components = int(3 + problem.complexity * 3)
        components = []
        
        for _ in range(num_components):
            category = random.choice(list(self.component_library.keys()))
            component = random.choice(self.component_library[category])
            components.append(component)
        
        solution = Solution(
            solution_id=f"sol_{problem.problem_id}_{len(self.solution_history.get(problem.problem_id, []))}",
            problem_id=problem.problem_id,
            approach=approach,
            components=components
        )
        
        # Calculate quality and novelty
        existing_solutions = self.solution_history.get(problem.problem_id, [])
        solution.calculate_quality(problem)
        solution.calculate_novelty(existing_solutions)
        
        return solution
    
    def solve_problem(self, problem: Problem, num_solutions: int = 1) -> List[Solution]:
        """Generate multiple solutions for a problem."""
        solutions = []
        
        if problem.problem_id not in self.solution_history:
            self.solution_history[problem.problem_id] = []
        
        for i in range(num_solutions):
            # Use different approaches for variety
            approach = self.approaches[i % len(self.approaches)]
            solution = self.generate_solution(problem, approach)
            solutions.append(solution)
            self.solution_history[problem.problem_id].append(solution)
        
        return solutions
    
    def generate_novel_solution(self, problem: Problem, min_novelty: float = 0.7) -> Optional[Solution]:
        """Generate a solution with minimum novelty threshold."""
        max_attempts = 20
        
        for attempt in range(max_attempts):
            solution = self.generate_solution(problem)
            
            if solution.novelty_score >= min_novelty:
                self.solution_history[problem.problem_id].append(solution)
                return solution
        
        return None
    
    def refine_solution(self, solution: Solution, problem: Problem) -> Solution:
        """Refine an existing solution to improve quality."""
        # Add more components or modify approach
        refined_components = solution.components.copy()
        
        # Add new components
        for _ in range(random.randint(1, 3)):
            category = random.choice(list(self.component_library.keys()))
            component = random.choice(self.component_library[category])
            refined_components.append(component)
        
        refined_solution = Solution(
            solution_id=f"{solution.solution_id}_refined",
            problem_id=problem.problem_id,
            approach=f"{solution.approach}_refined",
            components=refined_components
        )
        
        refined_solution.calculate_quality(problem)
        refined_solution.calculate_novelty(self.solution_history.get(problem.problem_id, []))
        
        return refined_solution
    
    def combine_solutions(self, sol1: Solution, sol2: Solution, problem: Problem) -> Solution:
        """Combine two solutions to create a hybrid."""
        combined_components = []
        
        # Mix components from both solutions
        for i in range(max(len(sol1.components), len(sol2.components))):
            if i < len(sol1.components) and random.random() < 0.5:
                combined_components.append(sol1.components[i])
            if i < len(sol2.components) and random.random() < 0.5:
                combined_components.append(sol2.components[i])
        
        combined_solution = Solution(
            solution_id=f"combined_{sol1.solution_id}_{sol2.solution_id}",
            problem_id=problem.problem_id,
            approach=f"hybrid_{sol1.approach}_{sol2.approach}",
            components=combined_components
        )
        
        combined_solution.calculate_quality(problem)
        combined_solution.calculate_novelty(self.solution_history.get(problem.problem_id, []))
        
        return combined_solution


def create_open_ended_problem(problem_id: str, complexity: float = 1.0) -> Problem:
    """Create an open-ended problem with minimal constraints."""
    return Problem(
        problem_id=problem_id,
        description=f"Open-ended problem {problem_id}",
        constraints=[f"constraint_{i}" for i in range(int(complexity))],
        target_solutions=random.randint(3, 10),
        complexity=complexity
    )


def create_constraint_based_problem(problem_id: str, num_constraints: int = 5) -> Problem:
    """Create a problem with specific constraints."""
    constraints = [
        f"constraint_{i}: {random.choice(['must_include', 'must_exclude', 'must_optimize'])}"
        for i in range(num_constraints)
    ]
    
    return Problem(
        problem_id=problem_id,
        description=f"Constraint-based problem {problem_id}",
        constraints=constraints,
        target_solutions=random.randint(2, 5),
        complexity=1.5
    )


def create_multi_solution_problem(problem_id: str, min_solutions: int = 5) -> Problem:
    """Create a problem requiring multiple diverse solutions."""
    return Problem(
        problem_id=problem_id,
        description=f"Multi-solution problem {problem_id}",
        constraints=[f"diversity_constraint_{i}" for i in range(3)],
        target_solutions=min_solutions,
        complexity=2.0
    )


def benchmark_open_ended_problems(collector: MetricsCollector, iterations: int = 50):
    """Benchmark solving open-ended problems."""
    solver = CreativeProblemSolver()
    
    for i in range(iterations):
        complexity = random.uniform(0.5, 2.0)
        problem = create_open_ended_problem(f"open_ended_{i}", complexity)
        
        with Timer(collector, "open_ended_solving", "deschooling_learning"):
            solutions = solver.solve_problem(problem, num_solutions=3)
            
            # Calculate metrics
            avg_quality = sum(s.quality_score for s in solutions) / len(solutions)
            avg_novelty = sum(s.novelty_score for s in solutions) / len(solutions)
            
            collector.record_custom_metric("solution_count", len(solutions))
            collector.record_custom_metric("avg_quality", avg_quality)
            collector.record_custom_metric("avg_novelty", avg_novelty)
            collector.record_custom_metric("problem_complexity", complexity)


def benchmark_constraint_based_problems(collector: MetricsCollector, iterations: int = 50):
    """Benchmark solving constraint-based problems."""
    solver = CreativeProblemSolver()
    
    for i in range(iterations):
        num_constraints = random.randint(3, 8)
        problem = create_constraint_based_problem(f"constraint_{i}", num_constraints)
        
        with Timer(collector, "constraint_based_solving", "deschooling_learning"):
            solutions = solver.solve_problem(problem, num_solutions=2)
            
            # Evaluate constraint satisfaction
            for solution in solutions:
                quality = solution.calculate_quality(problem)
            
            avg_quality = sum(s.quality_score for s in solutions) / len(solutions)
            
            collector.record_custom_metric("num_constraints", num_constraints)
            collector.record_custom_metric("solution_count", len(solutions))
            collector.record_custom_metric("avg_quality", avg_quality)
            collector.record_custom_metric("constraint_satisfaction", avg_quality)


def benchmark_multi_solution_problems(collector: MetricsCollector, iterations: int = 30):
    """Benchmark generating multiple diverse solutions."""
    solver = CreativeProblemSolver()
    
    for i in range(iterations):
        min_solutions = random.randint(5, 10)
        problem = create_multi_solution_problem(f"multi_sol_{i}", min_solutions)
        
        with Timer(collector, "multi_solution_generation", "deschooling_learning"):
            solutions = solver.solve_problem(problem, num_solutions=min_solutions)
            
            # Calculate diversity metrics
            unique_approaches = len(set(s.approach for s in solutions))
            avg_novelty = sum(s.novelty_score for s in solutions) / len(solutions)
            avg_quality = sum(s.quality_score for s in solutions) / len(solutions)
            
            collector.record_custom_metric("solution_count", len(solutions))
            collector.record_custom_metric("unique_approaches", unique_approaches)
            collector.record_custom_metric("avg_novelty", avg_novelty)
            collector.record_custom_metric("avg_quality", avg_quality)
            collector.record_custom_metric("diversity_score", unique_approaches / len(solutions))


def benchmark_novel_solution_generation(collector: MetricsCollector, iterations: int = 50):
    """Benchmark generating novel solutions with high novelty scores."""
    solver = CreativeProblemSolver()
    
    problem = create_open_ended_problem("novelty_test", complexity=1.5)
    
    # Generate some baseline solutions first
    solver.solve_problem(problem, num_solutions=5)
    
    novelty_thresholds = [0.5, 0.7, 0.9]
    
    for threshold in novelty_thresholds:
        for i in range(iterations):
            with Timer(collector, f"novel_generation_{threshold}", "deschooling_learning"):
                novel_solution = solver.generate_novel_solution(problem, min_novelty=threshold)
                
                if novel_solution:
                    collector.record_custom_metric("novelty_threshold", threshold)
                    collector.record_custom_metric("achieved_novelty", novel_solution.novelty_score)
                    collector.record_custom_metric("solution_quality", novel_solution.quality_score)
                    collector.record_custom_metric("generation_success", 1.0)
                else:
                    collector.record_custom_metric("novelty_threshold", threshold)
                    collector.record_custom_metric("generation_success", 0.0)


def benchmark_solution_quality(collector: MetricsCollector, iterations: int = 100):
    """Benchmark solution quality across different problem types."""
    solver = CreativeProblemSolver()
    
    problem_types = ['simple', 'moderate', 'complex']
    complexity_map = {'simple': 0.5, 'moderate': 1.5, 'complex': 3.0}
    
    for problem_type in problem_types:
        complexity = complexity_map[problem_type]
        
        for i in range(iterations):
            problem = create_open_ended_problem(f"quality_{problem_type}_{i}", complexity)
            
            with Timer(collector, f"solution_quality_{problem_type}", "deschooling_learning"):
                solutions = solver.solve_problem(problem, num_solutions=3)
                
                qualities = [s.quality_score for s in solutions]
                best_quality = max(qualities)
                avg_quality = sum(qualities) / len(qualities)
                
                collector.record_custom_metric("problem_type", complexity)
                collector.record_custom_metric("best_quality", best_quality)
                collector.record_custom_metric("avg_quality", avg_quality)
                collector.record_custom_metric("quality_variance", max(qualities) - min(qualities))


def benchmark_solution_refinement(collector: MetricsCollector, iterations: int = 50):
    """Benchmark refining existing solutions to improve quality."""
    solver = CreativeProblemSolver()
    
    for i in range(iterations):
        problem = create_open_ended_problem(f"refine_{i}", complexity=1.0)
        
        # Generate initial solution
        initial_solutions = solver.solve_problem(problem, num_solutions=1)
        initial_solution = initial_solutions[0]
        initial_quality = initial_solution.quality_score
        
        with Timer(collector, "solution_refinement", "deschooling_learning"):
            refined_solution = solver.refine_solution(initial_solution, problem)
            
            quality_improvement = refined_solution.quality_score - initial_quality
            
            collector.record_custom_metric("initial_quality", initial_quality)
            collector.record_custom_metric("refined_quality", refined_solution.quality_score)
            collector.record_custom_metric("quality_improvement", quality_improvement)
            collector.record_custom_metric("refinement_success", 1.0 if quality_improvement > 0 else 0.0)


def benchmark_solution_combination(collector: MetricsCollector, iterations: int = 50):
    """Benchmark combining solutions to create hybrid approaches."""
    solver = CreativeProblemSolver()
    
    for i in range(iterations):
        problem = create_open_ended_problem(f"combine_{i}", complexity=1.5)
        
        # Generate two initial solutions
        solutions = solver.solve_problem(problem, num_solutions=2)
        sol1, sol2 = solutions[0], solutions[1]
        
        with Timer(collector, "solution_combination", "deschooling_learning"):
            combined = solver.combine_solutions(sol1, sol2, problem)
            
            avg_parent_quality = (sol1.quality_score + sol2.quality_score) / 2
            quality_delta = combined.quality_score - avg_parent_quality
            
            collector.record_custom_metric("combined_quality", combined.quality_score)
            collector.record_custom_metric("avg_parent_quality", avg_parent_quality)
            collector.record_custom_metric("quality_delta", quality_delta)
            collector.record_custom_metric("combined_novelty", combined.novelty_score)


def run_all_benchmarks(mode: str = "comprehensive"):
    """Run all creative problem solving benchmarks."""
    collector = MetricsCollector()
    
    iterations = {
        "quick": {
            "open_ended": 20, "constraint": 20, "multi_solution": 10,
            "novel": 20, "quality": 30, "refinement": 20, "combination": 20
        },
        "comprehensive": {
            "open_ended": 50, "constraint": 50, "multi_solution": 30,
            "novel": 50, "quality": 100, "refinement": 50, "combination": 50
        }
    }
    
    iters = iterations.get(mode, iterations["comprehensive"])
    
    print(f"Running Deschooling Creative Problem Solving Benchmarks (mode: {mode})...")
    
    print("  - Open-ended problems...")
    benchmark_open_ended_problems(collector, iters["open_ended"])
    
    print("  - Constraint-based problems...")
    benchmark_constraint_based_problems(collector, iters["constraint"])
    
    print("  - Multi-solution problems...")
    benchmark_multi_solution_problems(collector, iters["multi_solution"])
    
    print("  - Novel solution generation...")
    benchmark_novel_solution_generation(collector, iters["novel"])
    
    print("  - Solution quality...")
    benchmark_solution_quality(collector, iters["quality"])
    
    print("  - Solution refinement...")
    benchmark_solution_refinement(collector, iters["refinement"])
    
    print("  - Solution combination...")
    benchmark_solution_combination(collector, iters["combination"])
    
    return collector.get_all_results()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Deschooling Creative Problem Solving Benchmarks")
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
