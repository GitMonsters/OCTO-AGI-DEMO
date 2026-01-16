"""
Emergent Behavior Benchmarks

Tests unexpected capabilities and behaviors from system integration.
Tracks novel behavior count, behavior quality through complex scenario testing,
edge case discovery, and capability emergence tracking.
"""

import time
import random
import math
import sys
import os
from typing import Dict, List, Set, Tuple, Any
from dataclasses import dataclass
from enum import Enum

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.metrics_collector import MetricsCollector, Timer


class BehaviorType(Enum):
    """Types of emergent behaviors."""
    PATTERN_RECOGNITION = "pattern_recognition"
    CREATIVE_SOLUTION = "creative_solution"
    UNEXPECTED_OPTIMIZATION = "unexpected_optimization"
    CROSS_DOMAIN_TRANSFER = "cross_domain_transfer"
    NOVEL_COMBINATION = "novel_combination"
    ADAPTIVE_RESPONSE = "adaptive_response"


@dataclass
class Behavior:
    """Represents an emergent behavior."""
    behavior_type: BehaviorType
    complexity: float
    novelty_score: float
    quality_score: float
    context: Dict[str, Any]
    timestamp: float
    
    def is_novel(self, threshold: float = 0.7) -> bool:
        """Check if behavior is considered novel."""
        return self.novelty_score >= threshold
    
    def is_high_quality(self, threshold: float = 0.7) -> bool:
        """Check if behavior is high quality."""
        return self.quality_score >= threshold


class BehaviorTracker:
    """Tracks and analyzes emergent behaviors."""
    
    def __init__(self):
        self.observed_behaviors: List[Behavior] = []
        self.behavior_patterns: Dict[BehaviorType, List[Behavior]] = {
            bt: [] for bt in BehaviorType
        }
        self.novel_behaviors: Set[str] = set()
    
    def record_behavior(self, behavior: Behavior):
        """Record a new behavior."""
        self.observed_behaviors.append(behavior)
        self.behavior_patterns[behavior.behavior_type].append(behavior)
        
        if behavior.is_novel():
            # Create unique signature for the behavior
            signature = f"{behavior.behavior_type.value}_{behavior.complexity:.2f}_{len(self.observed_behaviors)}"
            self.novel_behaviors.add(signature)
    
    def get_novel_behavior_count(self) -> int:
        """Get count of novel behaviors."""
        return len(self.novel_behaviors)
    
    def get_average_quality(self) -> float:
        """Get average quality of all behaviors."""
        if not self.observed_behaviors:
            return 0.0
        return sum(b.quality_score for b in self.observed_behaviors) / len(self.observed_behaviors)
    
    def get_behavior_diversity(self) -> float:
        """Calculate diversity of observed behaviors."""
        if not self.observed_behaviors:
            return 0.0
        
        type_counts = {bt: len(behaviors) for bt, behaviors in self.behavior_patterns.items()}
        total = len(self.observed_behaviors)
        
        # Shannon entropy for diversity
        diversity = 0.0
        for count in type_counts.values():
            if count > 0:
                p = count / total
                diversity -= p * math.log2(p)
        
        # Normalize by max possible entropy
        max_entropy = math.log2(len(BehaviorType))
        return diversity / max_entropy if max_entropy > 0 else 0.0
    
    def analyze_trends(self) -> Dict[str, float]:
        """Analyze trends in emergent behaviors."""
        if len(self.observed_behaviors) < 2:
            return {"quality_trend": 0.0, "novelty_trend": 0.0}
        
        # Split into first and second half
        mid = len(self.observed_behaviors) // 2
        first_half = self.observed_behaviors[:mid]
        second_half = self.observed_behaviors[mid:]
        
        # Compare averages
        first_quality = sum(b.quality_score for b in first_half) / len(first_half)
        second_quality = sum(b.quality_score for b in second_half) / len(second_half)
        
        first_novelty = sum(b.novelty_score for b in first_half) / len(first_half)
        second_novelty = sum(b.novelty_score for b in second_half) / len(second_half)
        
        return {
            "quality_trend": second_quality - first_quality,
            "novelty_trend": second_novelty - first_novelty
        }


class ComplexScenario:
    """Represents a complex scenario for testing emergence."""
    
    def __init__(self, scenario_id: str, complexity: int = 5):
        self.scenario_id = scenario_id
        self.complexity = complexity
        self.constraints = self._generate_constraints()
        self.goals = self._generate_goals()
        self.context = self._generate_context()
    
    def _generate_constraints(self) -> List[Dict[str, Any]]:
        """Generate scenario constraints."""
        constraints = []
        for i in range(self.complexity):
            constraints.append({
                "type": random.choice(["resource", "time", "quality", "safety"]),
                "value": random.uniform(0.3, 0.9),
                "priority": random.randint(1, 5)
            })
        return constraints
    
    def _generate_goals(self) -> List[str]:
        """Generate scenario goals."""
        goal_types = ["optimize", "minimize", "maximize", "balance", "discover"]
        return random.sample(goal_types, min(3, len(goal_types)))
    
    def _generate_context(self) -> Dict[str, Any]:
        """Generate scenario context."""
        return {
            "environment": random.choice(["stable", "dynamic", "chaotic"]),
            "resources": random.randint(5, 20),
            "time_limit": random.uniform(0.5, 2.0),
            "uncertainty": random.uniform(0.1, 0.5)
        }
    
    def evaluate_solution(self, solution: Dict[str, Any]) -> float:
        """Evaluate a solution to this scenario."""
        score = 0.0
        
        # Check constraint satisfaction
        for constraint in self.constraints:
            if constraint["type"] in solution:
                satisfaction = 1.0 - abs(solution[constraint["type"]] - constraint["value"])
                score += satisfaction * constraint["priority"]
        
        # Normalize by total possible score
        max_score = sum(c["priority"] for c in self.constraints)
        return score / max_score if max_score > 0 else 0.0


class EmergenceSimulator:
    """Simulates conditions for emergent behaviors."""
    
    def __init__(self, num_subsystems: int = 3):
        self.num_subsystems = num_subsystems
        self.subsystem_states: List[Dict[str, float]] = []
        self.interaction_matrix: List[List[float]] = []
        self._initialize()
    
    def _initialize(self):
        """Initialize subsystem states and interactions."""
        for i in range(self.num_subsystems):
            state = {
                "activation": random.uniform(0.5, 1.0),
                "coherence": random.uniform(0.6, 1.0),
                "capacity": random.uniform(0.7, 1.0)
            }
            self.subsystem_states.append(state)
        
        # Create interaction matrix
        self.interaction_matrix = [
            [random.uniform(0.1, 0.9) for _ in range(self.num_subsystems)]
            for _ in range(self.num_subsystems)
        ]
    
    def simulate_interaction(self) -> Behavior:
        """Simulate subsystem interaction and detect emergent behavior."""
        # Calculate interaction strength
        total_interaction = 0.0
        for i in range(self.num_subsystems):
            for j in range(self.num_subsystems):
                if i != j:
                    state_i = self.subsystem_states[i]["activation"]
                    state_j = self.subsystem_states[j]["activation"]
                    interaction = self.interaction_matrix[i][j]
                    total_interaction += state_i * state_j * interaction
        
        # Normalize interaction
        max_interaction = self.num_subsystems * (self.num_subsystems - 1)
        normalized_interaction = total_interaction / max_interaction if max_interaction > 0 else 0.0
        
        # Determine behavior type based on interaction pattern
        behavior_type = random.choice(list(BehaviorType))
        
        # Calculate complexity based on subsystem states
        avg_coherence = sum(s["coherence"] for s in self.subsystem_states) / self.num_subsystems
        complexity = normalized_interaction * avg_coherence
        
        # Novelty is higher for stronger, more complex interactions
        novelty_score = complexity * random.uniform(0.8, 1.2)
        novelty_score = min(1.0, max(0.0, novelty_score))
        
        # Quality depends on capacity and coherence
        avg_capacity = sum(s["capacity"] for s in self.subsystem_states) / self.num_subsystems
        quality_score = (avg_coherence + avg_capacity) / 2 * random.uniform(0.9, 1.1)
        quality_score = min(1.0, max(0.0, quality_score))
        
        return Behavior(
            behavior_type=behavior_type,
            complexity=complexity,
            novelty_score=novelty_score,
            quality_score=quality_score,
            context={"num_subsystems": self.num_subsystems},
            timestamp=time.time()
        )
    
    def evolve_states(self):
        """Evolve subsystem states over time."""
        for state in self.subsystem_states:
            state["activation"] *= random.uniform(0.95, 1.05)
            state["activation"] = min(1.0, max(0.0, state["activation"]))
            
            state["coherence"] *= random.uniform(0.98, 1.02)
            state["coherence"] = min(1.0, max(0.0, state["coherence"]))


def benchmark_complex_scenario_testing(collector: MetricsCollector, iterations: int = 30):
    """Benchmark behavior emergence in complex scenarios."""
    for i in range(iterations):
        with Timer(collector, "complex_scenario_testing", "unified_consciousness"):
            tracker = BehaviorTracker()
            
            # Run multiple complex scenarios
            for scenario_num in range(5):
                scenario = ComplexScenario(f"scenario_{scenario_num}", complexity=random.randint(3, 7))
                simulator = EmergenceSimulator(num_subsystems=3)
                
                # Simulate multiple interactions
                for _ in range(10):
                    behavior = simulator.simulate_interaction()
                    tracker.record_behavior(behavior)
                    simulator.evolve_states()
                    
                    # Generate solution based on emergent behavior
                    solution = {
                        "resource": behavior.complexity * random.uniform(0.5, 1.0),
                        "time": behavior.quality_score,
                        "quality": behavior.novelty_score,
                        "safety": random.uniform(0.7, 1.0)
                    }
                    
                    # Evaluate solution
                    score = scenario.evaluate_solution(solution)
            
            novel_count = tracker.get_novel_behavior_count()
            avg_quality = tracker.get_average_quality()
            diversity = tracker.get_behavior_diversity()
            
            collector.record_custom_metric("novel_behavior_count", novel_count)
            collector.record_custom_metric("behavior_quality", avg_quality)
            collector.record_custom_metric("behavior_diversity", diversity)
            collector.record_custom_metric("scenarios_tested", 5)


def benchmark_edge_case_discovery(collector: MetricsCollector, iterations: int = 40):
    """Benchmark discovery of edge cases through emergent behavior."""
    for i in range(iterations):
        with Timer(collector, "edge_case_discovery", "unified_consciousness"):
            tracker = BehaviorTracker()
            edge_cases_found = 0
            
            # Test with varying subsystem counts to find edge cases
            for num_subsystems in [2, 3, 5, 7]:
                simulator = EmergenceSimulator(num_subsystems=num_subsystems)
                
                # Run interactions to discover edge behaviors
                for _ in range(15):
                    behavior = simulator.simulate_interaction()
                    tracker.record_behavior(behavior)
                    
                    # Edge cases: very high or very low metrics
                    if behavior.complexity > 0.9 or behavior.complexity < 0.1:
                        edge_cases_found += 1
                    if behavior.novelty_score > 0.95:
                        edge_cases_found += 1
                    
                    simulator.evolve_states()
            
            novel_count = tracker.get_novel_behavior_count()
            avg_quality = tracker.get_average_quality()
            
            collector.record_custom_metric("edge_cases_found", edge_cases_found)
            collector.record_custom_metric("novel_behavior_count", novel_count)
            collector.record_custom_metric("behavior_quality", avg_quality)
            collector.record_custom_metric("edge_case_rate", edge_cases_found / len(tracker.observed_behaviors) 
                                          if tracker.observed_behaviors else 0)


def benchmark_capability_emergence(collector: MetricsCollector, iterations: int = 25):
    """Benchmark emergence of new capabilities over time."""
    for i in range(iterations):
        with Timer(collector, "capability_emergence", "unified_consciousness"):
            tracker = BehaviorTracker()
            simulator = EmergenceSimulator(num_subsystems=4)
            
            # Track capabilities over time periods
            time_periods = 5
            behaviors_per_period = 20
            
            for period in range(time_periods):
                period_behaviors = []
                
                for _ in range(behaviors_per_period):
                    behavior = simulator.simulate_interaction()
                    tracker.record_behavior(behavior)
                    period_behaviors.append(behavior)
                    simulator.evolve_states()
                
                # Analyze period
                period_quality = sum(b.quality_score for b in period_behaviors) / len(period_behaviors)
                period_novelty = sum(b.novelty_score for b in period_behaviors) / len(period_behaviors)
            
            # Analyze overall trends
            trends = tracker.analyze_trends()
            novel_count = tracker.get_novel_behavior_count()
            diversity = tracker.get_behavior_diversity()
            
            collector.record_custom_metric("novel_behavior_count", novel_count)
            collector.record_custom_metric("behavior_diversity", diversity)
            collector.record_custom_metric("quality_trend", trends["quality_trend"])
            collector.record_custom_metric("novelty_trend", trends["novelty_trend"])
            collector.record_custom_metric("total_behaviors", len(tracker.observed_behaviors))


def benchmark_behavior_quality_tracking(collector: MetricsCollector, iterations: int = 35):
    """Benchmark quality tracking of emergent behaviors."""
    for i in range(iterations):
        with Timer(collector, "behavior_quality_tracking", "unified_consciousness"):
            tracker = BehaviorTracker()
            
            # Test different configurations
            configurations = [
                {"subsystems": 2, "iterations": 15},
                {"subsystems": 3, "iterations": 20},
                {"subsystems": 4, "iterations": 25},
            ]
            
            quality_scores = []
            high_quality_count = 0
            
            for config in configurations:
                simulator = EmergenceSimulator(num_subsystems=config["subsystems"])
                
                for _ in range(config["iterations"]):
                    behavior = simulator.simulate_interaction()
                    tracker.record_behavior(behavior)
                    quality_scores.append(behavior.quality_score)
                    
                    if behavior.is_high_quality():
                        high_quality_count += 1
                    
                    simulator.evolve_states()
            
            avg_quality = sum(quality_scores) / len(quality_scores)
            quality_variance = sum((q - avg_quality) ** 2 for q in quality_scores) / len(quality_scores)
            quality_consistency = 1.0 - quality_variance  # Higher consistency = lower variance
            
            collector.record_custom_metric("average_quality", avg_quality)
            collector.record_custom_metric("quality_consistency", quality_consistency)
            collector.record_custom_metric("high_quality_count", high_quality_count)
            collector.record_custom_metric("high_quality_rate", high_quality_count / len(quality_scores))


def benchmark_novel_behavior_generation(collector: MetricsCollector, iterations: int = 30):
    """Benchmark generation of novel behaviors."""
    for i in range(iterations):
        with Timer(collector, "novel_behavior_generation", "unified_consciousness"):
            tracker = BehaviorTracker()
            simulator = EmergenceSimulator(num_subsystems=5)
            
            # Generate behaviors and track novelty
            generation_cycles = 50
            novelty_threshold = 0.7
            
            for cycle in range(generation_cycles):
                behavior = simulator.simulate_interaction()
                tracker.record_behavior(behavior)
                
                # Periodically evolve to encourage new behaviors
                if cycle % 10 == 0:
                    simulator.evolve_states()
            
            novel_count = tracker.get_novel_behavior_count()
            total_count = len(tracker.observed_behaviors)
            novelty_rate = novel_count / total_count if total_count > 0 else 0.0
            
            avg_novelty = sum(b.novelty_score for b in tracker.observed_behaviors) / total_count if total_count > 0 else 0.0
            diversity = tracker.get_behavior_diversity()
            
            collector.record_custom_metric("novel_behavior_count", novel_count)
            collector.record_custom_metric("novelty_rate", novelty_rate)
            collector.record_custom_metric("average_novelty", avg_novelty)
            collector.record_custom_metric("behavior_diversity", diversity)
            collector.record_custom_metric("generation_cycles", generation_cycles)


def run_all_benchmarks(mode: str = "comprehensive"):
    """Run all emergent behavior benchmarks."""
    collector = MetricsCollector()
    
    iterations = {
        "quick": {"complex": 8, "edge": 10, "capability": 6, "quality": 10, "novel": 8},
        "comprehensive": {"complex": 30, "edge": 40, "capability": 25, "quality": 35, "novel": 30}
    }
    
    iters = iterations.get(mode, iterations["comprehensive"])
    
    print(f"Running Emergent Behavior Benchmarks (mode: {mode})...")
    
    print("  - Complex scenario testing...")
    benchmark_complex_scenario_testing(collector, iters["complex"])
    
    print("  - Edge case discovery...")
    benchmark_edge_case_discovery(collector, iters["edge"])
    
    print("  - Capability emergence...")
    benchmark_capability_emergence(collector, iters["capability"])
    
    print("  - Behavior quality tracking...")
    benchmark_behavior_quality_tracking(collector, iters["quality"])
    
    print("  - Novel behavior generation...")
    benchmark_novel_behavior_generation(collector, iters["novel"])
    
    return collector.get_all_results()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Emergent Behavior Benchmarks")
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
            if 'novel_behavior_count' in summary['custom_metrics']:
                novel = summary['custom_metrics']['novel_behavior_count']
                print(f"  Novel behaviors: {novel['mean']:.1f}")
            if 'behavior_quality' in summary['custom_metrics']:
                quality = summary['custom_metrics']['behavior_quality']
                print(f"  Behavior quality: {quality['mean']:.3f}")
            if 'behavior_diversity' in summary['custom_metrics']:
                diversity = summary['custom_metrics']['behavior_diversity']
                print(f"  Diversity: {diversity['mean']:.3f}")
