from typing import Dict, List, Optional
import uuid
from datetime import datetime
import logging
from app.core.node import Node
from app.core.state import WorkflowState
from app.models.schemas import GraphDefinition, EdgeConfig

logger = logging.getLogger(__name__)

class WorkflowEngine:
    def __init__(self, graph_definition: GraphDefinition):
        self.graph_id = str(uuid.uuid4())
        self.name = graph_definition.name
        self.nodes: Dict[str, Node] = {}
        self.edges: Dict[str, List[EdgeConfig]] = {}
        self.start_node = graph_definition.start_node
        
        self._build_graph(graph_definition)
    
    def _build_graph(self, definition: GraphDefinition):
        """Build the graph from definition"""
        for node_config in definition.nodes:
            self.nodes[node_config.name] = Node(
                name=node_config.name,
                tool_name=node_config.tool,
                node_type=node_config.type,
                loop_condition=node_config.loop_condition,
                max_iterations=node_config.max_iterations or 10
            )
        
        for edge in definition.edges:
            if edge.from_node not in self.edges:
                self.edges[edge.from_node] = []
            self.edges[edge.from_node].append(edge)
    
    async def execute(self, initial_state: Dict = None) -> tuple:
        """Execute the workflow from start to finish"""
        state = WorkflowState(initial_state or {})
        execution_log = []
        
        current_node_name = self.start_node
        visited_nodes = set()
        
        while current_node_name:
            if current_node_name not in self.nodes:
                logger.error(f"Node '{current_node_name}' not found")
                break
            
            if current_node_name in visited_nodes and current_node_name != self.start_node:
                node = self.nodes[current_node_name]
                if node.node_type != "loop":
                    logger.warning(f"Cycle detected at node '{current_node_name}', stopping execution")
                    break
            
            visited_nodes.add(current_node_name)
            node = self.nodes[current_node_name]
            
            start_time = datetime.utcnow()
            try:
                state = await node.execute(state)
                status = "success"
                error = None
            except Exception as e:
                logger.error(f"Error executing node '{current_node_name}': {e}")
                status = "error"
                error = str(e)
            
            execution_log.append({
                "node": current_node_name,
                "timestamp": start_time.isoformat(),
                "status": status,
                "error": error,
                "state_snapshot": state.data.copy()
            })
            
            current_node_name = self._get_next_node(current_node_name, state)
        
        return state, execution_log
    
    def _get_next_node(self, current_node: str, state: WorkflowState) -> Optional[str]:
        """Determine the next node based on edges and conditions"""
        if current_node not in self.edges:
            return None
        
        edges = self.edges[current_node]
        
        for edge in edges:
            if edge.condition:
                if self._evaluate_condition(edge.condition, state):
                    return edge.to_node
        
        for edge in edges:
            if not edge.condition:
                return edge.to_node
        
        return None
    
    def _evaluate_condition(self, condition: str, state: WorkflowState) -> bool:
        """Evaluate edge condition"""
        try:
            local_vars = state.data.copy()
            return eval(condition, {"__builtins__": {}}, local_vars)
        except Exception as e:
            logger.error(f"Error evaluating edge condition '{condition}': {e}")
            return False
