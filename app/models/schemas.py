from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from enum import Enum

class NodeType(str, Enum):
    STANDARD = "standard"
    CONDITIONAL = "conditional"
    LOOP = "loop"

class EdgeConfig(BaseModel):
    from_node: str
    to_node: str
    condition: Optional[str] = None

class NodeConfig(BaseModel):
    name: str
    type: NodeType = NodeType.STANDARD
    tool: str
    loop_condition: Optional[str] = None
    max_iterations: Optional[int] = 10

class GraphDefinition(BaseModel):
    name: str
    nodes: List[NodeConfig]
    edges: List[EdgeConfig]
    start_node: str

class CreateGraphRequest(BaseModel):
    definition: GraphDefinition

class CreateGraphResponse(BaseModel):
    graph_id: str
    message: str

class RunGraphRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any] = Field(default_factory=dict)

class RunGraphResponse(BaseModel):
    execution_id: str
    status: str
    message: str

class ExecutionStateResponse(BaseModel):
    execution_id: str
    graph_id: str
    status: str
    current_state: Dict[str, Any]
    execution_log: List[Dict[str, Any]]
