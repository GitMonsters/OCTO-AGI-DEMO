"""
Deschooling Learning Framework

Implements Ivan Illich's deschooling philosophy for human-centric learning.
Focuses on self-directed learning, peer-to-peer knowledge exchange, and
breaking free from institutional constraints to foster genuine understanding.
"""

from typing import Dict, List, Any, Optional, Set
from datetime import datetime


class LearningResource:
    """
    Represents a learning resource in the deschooling framework.
    Resources are freely accessible and learner-directed.
    """
    
    def __init__(self, resource_id: str, title: str, 
                 resource_type: str, content: Any):
        """
        Initialize a learning resource.
        
        Args:
            resource_id: Unique identifier
            title: Resource title
            resource_type: Type (e.g., 'concept', 'skill', 'experience')
            content: Resource content
        """
        self.resource_id = resource_id
        self.title = title
        self.resource_type = resource_type
        self.content = content
        self.access_count = 0
        self.peer_connections: Set[str] = set()
    
    def access(self) -> Dict[str, Any]:
        """Access the resource and return its content."""
        self.access_count += 1
        return {
            "resource_id": self.resource_id,
            "title": self.title,
            "type": self.resource_type,
            "content": self.content,
            "access_count": self.access_count
        }


class Learner:
    """
    Represents an autonomous learner in the deschooled system.
    Learners are self-directed and define their own learning paths.
    """
    
    def __init__(self, learner_id: str, interests: List[str]):
        """
        Initialize a learner.
        
        Args:
            learner_id: Unique identifier
            interests: List of learning interests
        """
        self.learner_id = learner_id
        self.interests = interests
        self.learning_history: List[Dict[str, Any]] = []
        self.peer_network: Set[str] = set()
        self.knowledge_graph: Dict[str, Any] = {}
    
    def learn(self, resource: LearningResource) -> Dict[str, Any]:
        """
        Engage with a learning resource.
        
        Args:
            resource: The learning resource to engage with
            
        Returns:
            Learning outcome
        """
        resource_data = resource.access()
        
        # Record learning experience
        learning_event = {
            "timestamp": datetime.now().isoformat(),
            "resource_id": resource.resource_id,
            "resource_type": resource.resource_type,
            "self_directed": True,
            "understanding_level": self._assess_understanding(resource)
        }
        
        self.learning_history.append(learning_event)
        
        # Update knowledge graph
        self._integrate_knowledge(resource)
        
        return {
            "learner_id": self.learner_id,
            "learning_event": learning_event,
            "knowledge_growth": len(self.knowledge_graph)
        }
    
    def _assess_understanding(self, resource: LearningResource) -> str:
        """
        Self-assess understanding of a resource.
        In deschooling, assessment is learner-driven.
        """
        # Simplified self-assessment based on interest alignment
        if resource.resource_type in self.interests:
            return "deep"
        return "exploratory"
    
    def _integrate_knowledge(self, resource: LearningResource):
        """
        Integrate new knowledge into the learner's knowledge graph.
        
        Args:
            resource: Resource to integrate
        """
        if resource.resource_type not in self.knowledge_graph:
            self.knowledge_graph[resource.resource_type] = []
        
        self.knowledge_graph[resource.resource_type].append({
            "resource_id": resource.resource_id,
            "title": resource.title,
            "learned_at": datetime.now().isoformat()
        })
    
    def connect_with_peer(self, peer_id: str):
        """
        Form a peer learning connection.
        
        Args:
            peer_id: ID of the peer to connect with
        """
        self.peer_network.add(peer_id)


class LearningWeb:
    """
    The Learning Web - a decentralized network for knowledge exchange.
    Inspired by Illich's concept of learning webs that replace traditional schools.
    """
    
    def __init__(self):
        """Initialize the learning web."""
        self.resources: Dict[str, LearningResource] = {}
        self.learners: Dict[str, Learner] = {}
        self.peer_exchanges: List[Dict[str, Any]] = []
        self._initialize_foundational_resources()
    
    def _initialize_foundational_resources(self):
        """Initialize foundational learning resources."""
        foundational = [
            LearningResource(
                "concept_autonomy",
                "Autonomous Learning",
                "concept",
                "Learning is self-directed and driven by genuine curiosity"
            ),
            LearningResource(
                "skill_critical_thinking",
                "Critical Thinking",
                "skill",
                "Questioning assumptions and thinking independently"
            ),
            LearningResource(
                "experience_collaboration",
                "Peer Collaboration",
                "experience",
                "Learning through peer-to-peer knowledge exchange"
            ),
            LearningResource(
                "concept_convivial_tools",
                "Convivial Tools",
                "concept",
                "Tools that enhance human capability without creating dependency"
            )
        ]
        
        for resource in foundational:
            self.add_resource(resource)
    
    def add_resource(self, resource: LearningResource):
        """
        Add a learning resource to the web.
        
        Args:
            resource: Resource to add
        """
        self.resources[resource.resource_id] = resource
    
    def register_learner(self, learner: Learner):
        """
        Register a learner in the learning web.
        
        Args:
            learner: Learner to register
        """
        self.learners[learner.learner_id] = learner
    
    def find_resources(self, criteria: Dict[str, Any]) -> List[LearningResource]:
        """
        Find resources matching criteria.
        
        Args:
            criteria: Search criteria (e.g., type, keywords)
            
        Returns:
            List of matching resources
        """
        matches = []
        
        resource_type = criteria.get("type")
        keywords = criteria.get("keywords", [])
        
        for resource in self.resources.values():
            if resource_type and resource.resource_type != resource_type:
                continue
            
            if keywords:
                # Check if any keyword matches title or content
                text = f"{resource.title} {resource.content}".lower()
                if not any(kw.lower() in text for kw in keywords):
                    continue
            
            matches.append(resource)
        
        return matches
    
    def facilitate_peer_exchange(self, learner1_id: str, learner2_id: str,
                                 topic: str) -> Dict[str, Any]:
        """
        Facilitate a peer-to-peer learning exchange.
        
        Args:
            learner1_id: First learner's ID
            learner2_id: Second learner's ID
            topic: Topic of exchange
            
        Returns:
            Exchange outcome
        """
        if learner1_id not in self.learners or learner2_id not in self.learners:
            return {"success": False, "reason": "Learner not found"}
        
        learner1 = self.learners[learner1_id]
        learner2 = self.learners[learner2_id]
        
        # Connect learners
        learner1.connect_with_peer(learner2_id)
        learner2.connect_with_peer(learner1_id)
        
        # Record exchange
        exchange = {
            "timestamp": datetime.now().isoformat(),
            "participants": [learner1_id, learner2_id],
            "topic": topic,
            "exchange_type": "peer_learning",
            "success": True
        }
        
        self.peer_exchanges.append(exchange)
        
        return exchange
    
    def get_learning_paths(self, learner_id: str) -> Dict[str, Any]:
        """
        Get personalized learning paths for a learner.
        Paths are self-directed based on interests and history.
        
        Args:
            learner_id: Learner's ID
            
        Returns:
            Suggested learning paths
        """
        if learner_id not in self.learners:
            return {"paths": []}
        
        learner = self.learners[learner_id]
        
        # Generate paths based on interests
        paths = []
        for interest in learner.interests:
            matching_resources = self.find_resources({"keywords": [interest]})
            if matching_resources:
                paths.append({
                    "interest": interest,
                    "resources": [r.resource_id for r in matching_resources[:3]],
                    "learning_mode": "self_directed"
                })
        
        return {
            "learner_id": learner_id,
            "paths": paths,
            "philosophy": "deschooling",
            "autonomy_level": "full"
        }


class DeschoolingFramework:
    """
    The complete Deschooling Framework implementing Illich's philosophy.
    Provides human-centric, self-directed learning capabilities.
    """
    
    def __init__(self):
        """Initialize the deschooling framework."""
        self.learning_web = LearningWeb()
        self.principles = self._define_core_principles()
    
    def _define_core_principles(self) -> Dict[str, str]:
        """Define the core principles of deschooling."""
        return {
            "autonomy": "Learners are autonomous and self-directed",
            "peer_learning": "Knowledge is exchanged peer-to-peer",
            "no_hierarchy": "No institutional hierarchy or credentials",
            "convivial_tools": "Tools enhance rather than replace human capability",
            "intrinsic_motivation": "Learning driven by genuine curiosity",
            "contextual_learning": "Learning happens in real-world contexts"
        }
    
    def create_learning_experience(self, learner_id: str, 
                                   interests: List[str]) -> Dict[str, Any]:
        """
        Create a deschooled learning experience.
        
        Args:
            learner_id: Unique learner identifier
            interests: Learner's interests
            
        Returns:
            Learning experience configuration
        """
        # Create learner
        learner = Learner(learner_id, interests)
        self.learning_web.register_learner(learner)
        
        # Find relevant resources
        resources = []
        for interest in interests:
            resources.extend(
                self.learning_web.find_resources({"keywords": [interest]})
            )
        
        # Generate learning paths
        paths = self.learning_web.get_learning_paths(learner_id)
        
        return {
            "learner_id": learner_id,
            "learning_mode": "deschooled",
            "available_resources": [r.resource_id for r in resources],
            "learning_paths": paths,
            "principles": self.principles,
            "community_size": len(self.learning_web.learners)
        }
    
    def facilitate_learning(self, learner_id: str, 
                           resource_id: str) -> Dict[str, Any]:
        """
        Facilitate a learning interaction.
        
        Args:
            learner_id: Learner's ID
            resource_id: Resource to learn from
            
        Returns:
            Learning outcome
        """
        if learner_id not in self.learning_web.learners:
            return {"success": False, "reason": "Learner not registered"}
        
        if resource_id not in self.learning_web.resources:
            return {"success": False, "reason": "Resource not found"}
        
        learner = self.learning_web.learners[learner_id]
        resource = self.learning_web.resources[resource_id]
        
        outcome = learner.learn(resource)
        
        return {
            **outcome,
            "success": True,
            "learning_philosophy": "deschooling",
            "self_directed": True
        }
    
    def get_framework_state(self) -> Dict[str, Any]:
        """
        Get the current state of the deschooling framework.
        
        Returns:
            Framework state information
        """
        return {
            "total_learners": len(self.learning_web.learners),
            "total_resources": len(self.learning_web.resources),
            "peer_exchanges": len(self.learning_web.peer_exchanges),
            "principles": self.principles,
            "philosophy": "Ivan Illich's Deschooling Society"
        }
