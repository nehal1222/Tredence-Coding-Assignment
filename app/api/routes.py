from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict
import uuid
import logging
from app.models.schemas import (
    CreateGraphRequest, CreateGraphResponse,
    RunGraphRequest, RunGraphResponse,
    ExecutionStateResponse
)
from app.core.engine import WorkflowEngine
from app.database import db

logger = logging.getLogger(__name__)
router = APIRouter()

active_executions: Dict[str, dict] = {}

async def execute_workflow_background(execution_id: str, graph_id: str, 
                                     engine: WorkflowEngine, initial_state: dict):
    """Background task to execute workflow"""
    try:
        active_executions[execution_id] = {
            "status": "running",
            "state": initial_state,
            "log": []
        }
        
        final_state, execution_log = await engine.execute(initial_state)
        
        active_executions[execution_id] = {
            "status": "completed",
            "state": final_state.data,
            "log": execution_log
        }
        
        await db.save_execution(
            execution_id, graph_id, "completed",
            final_state.data, execution_log
        )
        
    except Exception as e:
        logger.error(f"Workflow execution failed: {e}")
        active_executions[execution_id] = {
            "status": "failed",
            "state": initial_state,
            "log": [],
            "error": str(e)
        }

@router.post("/graph/create", response_model=CreateGraphResponse)
async def create_graph(request: CreateGraphRequest):
    """Create a new workflow graph"""
    try:
        engine = WorkflowEngine(request.definition)
        await db.save_graph(engine.graph_id, engine.name, request.definition.dict())
        
        return CreateGraphResponse(
            graph_id=engine.graph_id,
            message=f"Graph '{engine.name}' created successfully"
        )
    except Exception as e:
        logger.error(f"Error creating graph: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/graph/run", response_model=RunGraphResponse)
async def run_graph(request: RunGraphRequest, background_tasks: BackgroundTasks):
    """Execute a workflow graph"""
    try:
        graph_def = await db.get_graph(request.graph_id)
        if not graph_def:
            raise HTTPException(status_code=404, detail="Graph not found")
        
        from app.models.schemas import GraphDefinition
        engine = WorkflowEngine(GraphDefinition(**graph_def))
        
        execution_id = str(uuid.uuid4())
        
        background_tasks.add_task(
            execute_workflow_background,
            execution_id, request.graph_id, engine, request.initial_state
        )
        
        return RunGraphResponse(
            execution_id=execution_id,
            status="started",
            message="Workflow execution started"
        )
    except Exception as e:
        logger.error(f"Error running graph: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/graph/state/{execution_id}", response_model=ExecutionStateResponse)
async def get_execution_state(execution_id: str):
    """Get the current state of a workflow execution"""
    if execution_id in active_executions:
        exec_data = active_executions[execution_id]
        return ExecutionStateResponse(
            execution_id=execution_id,
            graph_id="",
            status=exec_data["status"],
            current_state=exec_data["state"],
            execution_log=exec_data["log"]
        )
    
    exec_data = await db.get_execution(execution_id)
    if not exec_data:
        raise HTTPException(status_code=404, detail="Execution not found")
    
    return ExecutionStateResponse(
        execution_id=execution_id,
        graph_id=exec_data["graph_id"],
        status=exec_data["status"],
        current_state=exec_data["state"],
        execution_log=exec_data["log"]
    )

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Workflow Engine is running"}
