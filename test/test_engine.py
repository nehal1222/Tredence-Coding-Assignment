import pytest
import asyncio
from app.core.engine import WorkflowEngine
from app.core.state import WorkflowState
from app.core.registry import tool_registry
from app.models.schemas import GraphDefinition, NodeConfig, EdgeConfig, NodeType

# Test tools
def add_ten(state):
    return {"value": state.get("value", 0) + 10}

def multiply_by_two(state):
    return {"value": state.get("value", 0) * 2}

def check_threshold(state):
    value = state.get("value", 0)
    return {"passed": value > 50}

@pytest.fixture
def setup_tools():
    tool_registry.register("add_ten", add_ten)
    tool_registry.register("multiply_by_two", multiply_by_two)
    tool_registry.register("check_threshold", check_threshold)

@pytest.mark.asyncio
async def test_simple_workflow(setup_tools):
    """Test a simple linear workflow"""
    graph_def = GraphDefinition(
        name="Simple Test",
        nodes=[
            NodeConfig(name="add", type=NodeType.STANDARD, tool="add_ten"),
            NodeConfig(name="multiply", type=NodeType.STANDARD, tool="multiply_by_two"),
        ],
        edges=[
            EdgeConfig(from_node="add", to_node="multiply"),
        ],
        start_node="add"
    )
    
    engine = WorkflowEngine(graph_def)
    final_state, log = await engine.execute({"value": 5})
    
    assert final_state.data["value"] == 30  # (5 + 10) * 2
    assert len(log) == 2

@pytest.mark.asyncio
async def test_conditional_branching(setup_tools):
    """Test conditional edge routing"""
    graph_def = GraphDefinition(
        name="Conditional Test",
        nodes=[
            NodeConfig(name="add", type=NodeType.STANDARD, tool="add_ten"),
            NodeConfig(name="check", type=NodeType.STANDARD, tool="check_threshold"),
            NodeConfig(name="multiply", type=NodeType.STANDARD, tool="multiply_by_two"),
        ],
        edges=[
            EdgeConfig(from_node="add", to_node="check"),
            EdgeConfig(from_node="check", to_node="multiply", condition="passed == True"),
        ],
        start_node="add"
    )
    
    engine = WorkflowEngine(graph_def)
    
    # Test with value that passes threshold
    final_state, log = await engine.execute({"value": 50})
    assert "passed" in final_state.data
    assert final_state.data["passed"] == True

@pytest.mark.asyncio
async def test_loop_node(setup_tools):
    """Test loop execution"""
    def increment(state):
        return {"counter": state.get("counter", 0) + 1}
    
    tool_registry.register("increment", increment)
    
    graph_def = GraphDefinition(
        name="Loop Test",
        nodes=[
            NodeConfig(
                name="loop",
                type=NodeType.LOOP,
                tool="increment",
                loop_condition="counter < 5",
                max_iterations=10
            ),
        ],
        edges=[],
        start_node="loop"
    )
    
    engine = WorkflowEngine(graph_def)
    final_state, log = await engine.execute({"counter": 0})
    
    assert final_state.data["counter"] == 5
    assert final_state.metadata["iteration_count"] >= 5