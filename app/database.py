import aiosqlite
from typing import Optional
import json
from datetime import datetime

class Database:
    def __init__(self, db_path: str = "./workflow_engine.db"):
        self.db_path = db_path
        self.connection: Optional[aiosqlite.Connection] = None
    
    async def connect(self):
        self.connection = await aiosqlite.connect(self.db_path)
        await self.create_tables()
    
    async def disconnect(self):
        if self.connection:
            await self.connection.close()
    
    async def create_tables(self):
        await self.connection.execute("""
            CREATE TABLE IF NOT EXISTS graphs (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                definition TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await self.connection.execute("""
            CREATE TABLE IF NOT EXISTS executions (
                id TEXT PRIMARY KEY,
                graph_id TEXT NOT NULL,
                status TEXT NOT NULL,
                current_state TEXT,
                execution_log TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (graph_id) REFERENCES graphs(id)
            )
        """)
        
        await self.connection.commit()
    
    async def save_graph(self, graph_id: str, name: str, definition: dict):
        await self.connection.execute(
            "INSERT OR REPLACE INTO graphs (id, name, definition) VALUES (?, ?, ?)",
            (graph_id, name, json.dumps(definition))
        )
        await self.connection.commit()
    
    async def get_graph(self, graph_id: str) -> Optional[dict]:
        cursor = await self.connection.execute(
            "SELECT definition FROM graphs WHERE id = ?", (graph_id,)
        )
        row = await cursor.fetchone()
        return json.loads(row[0]) if row else None
    
    async def save_execution(self, execution_id: str, graph_id: str, status: str, 
                            state: dict, log: list):
        await self.connection.execute(
            """INSERT OR REPLACE INTO executions 
               (id, graph_id, status, current_state, execution_log, updated_at) 
               VALUES (?, ?, ?, ?, ?, ?)""",
            (execution_id, graph_id, status, json.dumps(state), 
             json.dumps(log), datetime.utcnow().isoformat())
        )
        await self.connection.commit()
    
    async def get_execution(self, execution_id: str) -> Optional[dict]:
        cursor = await self.connection.execute(
            "SELECT graph_id, status, current_state, execution_log FROM executions WHERE id = ?",
            (execution_id,)
        )
        row = await cursor.fetchone()
        if row:
            return {
                "graph_id": row[0],
                "status": row[1],
                "state": json.loads(row[2]) if row[2] else {},
                "log": json.loads(row[3]) if row[3] else []
            }
        return None

db = Database()
