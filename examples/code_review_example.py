
import asyncio
import httpx

SAMPLE_CODE = """
def process_data(data):
    # TODO: Add input validation
    result = []
    for item in data:
        if item:
            if item > 0:
                for i in range(item):
                    if i % 2 == 0:
                        result.append(i)
    return result

def another_function():
    try:
        # Some code
        pass
    except:
        pass
"""

async def main():
    base_url = "http://localhost:8000/api/v1"
    
    async with httpx.AsyncClient() as client:
        # Create full code review workflow
        print("Creating Code Review workflow...")
        graph_response = await client.post(
            f"{base_url}/graph/create",
            json={
                "definition": {
                    "name": "Advanced Code Review",
                    "nodes": [
                        {"name": "extract", "type": "standard", "tool": "extract_functions"},
                        {"name": "complexity", "type": "standard", "tool": "check_complexity"},
                        {"name": "issues", "type": "standard", "tool": "detect_issues"},
                        {
                            "name": "improve",
                            "type": "loop",
                            "tool": "suggest_improvements",
                            "loop_condition": "quality_score < 80",
                            "max_iterations": 3
                        }
                    ],
                    "edges": [
                        {"from_node": "extract", "to_node": "complexity"},
                        {"from_node": "complexity", "to_node": "issues"},
                        {"from_node": "issues", "to_node": "improve"}
                    ],
                    "start_node": "extract"
                }
            }
        )
        graph_id = graph_response.json()["graph_id"]
        print(f"✓ Graph created: {graph_id}")
        
        # Execute
        print("\nAnalyzing code...")
        run_response = await client.post(
            f"{base_url}/graph/run",
            json={
                "graph_id": graph_id,
                "initial_state": {"code": SAMPLE_CODE}
            }
        )
        execution_id = run_response.json()["execution_id"]
        
        # Wait and get results
        await asyncio.sleep(3)
        state_response = await client.get(f"{base_url}/graph/state/{execution_id}")
        result = state_response.json()
        
        # Display results
        print("\n" + "="*70)
        print("CODE REVIEW RESULTS")
        print("="*70)
        
        state = result['current_state']
        print(f"\n📊 Analysis Summary:")
        print(f"   Functions: {state.get('function_count', 0)}")
        print(f"   Complexity: {state.get('complexity_score', 0)} ({state.get('complexity_level', 'N/A')})")
        print(f"   Issues found: {state.get('issue_count', 0)}")
        print(f"   Quality score: {state.get('quality_score', 0)}/100")
        
        if state.get('issues'):
            print(f"\n🔍 Issues Detected:")
            for issue in state['issues']:
                print(f"   • {issue}")
        
        if state.get('suggestions'):
            print(f"\n💡 Suggestions:")
            for suggestion in state['suggestions']:
                print(f"   • {suggestion}")
        
        print(f"\n📝 Execution Steps: {len(result['execution_log'])}")
        for log_entry in result['execution_log']:
            print(f"   ✓ {log_entry['node']} - {log_entry['status']}")

if __name__ == "__main__":
    asyncio.run(main())
