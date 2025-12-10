# main.py
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

graphs = {}
executions = {}

class NodeDefinition(BaseModel):
    name: str
    type: str
    tool: str

class GraphDefinition(BaseModel):
    name: str
    nodes: List[NodeDefinition]
    edges: List[Dict] = []
    start_node: str

class GraphCreateRequest(BaseModel):
    definition: GraphDefinition

class WorkflowEngine:
    def __init__(self, definition: GraphDefinition):
        if not definition.nodes or not definition.start_node:
            raise ValueError("Graph definition must have nodes and a start node")
        self.graph = definition
        self.graph_id = str(uuid.uuid4())
        self.name = definition.name

    def execute(self, initial_state=None):
        execution_id = str(uuid.uuid4())
        executions[execution_id] = initial_state or {}
        return execution_id

@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/v1/graph/create")
async def create_graph(request: GraphCreateRequest):
    try:
        engine = WorkflowEngine(request.definition)
        graphs[engine.graph_id] = engine.graph
        return {"graph_id": engine.graph_id, "message": "Graph created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/graph/run")
async def run_graph(request: dict):
    graph_id = request.get("graph_id")
    initial_state = request.get("initial_state", {})
    if graph_id not in graphs:
        raise HTTPException(status_code=404, detail="Graph not found")
    engine = WorkflowEngine(graphs[graph_id])
    execution_id = engine.execute(initial_state)
    return {"execution_id": execution_id, "status": "started"}
