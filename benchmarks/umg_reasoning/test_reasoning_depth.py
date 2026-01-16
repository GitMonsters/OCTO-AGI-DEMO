"""
UMG Reasoning Depth Benchmarks

Measures the quality and depth of logical reasoning capabilities.
Tests inference accuracy, reasoning steps, and time per inference.
"""

import time
import random
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.metrics_collector import MetricsCollector, Timer


class LogicOperator(Enum):
    """Logical operators for reasoning."""
    AND = "and"
    OR = "or"
    NOT = "not"
    IMPLIES = "implies"


@dataclass
class LogicStatement:
    """Represents a logical statement."""
    premise: str
    operator: Optional[LogicOperator]
    conclusion: str
    truth_value: bool = True


class ReasoningEngine:
    """Simulated reasoning engine for benchmarking."""
    
    def __init__(self):
        self.knowledge_base: List[LogicStatement] = []
        self.inference_chain: List[str] = []
    
    def add_statement(self, statement: LogicStatement):
        """Add a statement to the knowledge base."""
        self.knowledge_base.append(statement)
    
    def simple_inference(self, query: str) -> Tuple[bool, int]:
        """
        Perform simple logical inference.
        Returns (conclusion, steps_taken).
        """
        steps = 0
        self.inference_chain.clear()
        
        # Direct lookup
        for stmt in self.knowledge_base:
            steps += 1
            if stmt.premise == query:
                self.inference_chain.append(f"Direct: {query} -> {stmt.truth_value}")
                return stmt.truth_value, steps
        
        # One-step inference
        for stmt in self.knowledge_base:
            steps += 1
            if stmt.conclusion == query and stmt.operator == LogicOperator.IMPLIES:
                premise_true, sub_steps = self.simple_inference(stmt.premise)
                steps += sub_steps
                if premise_true:
                    self.inference_chain.append(f"Implies: {stmt.premise} -> {query}")
                    return True, steps
        
        return False, steps
    
    def complex_inference(self, query: str, max_depth: int = 10) -> Tuple[bool, int]:
        """
        Perform complex multi-step inference.
        Returns (conclusion, steps_taken).
        """
        steps = 0
        visited = set()
        
        def recursive_inference(q: str, depth: int) -> Tuple[bool, int]:
            nonlocal steps
            
            if depth >= max_depth or q in visited:
                return False, 0
            
            visited.add(q)
            local_steps = 0
            
            # Check knowledge base
            for stmt in self.knowledge_base:
                local_steps += 1
                
                if stmt.conclusion == q:
                    if stmt.operator == LogicOperator.AND:
                        # Both premises must be true
                        parts = stmt.premise.split(" AND ")
                        if len(parts) == 2:
                            result1, steps1 = recursive_inference(parts[0].strip(), depth + 1)
                            result2, steps2 = recursive_inference(parts[1].strip(), depth + 1)
                            local_steps += steps1 + steps2
                            if result1 and result2:
                                return True, local_steps
                    
                    elif stmt.operator == LogicOperator.OR:
                        # At least one premise must be true
                        parts = stmt.premise.split(" OR ")
                        if len(parts) == 2:
                            result1, steps1 = recursive_inference(parts[0].strip(), depth + 1)
                            local_steps += steps1
                            if result1:
                                return True, local_steps
                            result2, steps2 = recursive_inference(parts[1].strip(), depth + 1)
                            local_steps += steps2
                            if result2:
                                return True, local_steps
                    
                    elif stmt.operator == LogicOperator.IMPLIES:
                        result, sub_steps = recursive_inference(stmt.premise, depth + 1)
                        local_steps += sub_steps
                        if result:
                            return True, local_steps
                    
                    elif stmt.premise == "true":
                        return stmt.truth_value, local_steps
            
            return False, local_steps
        
        result, steps = recursive_inference(query, 0)
        return result, steps
    
    def chain_reasoning(self, start: str, goal: str, max_steps: int = 20) -> Tuple[List[str], int]:
        """
        Perform chain reasoning from start to goal.
        Returns (reasoning_chain, total_steps).
        """
        chain = [start]
        steps = 0
        current = start
        
        for _ in range(max_steps):
            found_next = False
            
            for stmt in self.knowledge_base:
                steps += 1
                
                if stmt.premise == current:
                    chain.append(stmt.conclusion)
                    current = stmt.conclusion
                    found_next = True
                    
                    if current == goal:
                        return chain, steps
                    break
            
            if not found_next:
                break
        
        return chain, steps


def create_simple_knowledge_base() -> ReasoningEngine:
    """Create a simple knowledge base for testing."""
    engine = ReasoningEngine()
    
    # Basic facts
    engine.add_statement(LogicStatement("sky_is_blue", None, "true"))
    engine.add_statement(LogicStatement("water_is_wet", None, "true"))
    engine.add_statement(LogicStatement("fire_is_hot", None, "true"))
    
    # Simple implications
    engine.add_statement(LogicStatement("raining", LogicOperator.IMPLIES, "wet_outside"))
    engine.add_statement(LogicStatement("wet_outside", LogicOperator.IMPLIES, "slippery"))
    engine.add_statement(LogicStatement("slippery", LogicOperator.IMPLIES, "dangerous"))
    
    return engine


def create_complex_knowledge_base() -> ReasoningEngine:
    """Create a complex knowledge base with deeper reasoning chains."""
    engine = ReasoningEngine()
    
    # Build a reasoning chain of depth 10
    for i in range(15):
        premise = f"fact_{i}"
        conclusion = f"fact_{i+1}"
        engine.add_statement(LogicStatement(premise, LogicOperator.IMPLIES, conclusion))
    
    # Add some AND/OR logic
    engine.add_statement(LogicStatement("condition_a AND condition_b", LogicOperator.AND, "result_ab"))
    engine.add_statement(LogicStatement("option_x OR option_y", LogicOperator.OR, "result_xy"))
    
    # Add base facts
    for i in range(5):
        engine.add_statement(LogicStatement(f"base_{i}", None, "true"))
    
    return engine


def benchmark_simple_logical_chains(collector: MetricsCollector, iterations: int = 100):
    """Benchmark simple 2-3 step logical chains."""
    engine = create_simple_knowledge_base()
    
    queries = ["wet_outside", "slippery", "dangerous"]
    
    for i in range(iterations):
        query = random.choice(queries)
        with Timer(collector, "simple_logic_chain", "umg_reasoning"):
            result, steps = engine.simple_inference(query)
            collector.record_custom_metric("reasoning_steps", steps)
            collector.record_custom_metric("inference_accuracy", 1.0 if result else 0.0)


def benchmark_medium_complexity_reasoning(collector: MetricsCollector, iterations: int = 50):
    """Benchmark medium complexity reasoning (5-10 steps)."""
    engine = create_complex_knowledge_base()
    
    for i in range(iterations):
        depth = random.randint(5, 10)
        query = f"fact_{depth}"
        with Timer(collector, "medium_complexity_reasoning", "umg_reasoning"):
            result, steps = engine.complex_inference(query, max_depth=15)
            collector.record_custom_metric("reasoning_steps", steps)
            collector.record_custom_metric("inference_depth", depth)


def benchmark_complex_reasoning(collector: MetricsCollector, iterations: int = 30):
    """Benchmark complex reasoning (10+ steps)."""
    engine = create_complex_knowledge_base()
    
    for i in range(iterations):
        depth = random.randint(10, 15)
        query = f"fact_{depth}"
        with Timer(collector, "complex_reasoning", "umg_reasoning"):
            result, steps = engine.complex_inference(query, max_depth=20)
            collector.record_custom_metric("reasoning_steps", steps)
            collector.record_custom_metric("inference_depth", depth)


def benchmark_chain_reasoning(collector: MetricsCollector, iterations: int = 50):
    """Benchmark chain reasoning performance."""
    engine = create_complex_knowledge_base()
    
    for i in range(iterations):
        start = "fact_0"
        goal_depth = random.randint(5, 10)
        goal = f"fact_{goal_depth}"
        
        with Timer(collector, "chain_reasoning", "umg_reasoning"):
            chain, steps = engine.chain_reasoning(start, goal, max_steps=30)
            collector.record_custom_metric("chain_length", len(chain))
            collector.record_custom_metric("reasoning_steps", steps)
            collector.record_custom_metric("goal_reached", 1.0 if chain[-1] == goal else 0.0)


def benchmark_parallel_inferences(collector: MetricsCollector, iterations: int = 20):
    """Benchmark multiple simultaneous inferences."""
    engine = create_complex_knowledge_base()
    
    for i in range(iterations):
        queries = [f"fact_{random.randint(1, 10)}" for _ in range(5)]
        
        with Timer(collector, "parallel_inferences", "umg_reasoning"):
            results = []
            total_steps = 0
            for query in queries:
                result, steps = engine.complex_inference(query, max_depth=15)
                results.append(result)
                total_steps += steps
            
            collector.record_custom_metric("total_inferences", len(queries))
            collector.record_custom_metric("total_steps", total_steps)
            collector.record_custom_metric("accuracy", sum(results) / len(results))


def run_all_benchmarks(mode: str = "comprehensive"):
    """Run all reasoning depth benchmarks."""
    collector = MetricsCollector()
    
    iterations = {
        "quick": {"simple": 10, "medium": 5, "complex": 3, "chain": 5, "parallel": 3},
        "comprehensive": {"simple": 100, "medium": 50, "complex": 30, "chain": 50, "parallel": 20}
    }
    
    iters = iterations.get(mode, iterations["comprehensive"])
    
    print(f"Running UMG Reasoning Depth Benchmarks (mode: {mode})...")
    
    print("  - Simple logical chains...")
    benchmark_simple_logical_chains(collector, iters["simple"])
    
    print("  - Medium complexity reasoning...")
    benchmark_medium_complexity_reasoning(collector, iters["medium"])
    
    print("  - Complex reasoning...")
    benchmark_complex_reasoning(collector, iters["complex"])
    
    print("  - Chain reasoning...")
    benchmark_chain_reasoning(collector, iters["chain"])
    
    print("  - Parallel inferences...")
    benchmark_parallel_inferences(collector, iters["parallel"])
    
    return collector.get_all_results()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="UMG Reasoning Depth Benchmarks")
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
                print(f"  {metric_name}: {metric_data['mean']:.2f}")
