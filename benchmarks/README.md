# OCTO-AGI Benchmark Suite

A comprehensive benchmark suite for measuring and validating the performance of the OCTO-AGI system across all its core components.

## Overview

This benchmark suite provides performance testing and validation for:

- **UMG (Universal Module Graph) Reasoning**: Graph traversal, reasoning depth, and memory efficiency
- **Tetrahedral Spatial Reasoning**: 3D spatial processing, multi-dimensional mapping, and geometric inference
- **Deschooling Learning**: Learning adaptation, knowledge retention, and creative problem solving
- **Unified Consciousness Integration**: Cross-system coherence, integration latency, and emergent behavior

## Quick Start

### Running All Benchmarks

```bash
python benchmarks/run_all_benchmarks.py
```

### Running Specific Benchmark Categories

```bash
# UMG Reasoning benchmarks only
python benchmarks/run_all_benchmarks.py --category umg_reasoning

# Tetrahedral Spatial benchmarks only
python benchmarks/run_all_benchmarks.py --category tetrahedral_spatial

# Deschooling Learning benchmarks only
python benchmarks/run_all_benchmarks.py --category deschooling_learning

# Unified Consciousness benchmarks only
python benchmarks/run_all_benchmarks.py --category unified_consciousness
```

### Running Individual Benchmarks

```bash
# Using pytest
pytest benchmarks/umg_reasoning/test_module_graph_traversal.py -v

# Direct execution
python benchmarks/umg_reasoning/test_module_graph_traversal.py
```

### Quick vs Comprehensive Runs

```bash
# Quick run (reduced iterations, faster)
python benchmarks/run_all_benchmarks.py --mode quick

# Comprehensive run (full iterations, slower but more accurate)
python benchmarks/run_all_benchmarks.py --mode comprehensive
```

## Understanding Results

### Performance Metrics

Each benchmark reports the following metrics:

- **Execution Time**: Average, median, min, max execution times
- **Memory Usage**: Peak memory consumption, memory efficiency
- **CPU Usage**: Average CPU utilization
- **Throughput**: Operations per second
- **Accuracy**: Quality metrics specific to each benchmark

### Result Files

Results are saved in the `benchmarks/results/` directory:

- **JSON Reports**: Machine-readable detailed results
- **Markdown Reports**: Human-readable summary reports
- **Visualizations**: Charts and graphs in `benchmarks/results/visualizations/`

### Performance Baselines

Current performance targets:

#### UMG Reasoning
- **Graph Traversal**: < 100ms for 1000 nodes, < 50MB memory
- **Reasoning Depth**: > 90% accuracy, < 200ms per inference
- **Memory Efficiency**: < 1MB per 100 nodes

#### Tetrahedral Spatial
- **3D Processing**: < 50ms for 1000 points, > 95% accuracy
- **Multi-dimensional Mapping**: < 100ms, > 90% relationship accuracy
- **Geometric Inference**: < 150ms, > 85% spatial reasoning accuracy

#### Deschooling Learning
- **Learning Adaptation**: > 80% adaptation rate
- **Knowledge Retention**: > 90% retention after 1000 iterations
- **Creative Problem Solving**: > 3 novel solutions per problem

#### Unified Consciousness
- **Cross-System Coherence**: > 95% coherence score
- **Integration Latency**: < 20ms overhead
- **Emergent Behavior**: Trackable novel behaviors

## Benchmark Details

### UMG Reasoning Benchmarks

#### Module Graph Traversal
Tests the speed and efficiency of navigating the Universal Module Graph.

**Metrics**: Traversal time, memory usage, path accuracy

**Test Cases**:
- Small graphs (100 nodes)
- Medium graphs (1,000 nodes)
- Large graphs (10,000 nodes)
- Complex graphs (multiple connections per node)

#### Reasoning Depth
Measures the quality and depth of logical reasoning capabilities.

**Metrics**: Inference accuracy, reasoning steps, time per inference

**Test Cases**:
- Simple logical chains (2-3 steps)
- Medium complexity (5-10 steps)
- Complex reasoning (10+ steps)

#### Memory Efficiency
Evaluates RAM usage and optimization during operations.

**Metrics**: Peak memory, average memory, memory per node

**Test Cases**:
- Memory scaling with graph size
- Memory cleanup after operations
- Concurrent operation memory usage

### Tetrahedral Spatial Benchmarks

#### 3D Spatial Processing
Tests the speed of 3D computational operations.

**Metrics**: Processing time, accuracy, throughput

**Test Cases**:
- Point cloud processing
- Volumetric calculations
- Spatial transformations

#### Multi-dimensional Mapping
Evaluates relationship mapping accuracy across dimensions.

**Metrics**: Mapping accuracy, time, relationship preservation

**Test Cases**:
- 2D to 3D mapping
- 3D to 4D mapping
- Complex relationship networks

#### Geometric Inference
Assesses spatial reasoning quality.

**Metrics**: Inference accuracy, time, spatial understanding

**Test Cases**:
- Shape recognition
- Spatial relationship inference
- Geometric problem solving

### Deschooling Learning Benchmarks

#### Learning Adaptation
Tests human-centric learning metrics and adaptation capabilities.

**Metrics**: Adaptation rate, learning speed, flexibility

**Test Cases**:
- New pattern learning
- Context switching
- Adaptive responses

#### Knowledge Retention
Measures long-term memory performance.

**Metrics**: Retention rate, recall accuracy, decay rate

**Test Cases**:
- Short-term retention (100 iterations)
- Medium-term retention (1,000 iterations)
- Long-term retention (10,000 iterations)

#### Creative Problem Solving
Evaluates novel solution generation.

**Metrics**: Solution count, novelty score, quality

**Test Cases**:
- Open-ended problems
- Constraint-based problems
- Multi-solution problems

### Unified Consciousness Benchmarks

#### Cross-System Coherence
Tests integration quality across all subsystems.

**Metrics**: Coherence score, consistency, integration quality

**Test Cases**:
- Two-system integration
- Three-system integration
- Full system integration

#### Integration Latency
Measures performance overhead of system integration.

**Metrics**: Latency overhead, throughput impact

**Test Cases**:
- Minimal integration
- Standard integration
- Full integration

#### Emergent Behavior
Tracks unexpected capabilities and behaviors.

**Metrics**: Novel behavior count, behavior quality

**Test Cases**:
- Complex scenario testing
- Edge case discovery
- Capability emergence tracking

## Configuration

Benchmark configuration is managed in `benchmarks/config/benchmark_config.yaml`.

Key configuration options:

```yaml
general:
  output_directory: "benchmarks/results"
  save_visualizations: true
  mode: "comprehensive"  # or "quick"
  
performance_thresholds:
  umg_reasoning:
    graph_traversal_ms: 100
    memory_per_node_kb: 10
  # ... other thresholds
```

## Development

### Adding New Benchmarks

1. Create a new test file in the appropriate category directory
2. Implement benchmark functions using the `@benchmark` decorator
3. Use `MetricsCollector` to track performance metrics
4. Add configuration to `benchmark_config.yaml`
5. Update this README

### Benchmark Best Practices

- Use the `Timer` context manager for accurate timing
- Call `MetricsCollector.reset()` between test runs
- Generate reproducible test data
- Document expected performance ranges
- Include both positive and edge cases

## Dependencies

Required Python packages:

```
pytest>=7.0.0
pyyaml>=6.0
psutil>=5.9.0
numpy>=1.20.0
matplotlib>=3.5.0
```

Install with:

```bash
pip install pytest pyyaml psutil numpy matplotlib
```

## Troubleshooting

### Common Issues

**Issue**: Benchmarks run slowly
- **Solution**: Try using `--mode quick` for faster iterations

**Issue**: Memory errors on large tests
- **Solution**: Reduce test size in configuration or increase system memory

**Issue**: Results not saved
- **Solution**: Check write permissions on `benchmarks/results/` directory

### Getting Help

For issues or questions:
1. Check the configuration in `benchmark_config.yaml`
2. Review benchmark-specific documentation
3. Check the results for error messages
4. Open an issue in the repository

## License

Same as the OCTO-AGI-DEMO project license.
