"""
Deschooling Knowledge Retention Benchmarks

Tests long-term memory performance including retention rate, recall accuracy,
and decay rate. Tests short-term (100 iterations), medium-term (1000 iterations),
and long-term (simulated 10000 iterations) retention.
"""

import time
import random
import math
import sys
import os
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, field

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.metrics_collector import MetricsCollector, Timer


@dataclass
class MemoryItem:
    """Represents an item stored in memory."""
    item_id: str
    data: Any
    timestamp: float
    access_count: int = 0
    strength: float = 1.0
    importance: float = 1.0
    
    def decay(self, current_time: float, decay_rate: float = 0.0001):
        """Apply time-based decay to memory strength."""
        time_elapsed = current_time - self.timestamp
        self.strength *= math.exp(-decay_rate * time_elapsed)
    
    def reinforce(self, boost: float = 0.1):
        """Reinforce memory strength through recall."""
        self.strength = min(1.0, self.strength + boost)
        self.access_count += 1


class LongTermMemory:
    """Simulates a long-term memory system with retention and decay."""
    
    def __init__(self, decay_rate: float = 0.0001):
        self.storage: Dict[str, MemoryItem] = {}
        self.decay_rate = decay_rate
        self.total_stored: int = 0
        self.total_recalled: int = 0
        self.successful_recalls: int = 0
    
    def store(self, item_id: str, data: Any, importance: float = 1.0):
        """Store an item in long-term memory."""
        memory_item = MemoryItem(
            item_id=item_id,
            data=data,
            timestamp=time.time(),
            importance=importance,
            strength=importance
        )
        self.storage[item_id] = memory_item
        self.total_stored += 1
    
    def recall(self, item_id: str, reinforce: bool = True) -> Tuple[bool, Optional[Any], float]:
        """Attempt to recall an item from memory."""
        self.total_recalled += 1
        
        if item_id not in self.storage:
            return False, None, 0.0
        
        memory_item = self.storage[item_id]
        memory_item.decay(time.time(), self.decay_rate)
        
        # Recall success probability based on strength
        recall_threshold = 0.3
        if memory_item.strength >= recall_threshold:
            if reinforce:
                memory_item.reinforce()
            self.successful_recalls += 1
            return True, memory_item.data, memory_item.strength
        
        return False, None, memory_item.strength
    
    def get_retention_rate(self) -> float:
        """Calculate overall retention rate."""
        if self.total_recalled == 0:
            return 0.0
        return self.successful_recalls / self.total_recalled
    
    def get_recall_accuracy(self) -> float:
        """Calculate recall accuracy."""
        return self.get_retention_rate()
    
    def get_average_strength(self) -> float:
        """Get average memory strength across all items."""
        if not self.storage:
            return 0.0
        
        current_time = time.time()
        total_strength = 0.0
        
        for item in self.storage.values():
            # Calculate decayed strength without modifying
            time_elapsed = current_time - item.timestamp
            decayed_strength = item.strength * math.exp(-self.decay_rate * time_elapsed)
            total_strength += decayed_strength
        
        return total_strength / len(self.storage)
    
    def consolidate_memories(self, threshold: float = 0.2):
        """Remove weak memories (simulate forgetting)."""
        current_time = time.time()
        to_remove = []
        
        for item_id, item in self.storage.items():
            item.decay(current_time, self.decay_rate)
            if item.strength < threshold:
                to_remove.append(item_id)
        
        for item_id in to_remove:
            del self.storage[item_id]
        
        return len(to_remove)


class ShortTermMemory:
    """Simulates short-term memory with limited capacity."""
    
    def __init__(self, capacity: int = 7):
        self.capacity = capacity
        self.items: List[Tuple[str, Any, float]] = []
        self.overflow_count: int = 0
    
    def add(self, item_id: str, data: Any, importance: float = 1.0):
        """Add item to short-term memory."""
        if len(self.items) >= self.capacity:
            # Remove least important item
            self.items.sort(key=lambda x: x[2])
            self.items.pop(0)
            self.overflow_count += 1
        
        self.items.append((item_id, data, importance))
    
    def recall(self, item_id: str) -> Tuple[bool, Optional[Any]]:
        """Recall item from short-term memory."""
        for stored_id, data, _ in self.items:
            if stored_id == item_id:
                return True, data
        return False, None
    
    def transfer_to_long_term(self, ltm: LongTermMemory, threshold: float = 0.5):
        """Transfer important items to long-term memory."""
        transferred = 0
        for item_id, data, importance in self.items:
            if importance >= threshold:
                ltm.store(item_id, data, importance)
                transferred += 1
        return transferred


def benchmark_short_term_retention(collector: MetricsCollector, iterations: int = 100):
    """Benchmark short-term memory retention (100 iterations)."""
    stm = ShortTermMemory(capacity=7)
    
    for i in range(iterations):
        item_id = f"stm_item_{i}"
        data = {'value': random.randint(1, 1000), 'timestamp': time.time()}
        importance = random.uniform(0.3, 1.0)
        
        with Timer(collector, "short_term_retention", "deschooling_learning"):
            stm.add(item_id, data, importance)
            
            # Attempt to recall recent items
            recall_id = f"stm_item_{max(0, i - random.randint(0, 5))}"
            success, recalled_data = stm.recall(recall_id)
            
            collector.record_custom_metric("stm_size", len(stm.items))
            collector.record_custom_metric("stm_overflow", stm.overflow_count)
            collector.record_custom_metric("recall_success", 1.0 if success else 0.0)


def benchmark_medium_term_retention(collector: MetricsCollector, iterations: int = 1000):
    """Benchmark medium-term memory retention (1000 iterations)."""
    ltm = LongTermMemory(decay_rate=0.00005)
    
    # Store items over time
    stored_items = []
    for i in range(iterations):
        item_id = f"mtm_item_{i}"
        data = {'index': i, 'value': random.random(), 'metadata': f"data_{i}"}
        importance = random.uniform(0.5, 1.0)
        
        with Timer(collector, "medium_term_storage", "deschooling_learning"):
            ltm.store(item_id, data, importance)
            stored_items.append(item_id)
        
        # Periodically test recall
        if i % 50 == 0 and i > 0:
            recall_id = random.choice(stored_items[:i])
            with Timer(collector, "medium_term_recall", "deschooling_learning"):
                success, data, strength = ltm.recall(recall_id)
                
                collector.record_custom_metric("mtm_retention_rate", ltm.get_retention_rate())
                collector.record_custom_metric("mtm_strength", strength)
                collector.record_custom_metric("mtm_stored", len(ltm.storage))


def benchmark_long_term_retention(collector: MetricsCollector, iterations: int = 10000):
    """Benchmark long-term memory retention (simulated 10000 iterations)."""
    ltm = LongTermMemory(decay_rate=0.0001)
    
    # Simulate long-term storage with time acceleration
    stored_items = []
    time_step = 0.01  # Simulated time step
    
    for i in range(iterations):
        item_id = f"ltm_item_{i}"
        data = {'index': i, 'content': f"long_term_data_{i}"}
        importance = random.uniform(0.6, 1.0)
        
        # Store at regular intervals (every 10 iterations)
        if i % 10 == 0:
            with Timer(collector, "long_term_storage", "deschooling_learning"):
                ltm.store(item_id, data, importance)
                stored_items.append(item_id)
        
        # Test recall at intervals
        if i % 100 == 0 and stored_items:
            # Recall from different time periods
            recent_id = stored_items[-1] if stored_items else None
            mid_id = stored_items[len(stored_items) // 2] if len(stored_items) > 1 else None
            old_id = stored_items[0] if stored_items else None
            
            for recall_id, age_label in [(recent_id, 'recent'), (mid_id, 'mid'), (old_id, 'old')]:
                if recall_id:
                    with Timer(collector, f"long_term_recall_{age_label}", "deschooling_learning"):
                        success, data, strength = ltm.recall(recall_id)
                        
                        collector.record_custom_metric("ltm_retention_rate", ltm.get_retention_rate())
                        collector.record_custom_metric("ltm_strength", strength)
                        collector.record_custom_metric("ltm_age_category", 
                                                      {'recent': 1, 'mid': 2, 'old': 3}[age_label])


def benchmark_retention_rate(collector: MetricsCollector, iterations: int = 500):
    """Benchmark overall retention rate across different time scales."""
    ltm = LongTermMemory(decay_rate=0.0002)
    
    # Store items with varying importance
    for i in range(iterations):
        item_id = f"retention_item_{i}"
        data = {'value': i, 'data': random.random()}
        importance = random.choice([0.3, 0.5, 0.7, 0.9, 1.0])
        
        with Timer(collector, "retention_storage", "deschooling_learning"):
            ltm.store(item_id, data, importance)
        
        # Test retention at different intervals
        if i > 50 and i % 25 == 0:
            test_intervals = [10, 25, 50]
            for interval in test_intervals:
                if i >= interval:
                    test_id = f"retention_item_{i - interval}"
                    with Timer(collector, f"retention_test_{interval}", "deschooling_learning"):
                        success, data, strength = ltm.recall(test_id, reinforce=False)
                        
                        collector.record_custom_metric("retention_interval", interval)
                        collector.record_custom_metric("retention_success", 1.0 if success else 0.0)
                        collector.record_custom_metric("retention_strength", strength)


def benchmark_recall_accuracy(collector: MetricsCollector, iterations: int = 300):
    """Benchmark recall accuracy under different conditions."""
    ltm = LongTermMemory(decay_rate=0.00015)
    
    # Create dataset with known items
    known_items = []
    for i in range(100):
        item_id = f"accuracy_item_{i}"
        data = {'index': i, 'value': i * 2, 'label': f"label_{i}"}
        importance = random.uniform(0.5, 1.0)
        ltm.store(item_id, data, importance)
        known_items.append(item_id)
    
    # Test recall accuracy
    for i in range(iterations):
        # Mix of existing and non-existing items
        if random.random() < 0.8:
            test_id = random.choice(known_items)
            expected_exists = True
        else:
            test_id = f"nonexistent_item_{i}"
            expected_exists = False
        
        with Timer(collector, "recall_accuracy", "deschooling_learning"):
            success, data, strength = ltm.recall(test_id)
            
            # Check accuracy
            correct = (success == expected_exists) or (not expected_exists and not success)
            
            collector.record_custom_metric("recall_correct", 1.0 if correct else 0.0)
            collector.record_custom_metric("recall_strength", strength)
            collector.record_custom_metric("overall_accuracy", ltm.get_recall_accuracy())


def benchmark_decay_rate(collector: MetricsCollector, iterations: int = 200):
    """Benchmark memory decay rate over time."""
    decay_rates = [0.00005, 0.0001, 0.0002]
    
    for decay_rate in decay_rates:
        ltm = LongTermMemory(decay_rate=decay_rate)
        
        # Store initial set of items
        initial_items = []
        for i in range(50):
            item_id = f"decay_item_{decay_rate}_{i}"
            data = {'value': i}
            ltm.store(item_id, data, importance=1.0)
            initial_items.append(item_id)
        
        # Measure decay over iterations
        for i in range(iterations):
            if i % 20 == 0:
                with Timer(collector, f"decay_rate_{decay_rate}", "deschooling_learning"):
                    avg_strength = ltm.get_average_strength()
                    
                    # Sample recall
                    test_id = random.choice(initial_items)
                    success, data, strength = ltm.recall(test_id, reinforce=False)
                    
                    collector.record_custom_metric("decay_rate_param", decay_rate)
                    collector.record_custom_metric("average_strength", avg_strength)
                    collector.record_custom_metric("sample_strength", strength)
                    collector.record_custom_metric("iteration", i)


def benchmark_memory_consolidation(collector: MetricsCollector, iterations: int = 100):
    """Benchmark memory consolidation and forgetting."""
    ltm = LongTermMemory(decay_rate=0.0003)
    stm = ShortTermMemory(capacity=7)
    
    for i in range(iterations):
        # Add to short-term memory
        item_id = f"consolidate_item_{i}"
        data = {'value': random.randint(1, 1000)}
        importance = random.uniform(0.3, 1.0)
        
        with Timer(collector, "memory_consolidation", "deschooling_learning"):
            stm.add(item_id, data, importance)
            
            # Periodically consolidate to long-term memory
            if i % 10 == 0:
                transferred = stm.transfer_to_long_term(ltm, threshold=0.6)
                forgotten = ltm.consolidate_memories(threshold=0.2)
                
                collector.record_custom_metric("items_transferred", transferred)
                collector.record_custom_metric("items_forgotten", forgotten)
                collector.record_custom_metric("ltm_size", len(ltm.storage))
                collector.record_custom_metric("stm_size", len(stm.items))


def run_all_benchmarks(mode: str = "comprehensive"):
    """Run all knowledge retention benchmarks."""
    collector = MetricsCollector()
    
    iterations = {
        "quick": {
            "short_term": 50, "medium_term": 200, "long_term": 1000,
            "retention": 100, "accuracy": 100, "decay": 50, "consolidation": 30
        },
        "comprehensive": {
            "short_term": 100, "medium_term": 1000, "long_term": 10000,
            "retention": 500, "accuracy": 300, "decay": 200, "consolidation": 100
        }
    }
    
    iters = iterations.get(mode, iterations["comprehensive"])
    
    print(f"Running Deschooling Knowledge Retention Benchmarks (mode: {mode})...")
    
    print("  - Short-term retention (100 iterations)...")
    benchmark_short_term_retention(collector, iters["short_term"])
    
    print("  - Medium-term retention (1000 iterations)...")
    benchmark_medium_term_retention(collector, iters["medium_term"])
    
    print("  - Long-term retention (10000 iterations simulated)...")
    benchmark_long_term_retention(collector, iters["long_term"])
    
    print("  - Retention rate...")
    benchmark_retention_rate(collector, iters["retention"])
    
    print("  - Recall accuracy...")
    benchmark_recall_accuracy(collector, iters["accuracy"])
    
    print("  - Decay rate...")
    benchmark_decay_rate(collector, iters["decay"])
    
    print("  - Memory consolidation...")
    benchmark_memory_consolidation(collector, iters["consolidation"])
    
    return collector.get_all_results()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Deschooling Knowledge Retention Benchmarks")
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
