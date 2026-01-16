"""
Performance Profiler for OCTO-AGI Benchmarks

Detailed profiling tools for bottleneck identification and resource utilization analysis.
"""

import time
import psutil
import os
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from collections import defaultdict
import tracemalloc


@dataclass
class ProfileSnapshot:
    """A snapshot of system resources at a point in time."""
    timestamp: float
    cpu_percent: float
    memory_mb: float
    memory_percent: float
    thread_count: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'timestamp': self.timestamp,
            'cpu_percent': self.cpu_percent,
            'memory_mb': self.memory_mb,
            'memory_percent': self.memory_percent,
            'thread_count': self.thread_count,
        }


@dataclass
class FunctionProfile:
    """Profile data for a specific function."""
    name: str
    call_count: int = 0
    total_time: float = 0.0
    min_time: float = float('inf')
    max_time: float = 0.0
    avg_time: float = 0.0
    
    def add_call(self, duration: float):
        """Record a function call."""
        self.call_count += 1
        self.total_time += duration
        self.min_time = min(self.min_time, duration)
        self.max_time = max(self.max_time, duration)
        self.avg_time = self.total_time / self.call_count
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'call_count': self.call_count,
            'total_time_ms': self.total_time * 1000,
            'min_time_ms': self.min_time * 1000 if self.min_time != float('inf') else 0,
            'max_time_ms': self.max_time * 1000,
            'avg_time_ms': self.avg_time * 1000,
        }


class PerformanceProfiler:
    """
    Detailed performance profiler for OCTO-AGI benchmarks.
    
    Features:
    - Resource utilization tracking
    - Function-level profiling
    - Bottleneck identification
    - Memory allocation tracking
    - Timeline snapshots
    """
    
    def __init__(self, enable_memory_tracking: bool = True):
        self.enable_memory_tracking = enable_memory_tracking
        self._process = psutil.Process(os.getpid())
        self._snapshots: List[ProfileSnapshot] = []
        self._function_profiles: Dict[str, FunctionProfile] = {}
        self._is_profiling = False
        self._profile_start_time: Optional[float] = None
        
        if self.enable_memory_tracking:
            tracemalloc.start()
    
    def start(self):
        """Start profiling session."""
        self._is_profiling = True
        self._profile_start_time = time.perf_counter()
        self._snapshots.clear()
        self._function_profiles.clear()
        self._take_snapshot()
    
    def stop(self):
        """Stop profiling session."""
        self._is_profiling = False
        self._take_snapshot()  # Final snapshot
    
    def _take_snapshot(self):
        """Capture current resource usage snapshot."""
        if not self._is_profiling and len(self._snapshots) > 0:
            # Only take final snapshot if we have previous ones
            pass
        
        snapshot = ProfileSnapshot(
            timestamp=time.perf_counter() - (self._profile_start_time or 0),
            cpu_percent=self._process.cpu_percent(),
            memory_mb=self._process.memory_info().rss / (1024 * 1024),
            memory_percent=self._process.memory_percent(),
            thread_count=self._process.num_threads(),
        )
        self._snapshots.append(snapshot)
    
    def profile_function(self, func: Callable) -> Callable:
        """
        Decorator to profile a function.
        
        Usage:
            profiler = PerformanceProfiler()
            
            @profiler.profile_function
            def my_function():
                pass
        """
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                duration = time.perf_counter() - start
                func_name = func.__name__
                
                if func_name not in self._function_profiles:
                    self._function_profiles[func_name] = FunctionProfile(name=func_name)
                
                self._function_profiles[func_name].add_call(duration)
        
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper
    
    def record_function_call(self, name: str, duration: float):
        """Manually record a function call."""
        if name not in self._function_profiles:
            self._function_profiles[name] = FunctionProfile(name=name)
        self._function_profiles[name].add_call(duration)
    
    def get_snapshots(self) -> List[ProfileSnapshot]:
        """Get all resource snapshots."""
        return self._snapshots
    
    def get_function_profiles(self) -> Dict[str, FunctionProfile]:
        """Get all function profiles."""
        return self._function_profiles
    
    def get_bottlenecks(self, top_n: int = 10) -> List[FunctionProfile]:
        """
        Identify performance bottlenecks.
        
        Returns the top N functions by total time spent.
        """
        sorted_profiles = sorted(
            self._function_profiles.values(),
            key=lambda p: p.total_time,
            reverse=True
        )
        return sorted_profiles[:top_n]
    
    def get_resource_summary(self) -> Dict[str, Any]:
        """Get summary of resource utilization."""
        if not self._snapshots:
            return {}
        
        cpu_values = [s.cpu_percent for s in self._snapshots]
        memory_values = [s.memory_mb for s in self._snapshots]
        
        return {
            'duration_seconds': self._snapshots[-1].timestamp if self._snapshots else 0,
            'cpu': {
                'mean_percent': sum(cpu_values) / len(cpu_values) if cpu_values else 0,
                'max_percent': max(cpu_values) if cpu_values else 0,
                'min_percent': min(cpu_values) if cpu_values else 0,
            },
            'memory': {
                'peak_mb': max(memory_values) if memory_values else 0,
                'mean_mb': sum(memory_values) / len(memory_values) if memory_values else 0,
                'min_mb': min(memory_values) if memory_values else 0,
            },
            'snapshots_count': len(self._snapshots),
        }
    
    def get_memory_allocations(self) -> Optional[List[tuple]]:
        """
        Get top memory allocations.
        
        Returns None if memory tracking is disabled.
        """
        if not self.enable_memory_tracking:
            return None
        
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')
        return [(str(stat), stat.size / 1024) for stat in top_stats[:10]]
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive profiling report."""
        report = {
            'resource_summary': self.get_resource_summary(),
            'function_profiles': {
                name: profile.to_dict()
                for name, profile in self._function_profiles.items()
            },
            'bottlenecks': [
                profile.to_dict()
                for profile in self.get_bottlenecks(10)
            ],
            'timeline': [
                snapshot.to_dict()
                for snapshot in self._snapshots
            ],
        }
        
        if self.enable_memory_tracking:
            allocations = self.get_memory_allocations()
            if allocations:
                report['top_memory_allocations'] = [
                    {'location': loc, 'size_kb': size}
                    for loc, size in allocations
                ]
        
        return report
    
    def reset(self):
        """Reset profiler state."""
        self._snapshots.clear()
        self._function_profiles.clear()
        self._is_profiling = False
        self._profile_start_time = None
    
    def __del__(self):
        """Cleanup on deletion."""
        if self.enable_memory_tracking:
            tracemalloc.stop()


class SimpleProfiler:
    """
    Simplified profiler for quick performance checks.
    
    Usage:
        with SimpleProfiler("My Operation") as profiler:
            # Code to profile
            pass
        print(f"Duration: {profiler.duration_ms}ms")
    """
    
    def __init__(self, name: str):
        self.name = name
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.duration_ms: float = 0.0
    
    def __enter__(self):
        self.start_time = time.perf_counter()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.perf_counter()
        if self.start_time:
            self.duration_ms = (self.end_time - self.start_time) * 1000
    
    def __str__(self):
        return f"{self.name}: {self.duration_ms:.2f}ms"
