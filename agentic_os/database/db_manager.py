import asyncio
import sqlite3
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path

from agentic_os.core.logger import get_logger

class DatabaseManager:
    """
    Manages database operations for the Agentic OS
    """
    
    def __init__(self, db_path: str = "data/agentic_os.db"):
        self.db_path = db_path
        self.logger = get_logger("DatabaseManager")
        self._connection = None
        
    async def initialize(self):
        """Initialize the database"""
        try:
            # Ensure data directory exists
            Path(self.db_path).parent.mkdir(exist_ok=True)
            
            # Create connection
            self._connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self._connection.row_factory = sqlite3.Row
            
            # Create tables if they don't exist
            await self._create_tables()
            
            self.logger.info("Database initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize database: {e}")
            raise
    
    async def _create_tables(self):
        """Create database tables"""
        cursor = self._connection.cursor()
        
        # Businesses table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS businesses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                status TEXT DEFAULT 'active',
                config TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Agents table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                business_id INTEGER,
                status TEXT DEFAULT 'idle',
                config TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (business_id) REFERENCES businesses (id)
            )
        ''')
        
        # Metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                business_id INTEGER,
                metric_name TEXT NOT NULL,
                metric_value REAL,
                metadata TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (business_id) REFERENCES businesses (id)
            )
        ''')
        
        # Logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                level TEXT NOT NULL,
                message TEXT NOT NULL,
                component TEXT,
                business_id INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (business_id) REFERENCES businesses (id)
            )
        ''')
        
        # Products table for dropshipping
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                business_id INTEGER,
                name TEXT NOT NULL,
                description TEXT,
                price REAL,
                cost REAL,
                supplier_info TEXT,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (business_id) REFERENCES businesses (id)
            )
        ''')
        
        # Orders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                business_id INTEGER,
                customer_email TEXT,
                product_id INTEGER,
                quantity INTEGER,
                total_amount REAL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (business_id) REFERENCES businesses (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        self._connection.commit()
    
    # Business operations
    async def create_business(self, name: str, business_type: str, config: dict) -> int:
        """Create a new business record"""
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO businesses (name, type, config) VALUES (?, ?, ?)",
            (name, business_type, json.dumps(config))
        )
        self._connection.commit()
        return cursor.lastrowid
    
    async def get_business(self, business_id: int) -> Optional[dict]:
        """Get a business by ID"""
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM businesses WHERE id = ?", (business_id,))
        row = cursor.fetchone()
        
        if row:
            return {
                "id": row["id"],
                "name": row["name"],
                "type": row["type"],
                "status": row["status"],
                "config": json.loads(row["config"]) if row["config"] else {},
                "created_at": row["created_at"],
                "updated_at": row["updated_at"]
            }
        return None
    
    async def get_all_businesses(self) -> List[dict]:
        """Get all businesses"""
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM businesses ORDER BY created_at DESC")
        rows = cursor.fetchall()
        
        businesses = []
        for row in rows:
            businesses.append({
                "id": row["id"],
                "name": row["name"],
                "type": row["type"],
                "status": row["status"],
                "config": json.loads(row["config"]) if row["config"] else {},
                "created_at": row["created_at"],
                "updated_at": row["updated_at"]
            })
        
        return businesses
    
    async def update_business_status(self, business_id: int, status: str):
        """Update business status"""
        cursor = self._connection.cursor()
        cursor.execute(
            "UPDATE businesses SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (status, business_id)
        )
        self._connection.commit()
    
    # Agent operations
    async def create_agent(self, name: str, agent_type: str, business_id: Optional[int], config: dict) -> int:
        """Create a new agent record"""
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO agents (name, type, business_id, config) VALUES (?, ?, ?, ?)",
            (name, agent_type, business_id, json.dumps(config))
        )
        self._connection.commit()
        return cursor.lastrowid
    
    async def get_all_agents(self) -> List[dict]:
        """Get all agents"""
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM agents ORDER BY created_at DESC")
        rows = cursor.fetchall()
        
        agents = []
        for row in rows:
            agents.append({
                "id": row["id"],
                "name": row["name"],
                "type": row["type"],
                "business_id": row["business_id"],
                "status": row["status"],
                "config": json.loads(row["config"]) if row["config"] else {},
                "created_at": row["created_at"]
            })
        
        return agents
    
    async def update_agent_status(self, agent_id: int, status: str):
        """Update agent status"""
        cursor = self._connection.cursor()
        cursor.execute(
            "UPDATE agents SET status = ? WHERE id = ?",
            (status, agent_id)
        )
        self._connection.commit()
    
    # Metrics operations
    async def save_metric(self, business_id: int, metric_name: str, metric_value: float, metadata: dict = None):
        """Save a metric"""
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO metrics (business_id, metric_name, metric_value, metadata) VALUES (?, ?, ?, ?)",
            (business_id, metric_name, metric_value, json.dumps(metadata) if metadata else None)
        )
        self._connection.commit()
    
    async def get_metric(self, business_id: int, metric_name: str) -> Optional[float]:
        """Get the latest value for a metric"""
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT metric_value FROM metrics WHERE business_id = ? AND metric_name = ? ORDER BY timestamp DESC LIMIT 1",
            (business_id, metric_name)
        )
        row = cursor.fetchone()
        return row["metric_value"] if row else None
    
    async def get_metrics_history(self, business_id: int, metric_name: str, limit: int = 100) -> List[dict]:
        """Get metrics history"""
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT * FROM metrics WHERE business_id = ? AND metric_name = ? ORDER BY timestamp DESC LIMIT ?",
            (business_id, metric_name, limit)
        )
        rows = cursor.fetchall()
        
        metrics = []
        for row in rows:
            metrics.append({
                "id": row["id"],
                "metric_value": row["metric_value"],
                "metadata": json.loads(row["metadata"]) if row["metadata"] else {},
                "timestamp": row["timestamp"]
            })
        
        return metrics
    
    # Product operations (for dropshipping)
    async def create_product(self, business_id: int, name: str, description: str, price: float, cost: float, supplier_info: dict) -> int:
        """Create a new product"""
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO products (business_id, name, description, price, cost, supplier_info) VALUES (?, ?, ?, ?, ?, ?)",
            (business_id, name, description, price, cost, json.dumps(supplier_info))
        )
        self._connection.commit()
        return cursor.lastrowid
    
    async def get_products(self, business_id: int) -> List[dict]:
        """Get all products for a business"""
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM products WHERE business_id = ? AND status = 'active'", (business_id,))
        rows = cursor.fetchall()
        
        products = []
        for row in rows:
            products.append({
                "id": row["id"],
                "name": row["name"],
                "description": row["description"],
                "price": row["price"],
                "cost": row["cost"],
                "supplier_info": json.loads(row["supplier_info"]) if row["supplier_info"] else {},
                "status": row["status"],
                "created_at": row["created_at"]
            })
        
        return products
    
    # Order operations
    async def create_order(self, business_id: int, customer_email: str, product_id: int, quantity: int, total_amount: float) -> int:
        """Create a new order"""
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO orders (business_id, customer_email, product_id, quantity, total_amount) VALUES (?, ?, ?, ?, ?)",
            (business_id, customer_email, product_id, quantity, total_amount)
        )
        self._connection.commit()
        return cursor.lastrowid
    
    async def get_orders(self, business_id: int) -> List[dict]:
        """Get all orders for a business"""
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM orders WHERE business_id = ? ORDER BY created_at DESC", (business_id,))
        rows = cursor.fetchall()
        
        orders = []
        for row in rows:
            orders.append({
                "id": row["id"],
                "customer_email": row["customer_email"],
                "product_id": row["product_id"],
                "quantity": row["quantity"],
                "total_amount": row["total_amount"],
                "status": row["status"],
                "created_at": row["created_at"]
            })
        
        return orders
    
    async def health_check(self) -> bool:
        """Check database health"""
        try:
            cursor = self._connection.cursor()
            cursor.execute("SELECT 1")
            return True
        except Exception as e:
            self.logger.error(f"Database health check failed: {e}")
            return False
    
    async def close(self):
        """Close the database connection"""
        if self._connection:
            self._connection.close()
            self.logger.info("Database connection closed")