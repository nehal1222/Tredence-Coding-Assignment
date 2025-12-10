from app.core.registry import tool_registry
# Use relative imports
from .tools import extract_functions, check_complexity, detect_issues, suggest_improvements
from ..core.registry import tool_registry
from ..models.schemas import GraphDefinition, NodeConfig, EdgeConfig, NodeType

from app.models.schemas import GraphDefinition, NodeConfig, EdgeConfig, NodeType

def register_code_review_tools():
    """Register all code review tools"""
    tool_registry.register("extract_functions", extract_functions)
    tool_registry.register("check_complexity", check_complexity)
    tool_registry.register("detect_issues", detect_issues)
    tool_registry.register("suggest_improvements", suggest_improvements)

def get_code_review_workflow() -> GraphDefinition:
    """Get the code review workflow definition"""
    return GraphDefinition(
        name="Code Review Agent",
        nodes=[
            NodeConfig(name="extract", type=NodeType.STANDARD, tool="extract_functions"),
            NodeConfig(name="complexity", type=NodeType.STANDARD, tool="check_complexity"),
            NodeConfig(name="issues", type=NodeType.STANDARD, tool="detect_issues"),
            NodeConfig(
                name="improve",
                type=NodeType.LOOP,
                tool="suggest_improvements",
                loop_condition="quality_score < 80",
                max_iterations=3
            )
        ],
        edges=[
            EdgeConfig(from_node="extract", to_node="complexity"),
            EdgeConfig(from_node="complexity", to_node="issues"),
            EdgeConfig(from_node="issues", to_node="improve"),
        ],
        start_node="extract"
    )
