from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import logging

logger = logging.getLogger(__name__)
ws_router = APIRouter()

@ws_router.websocket("/ws/execution/{execution_id}")
async def websocket_execution_stream(websocket: WebSocket, execution_id: str):
    await websocket.accept()
    
    try:
        from app.api.routes import active_executions
        
        while True:
            if execution_id in active_executions:
                exec_data = active_executions[execution_id]
                
                # Send full logs along with status and current state
                await websocket.send_json({
                    "execution_id": execution_id,
                    "status": exec_data["status"],
                    "current_state": exec_data["state"],
                    "logs": exec_data["log"]
                })
                
                # Stop streaming if workflow is completed or failed
                if exec_data["status"] in ["completed", "failed"]:
                    break
            
            await asyncio.sleep(0.5)
        
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for execution {execution_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.close()
