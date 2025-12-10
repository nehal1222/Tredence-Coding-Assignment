from app.core.registry import tool_registry
from .tools import extract_functions, check_complexity, detect_issues, suggest_improvements
from app.models.schemas import GraphDefinition, NodeConfig, EdgeConfig, NodeType

def register_workflow_tools():
    tool_registry.register("extract_functions", extract_functions)
    tool_registry.register("check_complexity", check_complexity)
    tool_registry.register("detect_issues", detect_issues)
    tool_registry.register("suggest_improvements", suggest_improvements)

# Register immediately when imported
register_workflow_tools()
