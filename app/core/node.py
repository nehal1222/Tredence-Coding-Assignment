from typing import Optional, Callable
import asyncio
from app.core.state import WorkflowState
from app.core.registry import tool_registry
import logging

logger = logging.getLogger(__name__)

class Node:
    def __init__(self, name: str, tool_name: str, node_type: str = "standard",
                 loop_condition: Optional[str] = None, max_iterations: int = 10):
        self.name = name
        self.tool_name = tool_name
        self.node_type = node_type
        self.loop_condition = loop_condition
        self.max_iterations = max_iterations
    
    async def execute(self, state: WorkflowState) -> WorkflowState:
        """Execute the node's tool with the current state"""
        logger.info(f"Executing node: {self.name}")
        
        tool = tool_registry.get(self.tool_name)
        
        if self.node_type == "loop" and self.loop_condition:
            iteration = 0
            while iteration < self.max_iterations:
                if not self._evaluate_condition(self.loop_condition, state):
                    break
                
                state.increment_iteration()
                result = await self._run_tool(tool, state)
                state.update(result)
                iteration += 1
                logger.info(f"Loop iteration {iteration} completed for node {self.name}")
        else:
            result = await self._run_tool(tool, state)
            state.update(result)
        
        return state
    
    async def _run_tool(self, tool: Callable, state: WorkflowState) -> dict:
        """Run the tool, handling both sync and async functions"""
        if asyncio.iscoroutinefunction(tool):
            return await tool(state.data)
        else:
            return tool(state.data)
    
    def _evaluate_condition(self, condition: str, state: WorkflowState) -> bool:
        """Evaluate a condition string against the state"""
        try:
            local_vars = state.data.copy()
            return eval(condition, {"__builtins__": {}}, local_vars)
        except Exception as e:
            logger.error(f"Error evaluating condition '{condition}': {e}")
            return False
