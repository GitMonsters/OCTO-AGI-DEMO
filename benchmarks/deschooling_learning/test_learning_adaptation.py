"""
Deschooling Learning Adaptation Benchmarks

Tests human-centric learning metrics and adaptation capabilities including
adaptation rate, learning speed, flexibility, new pattern learning,
context switching, and adaptive responses.
"""

import time
import random
import math
import sys
import os
from typing import List, Dict, Tuple, Any, Optional
from dataclasses import dataclass

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.metrics_collector import MetricsCollector, Timer


@dataclass
class LearningContext:
    """Represents a learning context with patterns and rules."""
    name: str
    patterns: Dict[str, Any]
    rules: List[str]
    complexity: float


class AdaptiveLearner:
    """Simulates an adaptive learning system."""
    
    def __init__(self):
        self.knowledge_base: Dict[str, Any] = {}
        self.learning_history: List[Tuple[str, float]] = []
        self.adaptation_rate: float = 1.0
        self.current_context: Optional[LearningContext] = None
    
    def learn_pattern(self, pattern_id: str, pattern_data: Any, complexity: float = 1.0):
        """Learn a new pattern."""
        # Simulate learning process with complexity-dependent processing
        iterations = int(10 * complexity)
        for _ in range(iterations):
            _ = hash(str(pattern_data)) % 1000
        
        self.knowledge_base[pattern_id] = {
            'data': pattern_data,
            'learned_at': time.time(),
            'complexity': complexity,
            'confidence': random.uniform(0.7, 1.0)
        }
        
        self.learning_history.append((pattern_id, complexity))
    
    def adapt_to_context(self, context: LearningContext):
        """Adapt to a new learning context."""
        # Simulate context adaptation
        self.current_context = context
        
        for pattern_id, pattern_data in context.patterns.items():
            if pattern_id not in self.knowledge_base:
                self.learn_pattern(pattern_id, pattern_data, context.complexity)
            else:
                # Update existing knowledge
                self.knowledge_base[pattern_id]['confidence'] *= 1.1
                self.knowledge_base[pattern_id]['confidence'] = min(1.0, self.knowledge_base[pattern_id]['confidence'])
    
    def recall_pattern(self, pattern_id: str) -> Tuple[bool, float]:
        """Recall a learned pattern."""
        if pattern_id in self.knowledge_base:
            confidence = self.knowledge_base[pattern_id]['confidence']
            # Simulate recall decay
            age = time.time() - self.knowledge_base[pattern_id]['learned_at']
            decay_factor = math.exp(-age / 1000)
            return True, confidence * decay_factor
        return False, 0.0
    
    def switch_context(self, new_context: LearningContext) -> float:
        """Switch to a new context and measure adaptation cost."""
        old_context = self.current_context
        self.adapt_to_context(new_context)
        
        # Calculate switching cost based on context difference
        if old_context:
            shared_patterns = set(old_context.patterns.keys()) & set(new_context.patterns.keys())
            switching_cost = 1.0 - (len(shared_patterns) / max(len(old_context.patterns), len(new_context.patterns)))
        else:
            switching_cost = 1.0
        
        return switching_cost
    
    def generate_adaptive_response(self, input_data: Any) -> Any:
        """Generate an adaptive response based on current knowledge."""
        # Use knowledge base to generate response
        response_quality = len(self.knowledge_base) / (len(self.knowledge_base) + 1)
        
        if self.current_context:
            # Apply context-specific processing
            for rule in self.current_context.rules:
                response_quality *= random.uniform(0.9, 1.1)
        
        return {'quality': min(1.0, response_quality), 'data': str(input_data)[::-1]}


def create_learning_context(name: str, num_patterns: int, complexity: float) -> LearningContext:
    """Create a learning context with random patterns."""
    patterns = {}
    for i in range(num_patterns):
        patterns[f"{name}_pattern_{i}"] = {
            'value': random.randint(1, 100),
            'type': random.choice(['numeric', 'categorical', 'sequential']),
            'weight': random.uniform(0.1, 1.0)
        }
    
    rules = [f"rule_{i}" for i in range(int(complexity * 5))]
    
    return LearningContext(name=name, patterns=patterns, rules=rules, complexity=complexity)


def benchmark_adaptation_rate(collector: MetricsCollector, iterations: int = 50):
    """Benchmark adaptation rate to new patterns."""
    learner = AdaptiveLearner()
    complexities = [0.5, 1.0, 2.0]
    
    for complexity in complexities:
        for i in range(iterations):
            pattern_id = f"adapt_pattern_{complexity}_{i}"
            pattern_data = {'value': random.randint(1, 1000), 'complexity': complexity}
            
            with Timer(collector, f"adaptation_rate_{complexity}", "deschooling_learning"):
                learner.learn_pattern(pattern_id, pattern_data, complexity)
                success, confidence = learner.recall_pattern(pattern_id)
                
                collector.record_custom_metric("adaptation_confidence", confidence)
                collector.record_custom_metric("complexity_level", complexity)
                collector.record_custom_metric("knowledge_base_size", len(learner.knowledge_base))


def benchmark_learning_speed(collector: MetricsCollector, iterations: int = 100):
    """Benchmark learning speed across different pattern types."""
    learner = AdaptiveLearner()
    pattern_types = ['simple', 'moderate', 'complex']
    complexity_map = {'simple': 0.5, 'moderate': 1.5, 'complex': 3.0}
    
    for pattern_type in pattern_types:
        complexity = complexity_map[pattern_type]
        patterns_learned = 0
        
        for i in range(iterations):
            pattern_id = f"speed_{pattern_type}_{i}"
            pattern_data = list(range(int(10 * complexity)))
            
            with Timer(collector, f"learning_speed_{pattern_type}", "deschooling_learning"):
                learner.learn_pattern(pattern_id, pattern_data, complexity)
                patterns_learned += 1
                
                collector.record_custom_metric("patterns_learned", patterns_learned)
                collector.record_custom_metric("learning_efficiency", patterns_learned / (i + 1))


def benchmark_flexibility(collector: MetricsCollector, iterations: int = 30):
    """Benchmark flexibility in handling diverse pattern types."""
    learner = AdaptiveLearner()
    pattern_varieties = ['numeric', 'text', 'mixed', 'nested']
    
    for i in range(iterations):
        for variety in pattern_varieties:
            if variety == 'numeric':
                pattern_data = [random.random() for _ in range(10)]
            elif variety == 'text':
                pattern_data = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=20))
            elif variety == 'mixed':
                pattern_data = {'num': random.random(), 'text': 'data', 'list': [1, 2, 3]}
            else:  # nested
                pattern_data = {'level1': {'level2': {'level3': [1, 2, 3]}}}
            
            with Timer(collector, f"flexibility_{variety}", "deschooling_learning"):
                learner.learn_pattern(f"flex_{variety}_{i}", pattern_data, 1.0)
                collector.record_custom_metric("pattern_variety", len(pattern_varieties))
                collector.record_custom_metric("total_patterns", len(learner.knowledge_base))


def benchmark_new_pattern_learning(collector: MetricsCollector, iterations: int = 50):
    """Benchmark ability to learn completely new patterns."""
    learner = AdaptiveLearner()
    
    for i in range(iterations):
        # Create increasingly novel patterns
        novelty_factor = 1 + (i / iterations)
        pattern_size = int(10 * novelty_factor)
        pattern_data = {
            'structure': [random.random() for _ in range(pattern_size)],
            'metadata': {'novelty': novelty_factor, 'timestamp': time.time()}
        }
        
        with Timer(collector, "new_pattern_learning", "deschooling_learning"):
            learner.learn_pattern(f"novel_pattern_{i}", pattern_data, novelty_factor)
            
            collector.record_custom_metric("novelty_factor", novelty_factor)
            collector.record_custom_metric("pattern_size", pattern_size)
            collector.record_custom_metric("accumulated_knowledge", len(learner.knowledge_base))


def benchmark_context_switching(collector: MetricsCollector, iterations: int = 30):
    """Benchmark context switching capabilities."""
    learner = AdaptiveLearner()
    
    contexts = [
        create_learning_context("math", 5, 1.0),
        create_learning_context("language", 7, 1.5),
        create_learning_context("logic", 6, 2.0),
        create_learning_context("creative", 8, 1.2)
    ]
    
    for i in range(iterations):
        old_context_idx = i % len(contexts)
        new_context_idx = (i + 1) % len(contexts)
        
        with Timer(collector, "context_switching", "deschooling_learning"):
            switching_cost = learner.switch_context(contexts[new_context_idx])
            
            collector.record_custom_metric("switching_cost", switching_cost)
            collector.record_custom_metric("context_complexity", contexts[new_context_idx].complexity)
            collector.record_custom_metric("context_patterns", len(contexts[new_context_idx].patterns))


def benchmark_adaptive_responses(collector: MetricsCollector, iterations: int = 100):
    """Benchmark adaptive response generation."""
    learner = AdaptiveLearner()
    
    # Pre-populate with knowledge
    context = create_learning_context("response_test", 10, 1.5)
    learner.adapt_to_context(context)
    
    for i in range(iterations):
        input_data = {
            'query': f"test_query_{i}",
            'context_id': random.randint(1, 5),
            'params': [random.random() for _ in range(5)]
        }
        
        with Timer(collector, "adaptive_responses", "deschooling_learning"):
            response = learner.generate_adaptive_response(input_data)
            
            collector.record_custom_metric("response_quality", response['quality'])
            collector.record_custom_metric("knowledge_utilized", len(learner.knowledge_base))


def run_all_benchmarks(mode: str = "comprehensive"):
    """Run all learning adaptation benchmarks."""
    collector = MetricsCollector()
    
    iterations = {
        "quick": {
            "adaptation": 10, "speed": 20, "flexibility": 10, 
            "new_pattern": 10, "context_switch": 10, "adaptive_response": 20
        },
        "comprehensive": {
            "adaptation": 50, "speed": 100, "flexibility": 30,
            "new_pattern": 50, "context_switch": 30, "adaptive_response": 100
        }
    }
    
    iters = iterations.get(mode, iterations["comprehensive"])
    
    print(f"Running Deschooling Learning Adaptation Benchmarks (mode: {mode})...")
    
    print("  - Adaptation rate...")
    benchmark_adaptation_rate(collector, iters["adaptation"])
    
    print("  - Learning speed...")
    benchmark_learning_speed(collector, iters["speed"])
    
    print("  - Flexibility...")
    benchmark_flexibility(collector, iters["flexibility"])
    
    print("  - New pattern learning...")
    benchmark_new_pattern_learning(collector, iters["new_pattern"])
    
    print("  - Context switching...")
    benchmark_context_switching(collector, iters["context_switch"])
    
    print("  - Adaptive responses...")
    benchmark_adaptive_responses(collector, iters["adaptive_response"])
    
    return collector.get_all_results()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Deschooling Learning Adaptation Benchmarks")
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
