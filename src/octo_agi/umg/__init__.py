"""
Universal Module Graph (UMG) - Modular Reasoning Engine

The UMG system provides modular reasoning capabilities through a graph-based
architecture where each node represents a reasoning module and edges represent
information flow and dependencies.
"""

from typing import Dict, List, Any, Optional, Set
import networkx as nx


class ReasoningModule:
    """
    A single reasoning module in the UMG system.
    Each module encapsulates a specific reasoning capability.
    """
    
    def __init__(self, module_id: str, module_type: str, capabilities: List[str]):
        """
        Initialize a reasoning module.
        
        Args:
            module_id: Unique identifier for the module
            module_type: Type of reasoning (e.g., 'logical', 'spatial', 'temporal')
            capabilities: List of specific capabilities this module provides
        """
        self.module_id = module_id
        self.module_type = module_type
        self.capabilities = capabilities
        self.state: Dict[str, Any] = {}
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input data through this reasoning module.
        
        Args:
            input_data: Input data to process
            
        Returns:
            Processed output data
        """
        # Update module state
        self.state.update(input_data)
        
        # Apply reasoning transformations based on module type
        output = {
            "module_id": self.module_id,
            "processed": True,
            "reasoning_type": self.module_type,
            "result": self._apply_reasoning(input_data)
        }
        
        return output
    
    def _apply_reasoning(self, data: Dict[str, Any]) -> Any:
        """Apply module-specific reasoning logic."""
        # Abstract reasoning - specialized by module type
        return {
            "inference": f"Reasoning applied by {self.module_type} module",
            "data": data,
            "capabilities_used": self.capabilities
        }


class UniversalModuleGraph:
    """
    The Universal Module Graph (UMG) coordinates multiple reasoning modules
    to provide comprehensive, modular reasoning capabilities.
    """
    
    def __init__(self):
        """Initialize the UMG system."""
        self.graph = nx.DiGraph()
        self.modules: Dict[str, ReasoningModule] = {}
        self._initialize_core_modules()
    
    def _initialize_core_modules(self):
        """Initialize the core reasoning modules."""
        core_modules = [
            ReasoningModule("logical_reasoning", "logical", 
                          ["deduction", "induction", "abduction"]),
            ReasoningModule("spatial_reasoning", "spatial", 
                          ["3d_understanding", "geometric_relations"]),
            ReasoningModule("temporal_reasoning", "temporal", 
                          ["sequence_analysis", "causality"]),
            ReasoningModule("abstract_reasoning", "abstract", 
                          ["pattern_recognition", "generalization"]),
            ReasoningModule("meta_reasoning", "meta", 
                          ["self_reflection", "strategy_selection"])
        ]
        
        for module in core_modules:
            self.add_module(module)
        
        # Establish core connections
        self._establish_core_connections()
    
    def add_module(self, module: ReasoningModule):
        """
        Add a reasoning module to the graph.
        
        Args:
            module: The reasoning module to add
        """
        self.modules[module.module_id] = module
        self.graph.add_node(module.module_id, module=module)
    
    def connect_modules(self, source_id: str, target_id: str, 
                       connection_type: str = "data_flow"):
        """
        Create a connection between two modules.
        
        Args:
            source_id: Source module ID
            target_id: Target module ID
            connection_type: Type of connection
        """
        if source_id in self.modules and target_id in self.modules:
            self.graph.add_edge(source_id, target_id, 
                              connection_type=connection_type)
    
    def _establish_core_connections(self):
        """Establish connections between core modules."""
        # Logical reasoning feeds into abstract reasoning
        self.connect_modules("logical_reasoning", "abstract_reasoning")
        
        # Spatial and temporal reasoning feed into meta reasoning
        self.connect_modules("spatial_reasoning", "meta_reasoning")
        self.connect_modules("temporal_reasoning", "meta_reasoning")
        
        # Abstract reasoning feeds into meta reasoning
        self.connect_modules("abstract_reasoning", "meta_reasoning")
        
        # Meta reasoning can influence all modules (feedback)
        for module_id in ["logical_reasoning", "spatial_reasoning", 
                         "temporal_reasoning", "abstract_reasoning"]:
            self.connect_modules("meta_reasoning", module_id, "feedback")
    
    def reason(self, query: Dict[str, Any], 
               target_modules: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Execute reasoning across the module graph.
        
        Args:
            query: The reasoning query
            target_modules: Specific modules to use (if None, uses all relevant)
            
        Returns:
            Reasoning results
        """
        if target_modules is None:
            # Determine relevant modules based on query
            target_modules = list(self.modules.keys())
        
        results = {}
        processing_order = self._get_processing_order(target_modules)
        
        current_data = query
        for module_id in processing_order:
            if module_id in self.modules:
                module = self.modules[module_id]
                result = module.process(current_data)
                results[module_id] = result
                
                # Pass results to next module
                current_data = {**current_data, **result}
        
        return {
            "query": query,
            "processing_order": processing_order,
            "module_results": results,
            "final_reasoning": self._synthesize_results(results)
        }
    
    def _get_processing_order(self, module_ids: List[str]) -> List[str]:
        """
        Determine optimal processing order for modules.
        
        Args:
            module_ids: List of module IDs to process
            
        Returns:
            Ordered list of module IDs
        """
        # Create a DAG by excluding feedback edges for ordering
        dag = nx.DiGraph()
        dag.add_nodes_from(module_ids)
        
        for source, target, data in self.graph.edges(data=True):
            if source in module_ids and target in module_ids:
                # Skip feedback edges to avoid cycles
                if data.get('connection_type') != 'feedback':
                    dag.add_edge(source, target)
        
        # Use topological sort for dependency-aware ordering
        try:
            return list(nx.topological_sort(dag))
        except nx.NetworkXError as e:
            # If cycles still exist (shouldn't happen after filtering feedback edges),
            # use a deterministic order based on module type priority
            # This ensures consistent processing even with complex dependencies
            priority_order = ["logical", "spatial", "temporal", "abstract", "meta"]
            ordered = sorted(module_ids, 
                           key=lambda mid: (
                               priority_order.index(self.modules[mid].module_type) 
                               if self.modules[mid].module_type in priority_order 
                               else len(priority_order)
                           ))
            return ordered
    
    def _synthesize_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesize results from multiple modules.
        
        Args:
            results: Results from all modules
            
        Returns:
            Synthesized reasoning output
        """
        return {
            "synthesis": "Integrated reasoning from multiple modules",
            "modules_used": list(results.keys()),
            "reasoning_depth": len(results),
            "unified_conclusion": "Modular reasoning complete"
        }
    
    def get_graph_structure(self) -> Dict[str, Any]:
        """
        Get the structure of the module graph.
        
        Returns:
            Graph structure information
        """
        return {
            "total_modules": len(self.modules),
            "module_ids": list(self.modules.keys()),
            "connections": list(self.graph.edges()),
            "module_types": {mid: m.module_type 
                           for mid, m in self.modules.items()}
        }
