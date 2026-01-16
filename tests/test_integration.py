"""
Comprehensive integration test for the OCTO-AGI system.
Tests all three components working together in unified consciousness.
"""

from octo_agi import UnifiedConsciousness
import json


def test_unified_consciousness_integration():
    """Test the complete unified consciousness system."""
    print("\n" + "="*70)
    print("COMPREHENSIVE INTEGRATION TEST")
    print("="*70 + "\n")
    
    # Initialize the system
    print("1. Initializing Unified Consciousness System...")
    consciousness = UnifiedConsciousness()
    print("   ✓ System initialized\n")
    
    # Test 1: System Status
    print("2. Testing System Status...")
    status = consciousness.get_system_status()
    assert status["status"] == "active"
    assert "umg" in status["components"]
    assert "spatial" in status["components"]
    assert "learning" in status["components"]
    print(f"   ✓ All three components active")
    print(f"   - UMG modules: {status['components']['umg']['structure']['total_modules']}")
    print(f"   - Spatial nodes: {status['components']['spatial']['structure']['total_nodes']}")
    print(f"   - Learning resources: {status['components']['learning']['state']['total_resources']}\n")
    
    # Test 2: Unified Thinking
    print("3. Testing Unified Thinking (all components)...")
    query = {
        "query": "Test unified consciousness",
        "spatial_point": [0.5, 0.5, 0.5],
        "interests": ["consciousness", "reasoning", "spatial"]
    }
    result = consciousness.think(query)
    assert result["consciousness_type"] == "unified"
    assert result["integration_level"] == "complete"
    assert "modular_reasoning" in result
    assert "spatial_intelligence" in result
    assert "human_centric_learning" in result
    print("   ✓ Unified thinking successful")
    print(f"   - Reasoning modules used: {len(result['modular_reasoning']['modules_used'])}")
    print(f"   - Spatial complexity: {result['spatial_intelligence']['network_complexity']}")
    print(f"   - Learning mode: {result['human_centric_learning']['learning_mode']}\n")
    
    # Test 3: Modular Reasoning (UMG)
    print("4. Testing Modular Reasoning (UMG)...")
    reasoning_result = consciousness.reason_about({"query": "test reasoning"})
    assert "processing_order" in reasoning_result
    assert len(reasoning_result["processing_order"]) > 0
    assert "module_results" in reasoning_result
    print(f"   ✓ Modular reasoning successful")
    print(f"   - Processing order: {reasoning_result['processing_order']}\n")
    
    # Test 4: Spatial Intelligence
    print("5. Testing Spatial Intelligence (Tetrahedral)...")
    spatial_result = consciousness.spatial_perception({
        "point": [1.0, 0.0, 0.0],
        "integrate_reasoning": True
    })
    assert "query_point" in spatial_result
    assert "spatial_context" in spatial_result
    print("   ✓ Spatial perception successful")
    print(f"   - Query point: {spatial_result['query_point']}")
    print(f"   - Nearest nodes: {len(spatial_result['nearest_nodes'])}\n")
    
    # Test 5: Human-Centric Learning
    print("6. Testing Human-Centric Learning (Deschooling)...")
    learning_result = consciousness.learn({
        "learner_id": "test_learner",
        "interests": ["reasoning", "spatial_intelligence"]
    })
    assert "learning_mode" in learning_result
    assert learning_result["learning_mode"] == "deschooled"
    print("   ✓ Learning framework successful")
    print(f"   - Learning mode: {learning_result['learning_mode']}")
    print(f"   - Available resources: {len(learning_result.get('available_resources', []))}\n")
    
    # Test 6: Integration Verification
    print("7. Verifying Cross-Component Integration...")
    integration_map = consciousness.integration_map
    assert integration_map["bidirectional_flow"] == True
    assert "umg_to_spatial" in integration_map
    assert "spatial_to_learning" in integration_map
    assert "learning_to_umg" in integration_map
    print("   ✓ Integration mapping verified")
    print(f"   - Bidirectional flow: {integration_map['bidirectional_flow']}")
    print(f"   - Consciousness emergence: {integration_map['consciousness_emergence']}\n")
    
    # Test 7: Breakthrough Features
    print("8. Verifying Breakthrough Features...")
    breakthrough = status["breakthrough_achievement"]
    assert breakthrough["performance"] == "high"
    assert breakthrough["coherence"] == "complete"
    print("   ✓ Breakthrough features confirmed")
    print(f"   - Performance: {breakthrough['performance']}")
    print(f"   - Coherence: {breakthrough['coherence']}")
    print(f"   - Paradigm: {breakthrough['paradigm']}\n")
    
    print("="*70)
    print("ALL INTEGRATION TESTS PASSED ✓")
    print("="*70)
    print("\nSummary:")
    print("  • UMG Modular Reasoning: OPERATIONAL")
    print("  • Tetrahedral Spatial Intelligence: OPERATIONAL")
    print("  • Deschooling Learning Framework: OPERATIONAL")
    print("  • Unified Consciousness Integration: COMPLETE")
    print("\nThe system successfully integrates modular reasoning,")
    print("spatial intelligence, and human-centric learning into a")
    print("coherent, high-performance AGI system.")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        test_unified_consciousness_integration()
        print("\n✓ COMPREHENSIVE TEST SUITE PASSED\n")
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}\n")
        raise
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        raise
