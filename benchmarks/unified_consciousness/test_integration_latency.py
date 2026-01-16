"""
Integration Latency Benchmarks

Tests performance overhead of system integration.
Measures latency overhead and throughput impact for minimal,
standard, and full integration scenarios.
"""

import time
import random
import sys
import os
from typing import Dict, List, Any, Callable
from dataclasses import dataclass
from collections import deque

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.metrics_collector import MetricsCollector, Timer


@dataclass
class Message:
    """Represents a message between subsystems."""
    source: str
    destination: str
    payload: Dict[str, Any]
    timestamp: float
    priority: int = 0
    
    def size_bytes(self) -> int:
        """Estimate message size in bytes."""
        # Simple estimation
        return len(str(self.payload).encode('utf-8'))


class MessageBus:
    """Message bus for inter-subsystem communication."""
    
    def __init__(self, max_queue_size: int = 1000):
        self.queues: Dict[str, deque] = {}
        self.max_queue_size = max_queue_size
        self.message_count = 0
        self.total_latency = 0.0
    
    def register_subsystem(self, system_id: str):
        """Register a subsystem with the message bus."""
        if system_id not in self.queues:
            self.queues[system_id] = deque(maxlen=self.max_queue_size)
    
    def send_message(self, message: Message) -> float:
        """Send a message and return latency."""
        start_time = time.perf_counter()
        
        if message.destination in self.queues:
            self.queues[message.destination].append(message)
            self.message_count += 1
        
        latency = time.perf_counter() - start_time
        self.total_latency += latency
        return latency
    
    def receive_message(self, system_id: str) -> Message | None:
        """Receive a message for a subsystem."""
        if system_id in self.queues and self.queues[system_id]:
            return self.queues[system_id].popleft()
        return None
    
    def get_queue_depth(self, system_id: str) -> int:
        """Get current queue depth for a subsystem."""
        return len(self.queues.get(system_id, []))
    
    def get_average_latency(self) -> float:
        """Get average message latency."""
        if self.message_count == 0:
            return 0.0
        return self.total_latency / self.message_count


class IntegrationLayer:
    """Manages integration between subsystems."""
    
    def __init__(self, integration_level: str = "standard"):
        self.integration_level = integration_level
        self.message_bus = MessageBus()
        self.subsystems: List[str] = []
        self.processing_overhead = 0.0
        
        # Configure based on integration level
        self.config = self._get_config(integration_level)
    
    def _get_config(self, level: str) -> Dict[str, Any]:
        """Get configuration for integration level."""
        configs = {
            "minimal": {
                "sync_frequency": 10,
                "validation_enabled": False,
                "transformation_enabled": False,
                "batching_enabled": False,
            },
            "standard": {
                "sync_frequency": 5,
                "validation_enabled": True,
                "transformation_enabled": True,
                "batching_enabled": False,
            },
            "full": {
                "sync_frequency": 1,
                "validation_enabled": True,
                "transformation_enabled": True,
                "batching_enabled": True,
            }
        }
        return configs.get(level, configs["standard"])
    
    def add_subsystem(self, system_id: str):
        """Add a subsystem to the integration layer."""
        if system_id not in self.subsystems:
            self.subsystems.append(system_id)
            self.message_bus.register_subsystem(system_id)
    
    def process_message(self, message: Message) -> float:
        """Process a message through the integration layer."""
        start_time = time.perf_counter()
        
        # Validation overhead
        if self.config["validation_enabled"]:
            self._validate_message(message)
        
        # Transformation overhead
        if self.config["transformation_enabled"]:
            message = self._transform_message(message)
        
        # Send through message bus
        bus_latency = self.message_bus.send_message(message)
        
        total_latency = time.perf_counter() - start_time
        self.processing_overhead += total_latency - bus_latency
        
        return total_latency
    
    def _validate_message(self, message: Message):
        """Validate message (simulated overhead)."""
        # Simulate validation work
        _ = message.source and message.destination and message.payload
        time.sleep(0.0001)  # Small delay to simulate validation
    
    def _transform_message(self, message: Message) -> Message:
        """Transform message (simulated overhead)."""
        # Simulate transformation work
        transformed_payload = {k: v for k, v in message.payload.items()}
        time.sleep(0.0001)  # Small delay to simulate transformation
        message.payload = transformed_payload
        return message
    
    def batch_process_messages(self, messages: List[Message]) -> float:
        """Process multiple messages in batch."""
        if not self.config["batching_enabled"]:
            # Process individually
            total_latency = sum(self.process_message(msg) for msg in messages)
            return total_latency
        
        # Batch processing
        start_time = time.perf_counter()
        
        # Batch validation
        if self.config["validation_enabled"]:
            for msg in messages:
                self._validate_message(msg)
        
        # Batch transformation
        if self.config["transformation_enabled"]:
            messages = [self._transform_message(msg) for msg in messages]
        
        # Send all messages
        for msg in messages:
            self.message_bus.send_message(msg)
        
        return time.perf_counter() - start_time
    
    def measure_throughput(self, duration_seconds: float = 0.1) -> float:
        """Measure message throughput."""
        messages_sent = 0
        start_time = time.perf_counter()
        
        while time.perf_counter() - start_time < duration_seconds:
            if len(self.subsystems) >= 2:
                source = random.choice(self.subsystems)
                dest = random.choice([s for s in self.subsystems if s != source])
                
                msg = Message(
                    source=source,
                    destination=dest,
                    payload={"data": random.random()},
                    timestamp=time.time()
                )
                
                self.process_message(msg)
                messages_sent += 1
        
        actual_duration = time.perf_counter() - start_time
        return messages_sent / actual_duration if actual_duration > 0 else 0.0


def benchmark_minimal_integration(collector: MetricsCollector, iterations: int = 50):
    """Benchmark minimal integration overhead."""
    for i in range(iterations):
        with Timer(collector, "minimal_integration", "unified_consciousness"):
            layer = IntegrationLayer("minimal")
            layer.add_subsystem("UMG")
            layer.add_subsystem("Spatial")
            
            # Send messages
            latencies = []
            for _ in range(20):
                msg = Message(
                    source="UMG",
                    destination="Spatial",
                    payload={"value": random.random()},
                    timestamp=time.time()
                )
                latency = layer.process_message(msg)
                latencies.append(latency)
            
            avg_latency = sum(latencies) / len(latencies)
            throughput = layer.measure_throughput(0.05)
            
            collector.record_custom_metric("latency_overhead_ms", avg_latency * 1000)
            collector.record_custom_metric("throughput_msg_per_sec", throughput)
            collector.record_custom_metric("messages_processed", len(latencies))
            collector.record_custom_metric("integration_level", 1)  # minimal = 1


def benchmark_standard_integration(collector: MetricsCollector, iterations: int = 40):
    """Benchmark standard integration overhead."""
    for i in range(iterations):
        with Timer(collector, "standard_integration", "unified_consciousness"):
            layer = IntegrationLayer("standard")
            layer.add_subsystem("UMG")
            layer.add_subsystem("Spatial")
            layer.add_subsystem("Learning")
            
            # Send messages with validation and transformation
            latencies = []
            for _ in range(30):
                source = random.choice(layer.subsystems)
                dest = random.choice([s for s in layer.subsystems if s != source])
                
                msg = Message(
                    source=source,
                    destination=dest,
                    payload={"data": [random.random() for _ in range(5)]},
                    timestamp=time.time(),
                    priority=random.randint(0, 5)
                )
                latency = layer.process_message(msg)
                latencies.append(latency)
            
            avg_latency = sum(latencies) / len(latencies)
            throughput = layer.measure_throughput(0.05)
            processing_overhead = layer.processing_overhead / len(latencies)
            
            collector.record_custom_metric("latency_overhead_ms", avg_latency * 1000)
            collector.record_custom_metric("throughput_msg_per_sec", throughput)
            collector.record_custom_metric("processing_overhead_ms", processing_overhead * 1000)
            collector.record_custom_metric("messages_processed", len(latencies))
            collector.record_custom_metric("integration_level", 2)  # standard = 2


def benchmark_full_integration(collector: MetricsCollector, iterations: int = 30):
    """Benchmark full integration overhead with batching."""
    for i in range(iterations):
        with Timer(collector, "full_integration", "unified_consciousness"):
            layer = IntegrationLayer("full")
            
            # Add multiple subsystems
            for sys in ["UMG", "Spatial", "Learning"]:
                for instance in range(2):
                    layer.add_subsystem(f"{sys}_{instance}")
            
            # Batch processing
            batch_sizes = [10, 20, 30]
            all_latencies = []
            
            for batch_size in batch_sizes:
                messages = []
                for _ in range(batch_size):
                    source = random.choice(layer.subsystems)
                    dest = random.choice([s for s in layer.subsystems if s != source])
                    
                    msg = Message(
                        source=source,
                        destination=dest,
                        payload={"data": [random.random() for _ in range(10)]},
                        timestamp=time.time(),
                        priority=random.randint(0, 10)
                    )
                    messages.append(msg)
                
                batch_latency = layer.batch_process_messages(messages)
                all_latencies.append(batch_latency / batch_size)  # Per-message latency
            
            avg_latency = sum(all_latencies) / len(all_latencies)
            throughput = layer.measure_throughput(0.05)
            bus_avg_latency = layer.message_bus.get_average_latency()
            
            collector.record_custom_metric("latency_overhead_ms", avg_latency * 1000)
            collector.record_custom_metric("throughput_msg_per_sec", throughput)
            collector.record_custom_metric("bus_latency_ms", bus_avg_latency * 1000)
            collector.record_custom_metric("subsystem_count", len(layer.subsystems))
            collector.record_custom_metric("integration_level", 3)  # full = 3


def benchmark_latency_scaling(collector: MetricsCollector, iterations: int = 20):
    """Benchmark latency scaling with subsystem count."""
    for i in range(iterations):
        subsystem_counts = [2, 4, 6, 8]
        
        for count in subsystem_counts:
            with Timer(collector, f"latency_scaling_{count}", "unified_consciousness"):
                layer = IntegrationLayer("standard")
                
                # Add subsystems
                for j in range(count):
                    layer.add_subsystem(f"System_{j}")
                
                # Measure latency
                latencies = []
                for _ in range(15):
                    source = random.choice(layer.subsystems)
                    dest = random.choice([s for s in layer.subsystems if s != source])
                    
                    msg = Message(
                        source=source,
                        destination=dest,
                        payload={"data": random.random()},
                        timestamp=time.time()
                    )
                    latency = layer.process_message(msg)
                    latencies.append(latency)
                
                avg_latency = sum(latencies) / len(latencies)
                
                collector.record_custom_metric("latency_overhead_ms", avg_latency * 1000)
                collector.record_custom_metric("subsystem_count", count)
                collector.record_custom_metric("latency_per_subsystem", avg_latency * 1000 / count)


def benchmark_throughput_impact(collector: MetricsCollector, iterations: int = 25):
    """Benchmark throughput impact of different integration levels."""
    integration_levels = ["minimal", "standard", "full"]
    
    for level in integration_levels:
        for i in range(iterations):
            with Timer(collector, f"throughput_{level}", "unified_consciousness"):
                layer = IntegrationLayer(level)
                
                # Add subsystems
                for sys in ["UMG", "Spatial", "Learning"]:
                    layer.add_subsystem(sys)
                
                # Measure throughput over longer duration
                throughput = layer.measure_throughput(0.1)
                
                # Also measure message sizes
                msg_sizes = []
                for _ in range(10):
                    msg = Message(
                        source="UMG",
                        destination="Spatial",
                        payload={"data": [random.random() for _ in range(10)]},
                        timestamp=time.time()
                    )
                    msg_sizes.append(msg.size_bytes())
                
                avg_msg_size = sum(msg_sizes) / len(msg_sizes)
                
                collector.record_custom_metric("throughput_msg_per_sec", throughput)
                collector.record_custom_metric("avg_message_size_bytes", avg_msg_size)
                collector.record_custom_metric("throughput_bytes_per_sec", throughput * avg_msg_size)
                collector.record_custom_metric("integration_level", 
                                              {"minimal": 1, "standard": 2, "full": 3}[level])


def run_all_benchmarks(mode: str = "comprehensive"):
    """Run all integration latency benchmarks."""
    collector = MetricsCollector()
    
    iterations = {
        "quick": {"minimal": 10, "standard": 8, "full": 5, "scaling": 5, "throughput": 8},
        "comprehensive": {"minimal": 50, "standard": 40, "full": 30, "scaling": 20, "throughput": 25}
    }
    
    iters = iterations.get(mode, iterations["comprehensive"])
    
    print(f"Running Integration Latency Benchmarks (mode: {mode})...")
    
    print("  - Minimal integration...")
    benchmark_minimal_integration(collector, iters["minimal"])
    
    print("  - Standard integration...")
    benchmark_standard_integration(collector, iters["standard"])
    
    print("  - Full integration...")
    benchmark_full_integration(collector, iters["full"])
    
    print("  - Latency scaling...")
    benchmark_latency_scaling(collector, iters["scaling"])
    
    print("  - Throughput impact...")
    benchmark_throughput_impact(collector, iters["throughput"])
    
    return collector.get_all_results()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Integration Latency Benchmarks")
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
            if 'latency_overhead_ms' in summary['custom_metrics']:
                latency = summary['custom_metrics']['latency_overhead_ms']
                print(f"  Latency overhead: {latency['mean']:.3f}ms")
            if 'throughput_msg_per_sec' in summary['custom_metrics']:
                throughput = summary['custom_metrics']['throughput_msg_per_sec']
                print(f"  Throughput: {throughput['mean']:.1f} msg/sec")
