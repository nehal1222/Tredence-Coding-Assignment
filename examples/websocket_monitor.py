import asyncio
import websockets
import json
import httpx

async def monitor_execution(execution_id: str):
    uri = f"ws://localhost:8000/api/v1/ws/execution/{execution_id}"
    
    print(f"Connecting to WebSocket: {uri}")
    
    async with websockets.connect(uri) as websocket:
        print("✓ Connected! Monitoring execution...\n")
        
        while True:
            try:
                message = await websocket.recv()
                data = json.loads(message)
                
                print(f"Status: {data['status']}")
                print(f"State keys: {list(data.get('current_state', {}).keys())}")
                print(f"Log entries: {data.get('log_count', 0)}")
                print("-" * 40)
                
                if data['status'] in ['completed', 'failed']:
                    print(f"\n✓ Execution {data['status']}")
                    break
                    
            except websockets.exceptions.ConnectionClosed:
                print("Connection closed")
                break

async def main():
    # First, start an execution
    base_url = "http://localhost:8000/api/v1"
    
    async with httpx.AsyncClient() as client:
        # Create and run a workflow
        graph_response = await client.post(
            f"{base_url}/graph/create",
            json={
                "definition": {
                    "name": "WS Monitor Test",
                    "nodes": [
                        {"name": "extract", "type": "standard", "tool": "extract_functions"},
                        {"name": "complexity", "type": "standard", "tool": "check_complexity"}
                    ],
                    "edges": [{"from_node": "extract", "to_node": "complexity"}],
                    "start_node": "extract"
                }
            }
        )
        graph_id = graph_response.json()["graph_id"]
        
        run_response = await client.post(
            f"{base_url}/graph/run",
            json={
                "graph_id": graph_id,
                "initial_state": {"code": "def test(): pass"}
            }
        )
        execution_id = run_response.json()["execution_id"]
        
        print(f"Started execution: {execution_id}\n")
        
        # Monitor via WebSocket
        await monitor_execution(execution_id)

if __name__ == "__main__":
    asyncio.run(main())
