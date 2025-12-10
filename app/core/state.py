from typing import Any, Dict
from datetime import datetime

class WorkflowState:
    def __init__(self, initial_state: Dict[str, Any] = None):
        self.data = initial_state or {}
        self.metadata = {
            "created_at": datetime.utcnow().isoformat(),
            "iteration_count": 0
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)
    
    def set(self, key: str, value: Any):
        self.data[key] = value
    
    def update(self, updates: Dict[str, Any]):
        self.data.update(updates)
    
    def increment_iteration(self):
        self.metadata["iteration_count"] += 1
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "data": self.data,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, state_dict: Dict[str, Any]) -> 'WorkflowState':
        instance = cls()
        instance.data = state_dict.get("data", {})
        instance.metadata = state_dict.get("metadata", {})
        return instance
