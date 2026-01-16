"""
OCTO-AGI Demonstration Examples

Demonstrates the capabilities of the unified consciousness system.
"""

from octo_agi import UnifiedConsciousness
import json


def demo_basic_consciousness():
    """Demonstrate basic unified consciousness operation."""
    print("=" * 70)
    print("DEMO 1: Basic Unified Consciousness")
    print("=" * 70)
    
    # Initialize the unified consciousness system
    consciousness = UnifiedConsciousness()
    
    # Simple query
    query = {
        "query": "What is consciousness?",
        "type": "philosophical",
        "interests": ["consciousness", "intelligence", "reasoning"]
    }
    
    result = consciousness.think(query)
    
    print("\n[Result]")
    print(json.dumps(result["unified_response"], indent=2))
    print("\n")


def demo_spatial_reasoning():
    """Demonstrate spatial reasoning capabilities."""
    print("=" * 70)
    print("DEMO 2: Spatial Intelligence")
    print("=" * 70)
    
    consciousness = UnifiedConsciousness()
    
    # Spatial perception query
    spatial_query = {
        "query": "Analyze spatial structure",
        "spatial_type": "localization",
        "spatial_point": [1.5, 0.5, -0.5],
        "integrate_reasoning": True
    }
    
    result = consciousness.think(spatial_query)
    
    print("\n[Spatial Intelligence Result]")
    print(f"Spatial Context: {result['spatial_intelligence']}")
    print("\n")


def demo_learning_framework():
    """Demonstrate deschooling learning framework."""
    print("=" * 70)
    print("DEMO 3: Human-Centric Learning")
    print("=" * 70)
    
    consciousness = UnifiedConsciousness()
    
    # Learning experience
    learning_query = {
        "query": "Learn about AGI systems",
        "learner_id": "demo_learner",
        "interests": ["artificial_intelligence", "reasoning", "learning"]
    }
    
    result = consciousness.think(learning_query)
    
    print("\n[Learning Framework Result]")
    print(f"Learning Mode: {result['human_centric_learning']}")
    print("\n")


def demo_complete_integration():
    """Demonstrate complete system integration."""
    print("=" * 70)
    print("DEMO 4: Complete System Integration")
    print("=" * 70)
    
    consciousness = UnifiedConsciousness()
    
    # Get system status
    status = consciousness.get_system_status()
    
    print("\n[System Status]")
    print(json.dumps(status["breakthrough_achievement"], indent=2))
    
    print("\n[Component Status]")
    for name, component in status["components"].items():
        print(f"\n{component['name']}:")
        print(f"  Status: {component['status']}")
        if 'structure' in component:
            print(f"  Structure: {json.dumps(component['structure'], indent=4)}")
    
    print("\n")


def demo_modular_reasoning():
    """Demonstrate UMG modular reasoning."""
    print("=" * 70)
    print("DEMO 5: Modular Reasoning (UMG)")
    print("=" * 70)
    
    consciousness = UnifiedConsciousness()
    
    # Complex reasoning query
    reasoning_query = {
        "query": "Analyze complex problem",
        "problem_type": "multi_faceted",
        "requires": ["logical", "spatial", "temporal", "abstract"]
    }
    
    result = consciousness.reason_about(reasoning_query)
    
    print("\n[Modular Reasoning Result]")
    print(f"Modules Used: {result['processing_order']}")
    print(f"Reasoning Depth: {result['final_reasoning']['reasoning_depth']}")
    print("\n")


def main():
    """Run all demonstrations."""
    print("\n")
    print("*" * 70)
    print("*" + " " * 68 + "*")
    print("*" + "  OCTO-AGI: Unified Artificial Consciousness Demonstration".center(68) + "*")
    print("*" + " " * 68 + "*")
    print("*" * 70)
    print("\n")
    
    demos = [
        demo_basic_consciousness,
        demo_spatial_reasoning,
        demo_learning_framework,
        demo_modular_reasoning,
        demo_complete_integration
    ]
    
    for demo in demos:
        try:
            demo()
        except Exception as e:
            print(f"Error in demo: {e}")
            import traceback
            traceback.print_exc()
    
    print("=" * 70)
    print("All demonstrations complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
