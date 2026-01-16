"""
Tetrahedral Spatial Reasoning Network

Implements spatial intelligence using tetrahedral geometric structures,
providing 3D spatial reasoning, geometric relationships, and multi-dimensional
pattern recognition capabilities.
"""

from typing import List, Tuple, Dict, Any, Optional
import numpy as np


class TetrahedralNode:
    """
    A node in the tetrahedral network representing a point in spatial reasoning space.
    """
    
    def __init__(self, node_id: str, position: np.ndarray, 
                 spatial_features: Optional[Dict[str, Any]] = None):
        """
        Initialize a tetrahedral node.
        
        Args:
            node_id: Unique identifier for the node
            position: 3D position vector [x, y, z]
            spatial_features: Optional spatial features associated with this node
        """
        self.node_id = node_id
        self.position = np.array(position)
        self.spatial_features = spatial_features or {}
        self.connections: List[str] = []
    
    def distance_to(self, other: 'TetrahedralNode') -> float:
        """Calculate Euclidean distance to another node."""
        return np.linalg.norm(self.position - other.position)
    
    def add_connection(self, node_id: str):
        """Add a connection to another node."""
        if node_id not in self.connections:
            self.connections.append(node_id)


class Tetrahedron:
    """
    A tetrahedral unit - the fundamental building block of spatial reasoning.
    Represents a 3D simplex with 4 vertices.
    """
    
    def __init__(self, vertices: List[TetrahedralNode]):
        """
        Initialize a tetrahedron.
        
        Args:
            vertices: List of 4 TetrahedralNode objects forming the tetrahedron
        """
        if len(vertices) != 4:
            raise ValueError("Tetrahedron requires exactly 4 vertices")
        
        self.vertices = vertices
        self.centroid = self._calculate_centroid()
        self.volume = self._calculate_volume()
    
    def _calculate_centroid(self) -> np.ndarray:
        """Calculate the centroid of the tetrahedron."""
        positions = np.array([v.position for v in self.vertices])
        return np.mean(positions, axis=0)
    
    def _calculate_volume(self) -> float:
        """Calculate the volume of the tetrahedron."""
        # Using the scalar triple product formula
        v0 = self.vertices[0].position
        v1 = self.vertices[1].position - v0
        v2 = self.vertices[2].position - v0
        v3 = self.vertices[3].position - v0
        
        volume = abs(np.dot(v1, np.cross(v2, v3))) / 6.0
        return volume
    
    def contains_point(self, point: np.ndarray) -> bool:
        """
        Check if a point is inside the tetrahedron using barycentric coordinates.
        
        Args:
            point: 3D point to check
            
        Returns:
            True if point is inside the tetrahedron
        """
        # Simplified check using volume comparison
        sub_volumes = []
        for i in range(4):
            # Create sub-tetrahedron with point replacing vertex i
            sub_vertices = [self.vertices[j] for j in range(4) if j != i]
            temp_node = TetrahedralNode(f"temp_{i}", point)
            sub_vertices.append(temp_node)
            
            try:
                sub_tet = Tetrahedron(sub_vertices)
                sub_volumes.append(sub_tet.volume)
            except (ValueError, IndexError):
                # Invalid tetrahedron configuration
                return False
        
        # Point is inside if sum of sub-volumes equals original volume
        return abs(sum(sub_volumes) - self.volume) < 1e-10


class TetrahedralNetwork:
    """
    A network of interconnected tetrahedra for spatial reasoning.
    Provides spatial intelligence through geometric structure analysis.
    """
    
    def __init__(self):
        """Initialize the tetrahedral network."""
        self.nodes: Dict[str, TetrahedralNode] = {}
        self.tetrahedra: List[Tetrahedron] = []
        self._initialize_base_structure()
    
    def _initialize_base_structure(self):
        """Initialize the base tetrahedral structure."""
        # Create a fundamental tetrahedral lattice
        # Using vertices of a regular tetrahedron centered at origin
        base_positions = [
            np.array([1.0, 1.0, 1.0]),
            np.array([1.0, -1.0, -1.0]),
            np.array([-1.0, 1.0, -1.0]),
            np.array([-1.0, -1.0, 1.0])
        ]
        
        # Create base nodes
        for i, pos in enumerate(base_positions):
            node = TetrahedralNode(
                f"base_{i}", 
                pos,
                {"type": "foundation", "level": 0}
            )
            self.nodes[node.node_id] = node
        
        # Create the fundamental tetrahedron
        base_vertices = [self.nodes[f"base_{i}"] for i in range(4)]
        base_tet = Tetrahedron(base_vertices)
        self.tetrahedra.append(base_tet)
        
        # Establish connections
        for i in range(4):
            for j in range(i + 1, 4):
                self.nodes[f"base_{i}"].add_connection(f"base_{j}")
                self.nodes[f"base_{j}"].add_connection(f"base_{i}")
    
    def add_spatial_node(self, node_id: str, position: np.ndarray, 
                        features: Optional[Dict[str, Any]] = None) -> TetrahedralNode:
        """
        Add a new spatial node to the network.
        
        Args:
            node_id: Unique identifier for the node
            position: 3D position vector
            features: Optional spatial features
            
        Returns:
            The created TetrahedralNode
        """
        node = TetrahedralNode(node_id, position, features)
        self.nodes[node_id] = node
        
        # Integrate into existing tetrahedral structure
        self._integrate_node(node)
        
        return node
    
    def _integrate_node(self, node: TetrahedralNode):
        """
        Integrate a new node into the tetrahedral network.
        
        Args:
            node: The node to integrate
        """
        # Find nearest existing nodes and form new tetrahedra
        nearest_nodes = self._find_nearest_nodes(node, k=4)
        
        if len(nearest_nodes) >= 3:
            # Create new tetrahedra with existing nodes
            for i in range(len(nearest_nodes) - 2):
                vertices = [node] + nearest_nodes[i:i+3]
                if len(vertices) == 4:
                    try:
                        tet = Tetrahedron(vertices)
                        self.tetrahedra.append(tet)
                    except (ValueError, IndexError):
                        # Skip invalid tetrahedron configurations
                        continue
    
    def _find_nearest_nodes(self, node: TetrahedralNode, k: int = 4) -> List[TetrahedralNode]:
        """
        Find k nearest nodes to the given node.
        
        Args:
            node: Reference node
            k: Number of nearest nodes to find
            
        Returns:
            List of nearest TetrahedralNode objects
        """
        if not self.nodes:
            return []
        
        distances = []
        for node_id, other_node in self.nodes.items():
            if node_id != node.node_id:
                dist = node.distance_to(other_node)
                distances.append((dist, other_node))
        
        distances.sort(key=lambda x: x[0])
        return [node for _, node in distances[:k]]
    
    def spatial_query(self, query_point: np.ndarray) -> Dict[str, Any]:
        """
        Perform a spatial query at a given point.
        
        Args:
            query_point: 3D point to query
            
        Returns:
            Spatial reasoning results
        """
        # Find containing tetrahedra
        containing_tetrahedra = []
        for tet in self.tetrahedra:
            if tet.contains_point(query_point):
                containing_tetrahedra.append(tet)
        
        # Find nearest nodes
        temp_node = TetrahedralNode("query_temp", query_point)
        nearest = self._find_nearest_nodes(temp_node, k=5)
        
        return {
            "query_point": query_point.tolist(),
            "containing_tetrahedra_count": len(containing_tetrahedra),
            "nearest_nodes": [n.node_id for n in nearest],
            "spatial_context": self._analyze_spatial_context(query_point, nearest)
        }
    
    def _analyze_spatial_context(self, point: np.ndarray, 
                                 nearby_nodes: List[TetrahedralNode]) -> Dict[str, Any]:
        """
        Analyze the spatial context around a point.
        
        Args:
            point: Point to analyze
            nearby_nodes: Nearby nodes for context
            
        Returns:
            Spatial context analysis
        """
        if not nearby_nodes:
            return {"density": 0.0, "pattern": "isolated"}
        
        # Calculate local density
        distances = [np.linalg.norm(point - n.position) for n in nearby_nodes]
        avg_distance = np.mean(distances)
        density = 1.0 / (avg_distance + 1e-10)
        
        # Analyze geometric pattern
        pattern = "clustered" if avg_distance < 2.0 else "sparse"
        
        return {
            "density": float(density),
            "pattern": pattern,
            "avg_distance_to_neighbors": float(avg_distance),
            "dimensionality": 3
        }
    
    def get_network_structure(self) -> Dict[str, Any]:
        """
        Get the structure of the tetrahedral network.
        
        Returns:
            Network structure information
        """
        total_volume = sum(tet.volume for tet in self.tetrahedra)
        
        return {
            "total_nodes": len(self.nodes),
            "total_tetrahedra": len(self.tetrahedra),
            "total_spatial_volume": float(total_volume),
            "node_ids": list(self.nodes.keys()),
            "average_tetrahedron_volume": float(total_volume / len(self.tetrahedra)) 
                if self.tetrahedra else 0.0
        }
    
    def spatial_reasoning(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform spatial reasoning on a given task.
        
        Args:
            task: Spatial reasoning task specification
            
        Returns:
            Reasoning results
        """
        task_type = task.get("type", "general")
        
        if task_type == "localization":
            point = np.array(task.get("point", [0, 0, 0]))
            return self.spatial_query(point)
        
        elif task_type == "pattern_recognition":
            # Analyze the overall spatial pattern
            return {
                "pattern_type": "tetrahedral_lattice",
                "complexity": len(self.tetrahedra),
                "structure": self.get_network_structure()
            }
        
        else:
            # General spatial reasoning
            return {
                "reasoning_type": "spatial",
                "network_state": self.get_network_structure(),
                "spatial_intelligence": "active"
            }
