"""
Cross-System Coherence Benchmarks

Tests integration quality across all subsystems (UMG, Spatial, Learning).
Measures coherence scores, consistency, and integration quality for
two-system, three-system, and full system integration.
"""

import time
import random
import math
import sys
import os
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.metrics_collector import MetricsCollector, Timer


@dataclass
class SystemState:
    """Represents the state of a subsystem."""
    system_id: str
    activation_level: float
    coherence_score: float
    data: Dict[str, Any]
    
    def validate(self) -> bool:
        """Check if state is valid."""
        return 0 <= self.activation_level <= 1 and 0 <= self.coherence_score <= 1


class SubsystemSimulator:
    """Simulates a subsystem (UMG, Spatial, or Learning)."""
    
    def __init__(self, system_id: str, complexity: int = 10):
        self.system_id = system_id
        self.complexity = complexity
        self.state = SystemState(
            system_id=system_id,
            activation_level=random.uniform(0.5, 1.0),
            coherence_score=random.uniform(0.7, 1.0),
            data=self._generate_data()
        )
    
    def _generate_data(self) -> Dict[str, Any]:
        """Generate system-specific data."""
        return {
            f"param_{i}": random.uniform(0, 100)
            for i in range(self.complexity)
        }
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input and return output."""
        output = {}
        for key, value in input_data.items():
            if isinstance(value, (int, float)):
                output[key] = value * self.state.activation_level
        return output
    
    def sync_with(self, other: 'SubsystemSimulator') -> float:
        """Synchronize with another subsystem and return coherence score."""
        # Simulate synchronization
        score = (self.state.coherence_score + other.state.coherence_score) / 2
        # Add some variance
        score *= random.uniform(0.9, 1.0)
        return min(1.0, score)


class IntegrationManager:
    """Manages integration across multiple subsystems."""
    
    def __init__(self):
        self.systems: Dict[str, SubsystemSimulator] = {}
        self.integration_graph: Dict[Tuple[str, str], float] = {}
    
    def add_system(self, system: SubsystemSimulator):
        """Add a subsystem to the integration manager."""
        self.systems[system.system_id] = system
    
    def compute_pairwise_coherence(self, sys1_id: str, sys2_id: str) -> float:
        """Compute coherence between two systems."""
        if sys1_id not in self.systems or sys2_id not in self.systems:
            return 0.0
        
        sys1 = self.systems[sys1_id]
        sys2 = self.systems[sys2_id]
        
        coherence = sys1.sync_with(sys2)
        self.integration_graph[(sys1_id, sys2_id)] = coherence
        return coherence
    
    def compute_global_coherence(self) -> float:
        """Compute overall coherence across all systems."""
        if not self.systems:
            return 0.0
        
        system_ids = list(self.systems.keys())
        coherence_scores = []
        
        for i, sys1_id in enumerate(system_ids):
            for sys2_id in system_ids[i+1:]:
                score = self.compute_pairwise_coherence(sys1_id, sys2_id)
                coherence_scores.append(score)
        
        return sum(coherence_scores) / len(coherence_scores) if coherence_scores else 0.0
    
    def compute_consistency_score(self) -> float:
        """Compute consistency across all system states."""
        if not self.systems:
            return 0.0
        
        states = [sys.state for sys in self.systems.values()]
        
        # Check activation level variance
        activations = [s.activation_level for s in states]
        avg_activation = sum(activations) / len(activations)
        activation_variance = sum((a - avg_activation) ** 2 for a in activations) / len(activations)
        
        # Check coherence score variance
        coherences = [s.coherence_score for s in states]
        avg_coherence = sum(coherences) / len(coherences)
        coherence_variance = sum((c - avg_coherence) ** 2 for c in coherences) / len(coherences)
        
        # Lower variance means higher consistency
        consistency = 1.0 - (activation_variance + coherence_variance) / 2
        return max(0.0, min(1.0, consistency))
    
    def integrate_data(self, system_ids: List[str]) -> Dict[str, Any]:
        """Integrate data from specified systems."""
        integrated = {}
        
        for sys_id in system_ids:
            if sys_id in self.systems:
                system = self.systems[sys_id]
                output = system.process(system.state.data)
                for key, value in output.items():
                    if key in integrated:
                        integrated[key] = (integrated[key] + value) / 2
                    else:
                        integrated[key] = value
        
        return integrated


def benchmark_two_system_integration(collector: MetricsCollector, iterations: int = 50):
    """Benchmark integration between two subsystems."""
    system_pairs = [
        ("UMG", "Spatial"),
        ("UMG", "Learning"),
        ("Spatial", "Learning")
    ]
    
    for sys1, sys2 in system_pairs:
        for i in range(iterations):
            with Timer(collector, f"two_system_{sys1}_{sys2}", "unified_consciousness"):
                manager = IntegrationManager()
                manager.add_system(SubsystemSimulator(sys1, complexity=10))
                manager.add_system(SubsystemSimulator(sys2, complexity=10))
                
                coherence = manager.compute_global_coherence()
                consistency = manager.compute_consistency_score()
                integrated_data = manager.integrate_data([sys1, sys2])
                
                collector.record_custom_metric("coherence_score", coherence)
                collector.record_custom_metric("consistency_score", consistency)
                collector.record_custom_metric("integration_quality", (coherence + consistency) / 2)
                collector.record_custom_metric("integrated_data_size", len(integrated_data))


def benchmark_three_system_integration(collector: MetricsCollector, iterations: int = 30):
    """Benchmark integration across all three subsystems."""
    for i in range(iterations):
        with Timer(collector, "three_system_integration", "unified_consciousness"):
            manager = IntegrationManager()
            manager.add_system(SubsystemSimulator("UMG", complexity=15))
            manager.add_system(SubsystemSimulator("Spatial", complexity=15))
            manager.add_system(SubsystemSimulator("Learning", complexity=15))
            
            coherence = manager.compute_global_coherence()
            consistency = manager.compute_consistency_score()
            integrated_data = manager.integrate_data(["UMG", "Spatial", "Learning"])
            
            # Calculate integration quality
            quality = (coherence * 0.5 + consistency * 0.5)
            
            collector.record_custom_metric("coherence_score", coherence)
            collector.record_custom_metric("consistency_score", consistency)
            collector.record_custom_metric("integration_quality", quality)
            collector.record_custom_metric("system_count", 3)
            collector.record_custom_metric("integrated_data_size", len(integrated_data))


def benchmark_full_system_integration(collector: MetricsCollector, iterations: int = 20):
    """Benchmark full system integration with multiple instances."""
    for i in range(iterations):
        with Timer(collector, "full_system_integration", "unified_consciousness"):
            manager = IntegrationManager()
            
            # Add multiple instances of each subsystem type
            for subsystem in ["UMG", "Spatial", "Learning"]:
                for instance in range(3):
                    system_id = f"{subsystem}_{instance}"
                    manager.add_system(SubsystemSimulator(system_id, complexity=20))
            
            coherence = manager.compute_global_coherence()
            consistency = manager.compute_consistency_score()
            
            # Integrate data from all systems
            all_system_ids = list(manager.systems.keys())
            integrated_data = manager.integrate_data(all_system_ids)
            
            # Calculate comprehensive integration quality
            quality = (coherence * 0.4 + consistency * 0.4 + 
                      (len(integrated_data) / 200) * 0.2)  # Normalize by expected size
            
            collector.record_custom_metric("coherence_score", coherence)
            collector.record_custom_metric("consistency_score", consistency)
            collector.record_custom_metric("integration_quality", quality)
            collector.record_custom_metric("system_count", len(manager.systems))
            collector.record_custom_metric("integration_pairs", len(manager.integration_graph))
            collector.record_custom_metric("integrated_data_size", len(integrated_data))


def benchmark_coherence_degradation(collector: MetricsCollector, iterations: int = 30):
    """Benchmark coherence under stress conditions."""
    for i in range(iterations):
        with Timer(collector, "coherence_degradation", "unified_consciousness"):
            manager = IntegrationManager()
            
            # Add systems with varying quality
            for j in range(5):
                system = SubsystemSimulator(f"System_{j}", complexity=10)
                # Simulate degradation
                system.state.coherence_score *= random.uniform(0.5, 1.0)
                manager.add_system(system)
            
            initial_coherence = manager.compute_global_coherence()
            
            # Perform multiple integration cycles
            for cycle in range(10):
                system_ids = random.sample(list(manager.systems.keys()), 3)
                manager.integrate_data(system_ids)
            
            final_coherence = manager.compute_global_coherence()
            degradation = initial_coherence - final_coherence
            
            collector.record_custom_metric("initial_coherence", initial_coherence)
            collector.record_custom_metric("final_coherence", final_coherence)
            collector.record_custom_metric("coherence_degradation", degradation)
            collector.record_custom_metric("integration_cycles", 10)


def benchmark_consistency_validation(collector: MetricsCollector, iterations: int = 40):
    """Benchmark consistency validation across systems."""
    for i in range(iterations):
        with Timer(collector, "consistency_validation", "unified_consciousness"):
            manager = IntegrationManager()
            
            # Add systems with controlled variance
            base_activation = random.uniform(0.6, 0.9)
            for j in range(4):
                system = SubsystemSimulator(f"System_{j}", complexity=12)
                # Control activation levels for consistency testing
                system.state.activation_level = base_activation + random.uniform(-0.1, 0.1)
                manager.add_system(system)
            
            consistency = manager.compute_consistency_score()
            
            # Validate all system states
            valid_count = sum(1 for sys in manager.systems.values() if sys.state.validate())
            validation_rate = valid_count / len(manager.systems)
            
            collector.record_custom_metric("consistency_score", consistency)
            collector.record_custom_metric("validation_rate", validation_rate)
            collector.record_custom_metric("systems_validated", valid_count)


def run_all_benchmarks(mode: str = "comprehensive"):
    """Run all cross-system coherence benchmarks."""
    collector = MetricsCollector()
    
    iterations = {
        "quick": {"two_sys": 10, "three_sys": 5, "full_sys": 3, "degrade": 5, "validate": 10},
        "comprehensive": {"two_sys": 50, "three_sys": 30, "full_sys": 20, "degrade": 30, "validate": 40}
    }
    
    iters = iterations.get(mode, iterations["comprehensive"])
    
    print(f"Running Cross-System Coherence Benchmarks (mode: {mode})...")
    
    print("  - Two-system integration...")
    benchmark_two_system_integration(collector, iters["two_sys"])
    
    print("  - Three-system integration...")
    benchmark_three_system_integration(collector, iters["three_sys"])
    
    print("  - Full system integration...")
    benchmark_full_system_integration(collector, iters["full_sys"])
    
    print("  - Coherence degradation...")
    benchmark_coherence_degradation(collector, iters["degrade"])
    
    print("  - Consistency validation...")
    benchmark_consistency_validation(collector, iters["validate"])
    
    return collector.get_all_results()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Cross-System Coherence Benchmarks")
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
            if 'coherence_score' in summary['custom_metrics']:
                coherence = summary['custom_metrics']['coherence_score']
                print(f"  Coherence: {coherence['mean']:.3f} (±{coherence['max'] - coherence['min']:.3f})")
            if 'integration_quality' in summary['custom_metrics']:
                quality = summary['custom_metrics']['integration_quality']
                print(f"  Quality: {quality['mean']:.3f}")
