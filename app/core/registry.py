from typing import Callable, Dict
import logging

logger = logging.getLogger(__name__)

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Callable] = {}
    
    def register(self, name: str, func: Callable):
        """Register a tool function"""
        self.tools[name] = func
        logger.info(f"Registered tool: {name}")
    
    def get(self, name: str) -> Callable:
        """Get a tool by name"""
        if name not in self.tools:
            raise ValueError(f"Tool '{name}' not found in registry")
        return self.tools[name]
    
    def list_tools(self) -> list:
        """List all registered tools"""
        return list(self.tools.keys())

tool_registry = ToolRegistry()
