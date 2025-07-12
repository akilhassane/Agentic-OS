#!/usr/bin/env python3
"""
Agentic OS - Demo Version (Simplified)
Runs with just standard Python libraries
"""

import asyncio
import json
import sqlite3
import random
import time
from datetime import datetime
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading

class AgenticOSDemo:
    def __init__(self):
        self.businesses = []
        self.agents = []
        self.metrics = []
        self.running = False
        self.start_time = None
        
        # Initialize database
        self.init_database()
        
    def init_database(self):
        """Initialize SQLite database"""
        Path("data").mkdir(exist_ok=True)
        self.conn = sqlite3.connect("data/agentic_os.db", check_same_thread=False)
        
        # Create tables
        self.conn.executescript('''
            CREATE TABLE IF NOT EXISTS businesses (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS agents (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                business_id INTEGER,
                status TEXT DEFAULT 'running'
            );
            
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                business_id INTEGER,
                customer_email TEXT,
                amount REAL,
                status TEXT DEFAULT 'completed',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        
        self.conn.commit()
        print("✅ Database initialized")
    
    def create_dropshipping_business(self, name, niche="general"):
        """Create a dropshipping business"""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO businesses (name, type) VALUES (?, ?)",
            (name, "dropshipping")
        )
        business_id = cursor.lastrowid
        
        # Create associated agents
        cursor.execute(
            "INSERT INTO agents (name, type, business_id) VALUES (?, ?, ?)",
            (f"{name} - Product Research Agent", "dropshipping", business_id)
        )
        cursor.execute(
            "INSERT INTO agents (name, type, business_id) VALUES (?, ?, ?)",
            (f"{name} - Customer Service Agent", "customer_service", business_id)
        )
        cursor.execute(
            "INSERT INTO agents (name, type, business_id) VALUES (?, ?, ?)",
            (f"{name} - Monitor Agent", "monitor", business_id)
        )
        
        self.conn.commit()
        
        print(f"✅ Created dropshipping business: {name} (ID: {business_id})")
        return business_id
    
    def simulate_business_activity(self):
        """Simulate business activity"""
        cursor = self.conn.cursor()
        
        # Get all active businesses
        cursor.execute("SELECT id, name FROM businesses WHERE status = 'active'")
        businesses = cursor.fetchall()
        
        for business_id, business_name in businesses:
            # Simulate random orders
            if random.random() < 0.3:  # 30% chance of new order
                customer_email = f"customer{random.randint(1000, 9999)}@example.com"
                amount = random.uniform(10, 200)
                
                cursor.execute(
                    "INSERT INTO orders (business_id, customer_email, amount) VALUES (?, ?, ?)",
                    (business_id, customer_email, amount)
                )
                
                print(f"💰 New order for {business_name}: ${amount:.2f}")
        
        self.conn.commit()
    
    def get_system_status(self):
        """Get system status"""
        cursor = self.conn.cursor()
        
        # Count businesses
        cursor.execute("SELECT COUNT(*) FROM businesses WHERE status = 'active'")
        active_businesses = cursor.fetchone()[0]
        
        # Count agents
        cursor.execute("SELECT COUNT(*) FROM agents WHERE status = 'running'")
        active_agents = cursor.fetchone()[0]
        
        # Calculate total revenue
        cursor.execute("SELECT SUM(amount) FROM orders")
        total_revenue = cursor.fetchone()[0] or 0
        
        # Calculate today's revenue
        cursor.execute(
            "SELECT SUM(amount) FROM orders WHERE date(created_at) = date('now')"
        )
        today_revenue = cursor.fetchone()[0] or 0
        
        uptime = str(datetime.now() - self.start_time) if self.start_time else "0:00:00"
        
        return {
            "status": "running" if self.running else "stopped",
            "uptime": uptime,
            "active_businesses": active_businesses,
            "active_agents": active_agents,
            "total_revenue": total_revenue,
            "today_revenue": today_revenue,
            "system_health": "healthy"
        }
    
    def get_all_businesses(self):
        """Get all businesses"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT b.id, b.name, b.type, b.status, b.created_at,
                   COUNT(o.id) as order_count,
                   COALESCE(SUM(o.amount), 0) as total_revenue
            FROM businesses b
            LEFT JOIN orders o ON b.id = o.business_id
            GROUP BY b.id, b.name, b.type, b.status, b.created_at
            ORDER BY b.created_at DESC
        """)
        
        businesses = []
        for row in cursor.fetchall():
            businesses.append({
                "id": row[0],
                "name": row[1],
                "type": row[2],
                "status": row[3],
                "created_at": row[4],
                "order_count": row[5],
                "total_revenue": row[6]
            })
        
        return businesses
    
    def get_all_agents(self):
        """Get all agents"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, type, business_id, status FROM agents")
        
        agents = []
        for row in cursor.fetchall():
            agents.append({
                "id": row[0],
                "name": row[1],
                "type": row[2],
                "business_id": row[3],
                "status": row[4]
            })
        
        return agents
    
    async def start(self):
        """Start the Agentic OS"""
        print("🚀 Starting Agentic OS Demo...")
        
        self.running = True
        self.start_time = datetime.now()
        
        # Start web server in background
        server_thread = threading.Thread(target=self.start_web_server)
        server_thread.daemon = True
        server_thread.start()
        
        print("✅ Agentic OS Demo started successfully!")
        print("📊 Dashboard: http://localhost:8080")
        print("🤖 System is now running autonomous business operations...")
        
        # Main loop
        try:
            while self.running:
                # Simulate business activity
                self.simulate_business_activity()
                
                # Print status every 30 seconds
                status = self.get_system_status()
                print(f"💼 Status: {status['active_businesses']} businesses, "
                      f"{status['active_agents']} agents, "
                      f"${status['total_revenue']:.2f} total revenue")
                
                await asyncio.sleep(10)  # Run every 10 seconds for demo
                
        except KeyboardInterrupt:
            print("\n🛑 Shutting down Agentic OS...")
            self.running = False
    
    def start_web_server(self):
        """Start simple web server"""
        server = HTTPServer(('localhost', 8080), AgenticOSRequestHandler)
        server.agentic_os = self
        server.serve_forever()

class AgenticOSRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == "/":
            self.serve_dashboard()
        elif parsed_path.path == "/api/status":
            self.serve_api_status()
        elif parsed_path.path == "/api/businesses":
            self.serve_api_businesses()
        elif parsed_path.path == "/api/agents":
            self.serve_api_agents()
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == "/api/businesses/dropshipping":
            self.create_dropshipping_business()
        else:
            self.send_error(404)
    
    def serve_dashboard(self):
        """Serve the main dashboard"""
        html = '''
<!DOCTYPE html>
<html>
<head>
    <title>🤖 Agentic OS - Demo</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; 
               background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
               color: white; min-height: 100vh; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 40px; }
        .header h1 { font-size: 3rem; margin: 0; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .card { background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; 
                backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2); }
        .card h3 { margin-top: 0; }
        .metric { display: flex; justify-content: space-between; margin: 10px 0; }
        .value { font-weight: bold; font-size: 1.2em; }
        .button { background: #4CAF50; color: white; padding: 10px 20px; border: none; 
                  border-radius: 5px; cursor: pointer; margin: 5px; }
        .button:hover { background: #45a049; }
        .status-healthy { color: #4CAF50; }
        #log { background: rgba(0,0,0,0.3); padding: 15px; border-radius: 5px; 
               height: 200px; overflow-y: auto; font-family: monospace; font-size: 0.9em; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Agentic OS</h1>
            <p>Autonomous Business Management System - Demo</p>
        </div>
        
        <div class="grid">
            <div class="card">
                <h3>📊 System Status</h3>
                <div class="metric">
                    <span>Status:</span>
                    <span class="value status-healthy" id="status">●</span>
                </div>
                <div class="metric">
                    <span>Uptime:</span>
                    <span class="value" id="uptime">--:--:--</span>
                </div>
                <div class="metric">
                    <span>Active Businesses:</span>
                    <span class="value" id="businesses">0</span>
                </div>
                <div class="metric">
                    <span>Active Agents:</span>
                    <span class="value" id="agents">0</span>
                </div>
            </div>
            
            <div class="card">
                <h3>💰 Revenue Dashboard</h3>
                <div class="metric">
                    <span>Total Revenue:</span>
                    <span class="value" id="total-revenue">$0.00</span>
                </div>
                <div class="metric">
                    <span>Today's Revenue:</span>
                    <span class="value" id="today-revenue">$0.00</span>
                </div>
                <div class="metric">
                    <span>Growth Rate:</span>
                    <span class="value">+15%</span>
                </div>
            </div>
            
            <div class="card">
                <h3>🚀 Quick Actions</h3>
                <button class="button" onclick="createBusiness()">
                    🛒 Create Dropshipping Business
                </button>
                <button class="button" onclick="viewBusinesses()">
                    📈 View All Businesses
                </button>
                <button class="button" onclick="viewAgents()">
                    🤖 View All Agents
                </button>
            </div>
            
            <div class="card">
                <h3>📝 Activity Log</h3>
                <div id="log">
                    System initialized successfully...<br>
                    Autonomous agents are running...<br>
                    Monitoring business operations...<br>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        function updateStatus() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('uptime').textContent = data.uptime;
                    document.getElementById('businesses').textContent = data.active_businesses;
                    document.getElementById('agents').textContent = data.active_agents;
                    document.getElementById('total-revenue').textContent = '$' + data.total_revenue.toFixed(2);
                    document.getElementById('today-revenue').textContent = '$' + data.today_revenue.toFixed(2);
                })
                .catch(error => console.error('Error:', error));
        }
        
        function createBusiness() {
            const name = prompt('Enter business name:');
            if (name) {
                fetch('/api/businesses/dropshipping', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({name: name})
                })
                .then(response => response.json())
                .then(data => {
                    alert('Dropshipping business created successfully!');
                    updateStatus();
                })
                .catch(error => alert('Error creating business'));
            }
        }
        
        function viewBusinesses() {
            fetch('/api/businesses')
                .then(response => response.json())
                .then(data => {
                    let info = 'Businesses:\\n\\n';
                    data.forEach(b => {
                        info += `${b.name} (${b.type})\\n`;
                        info += `  Orders: ${b.order_count}, Revenue: $${b.total_revenue.toFixed(2)}\\n\\n`;
                    });
                    alert(info);
                });
        }
        
        function viewAgents() {
            fetch('/api/agents')
                .then(response => response.json())
                .then(data => {
                    let info = 'Active Agents:\\n\\n';
                    data.forEach(a => {
                        info += `${a.name} (${a.type}) - ${a.status}\\n`;
                    });
                    alert(info);
                });
        }
        
        // Update status every 5 seconds
        updateStatus();
        setInterval(updateStatus, 5000);
        
        // Add some activity to the log
        function addLogEntry(message) {
            const log = document.getElementById('log');
            const time = new Date().toLocaleTimeString();
            log.innerHTML += `[${time}] ${message}<br>`;
            log.scrollTop = log.scrollHeight;
        }
        
        setInterval(() => {
            const activities = [
                '🔍 Agent researched trending product: Smart Water Bottle',
                '💬 Customer service agent handled inquiry in 2 minutes',
                '📢 Marketing agent created new Instagram campaign',
                '⚡ Pricing optimization improved margins by 8%',
                '📦 Order fulfilled automatically to customer',
                '📊 Business performance analysis completed'
            ];
            addLogEntry(activities[Math.floor(Math.random() * activities.length)]);
        }, 8000);
    </script>
</body>
</html>
        '''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def serve_api_status(self):
        """Serve system status API"""
        status = self.server.agentic_os.get_system_status()
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(status).encode())
    
    def serve_api_businesses(self):
        """Serve businesses API"""
        businesses = self.server.agentic_os.get_all_businesses()
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(businesses).encode())
    
    def serve_api_agents(self):
        """Serve agents API"""
        agents = self.server.agentic_os.get_all_agents()
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(agents).encode())
    
    def create_dropshipping_business(self):
        """Create dropshipping business via API"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            business_id = self.server.agentic_os.create_dropshipping_business(
                data.get('name', 'New Dropshipping Business')
            )
            
            response = {"id": business_id, "status": "created"}
            
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_error(500, str(e))
    
    def log_message(self, format, *args):
        """Suppress log messages"""
        pass

async def main():
    """Main function"""
    agentic_os = AgenticOSDemo()
    await agentic_os.start()

if __name__ == "__main__":
    print("🤖 Agentic OS - Autonomous Business Management System")
    print("=" * 60)
    print("📝 Demo Version - Simplified for demonstration")
    print("🌟 Features:")
    print("   • Autonomous dropshipping business creation")
    print("   • AI-powered agents for business management")
    print("   • Real-time monitoring and analytics")
    print("   • Automatic order processing simulation")
    print("   • Web dashboard interface")
    print("=" * 60)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Thank you for trying Agentic OS!")
        print("💡 This demo shows autonomous business management capabilities")
        print("🚀 The full version includes advanced AI integrations and scaling")