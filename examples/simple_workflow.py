
import asyncio
import httpx

async def main():
    base_url = "http://localhost:8000/api/v1"
    
    async with httpx.AsyncClient() as client:
        # 1. Create a simple workflow
        print("Creating workflow...")
        graph_response = await client.post(
            f"{base_url}/graph/create",
            json={
                "definition": {
                    "name": "Simple Code Analyzer",
                    "nodes": [
                        {"name": "extract", "type": "standard", "tool": "extract_functions"},
                        {"name": "complexity", "type": "standard", "tool": "check_complexity"}
                    ],
                    "edges": [
                        {"from_node": "extract", "to_node": "complexity"}
                    ],
                    "start_node": "extract"
                }
            }
        )
        graph_data = graph_response.json()
        graph_id = graph_data["graph_id"]
        print(f"✓ Created graph: {graph_id}")
        
        # 2. Execute the workflow
        print("\nExecuting workflow...")
        run_response = await client.post(
            f"{base_url}/graph/run",
            json={
                "graph_id": graph_id,
                "initial_state": {
                    "code": """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)
                    """
                }
            }
        )
        run_data = run_response.json()
        execution_id = run_data["execution_id"]
        print(f"✓ Started execution: {execution_id}")
        
        # 3. Poll for results
        print("\nWaiting for completion...")
        await asyncio.sleep(2)  # Give it time to complete
        
        state_response = await client.get(f"{base_url}/graph/state/{execution_id}")
        state_data = state_response.json()
        
        print("\n" + "="*60)
        print("EXECUTION RESULTS")
        print("="*60)
        print(f"Status: {state_data['status']}")
        print(f"\nFunctions found: {state_data['current_state'].get('functions', [])}")
        print(f"Complexity score: {state_data['current_state'].get('complexity_score', 'N/A')}")
        print(f"Complexity level: {state_data['current_state'].get('complexity_level', 'N/A')}")
        print(f"\nExecution log entries: {len(state_data['execution_log'])}")

if __name__ == "__main__":
    asyncio.run(main())