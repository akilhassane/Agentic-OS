from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json

from agentic_os.core.logger import get_logger

class BusinessConfig(BaseModel):
    name: str
    type: str
    config: Dict[str, Any]

class AgentConfig(BaseModel):
    name: str
    type: str
    business_id: Optional[int] = None
    config: Dict[str, Any]

def create_app(os_controller):
    """Create and configure the FastAPI application"""
    
    app = FastAPI(
        title="Agentic OS API",
        description="API for autonomous business management system",
        version="1.0.0"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    logger = get_logger("API")
    
    # Dependency to get OS controller
    def get_controller():
        return os_controller
    
    # System status endpoints
    @app.get("/")
    async def root():
        """Root endpoint - returns dashboard"""
        return HTMLResponse(content=get_dashboard_html(), status_code=200)
    
    @app.get("/api/status")
    async def get_system_status(controller = Depends(get_controller)):
        """Get overall system status"""
        try:
            status = await controller.get_system_status()
            return JSONResponse(content=status)
        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    # Business management endpoints
    @app.get("/api/businesses")
    async def get_businesses(controller = Depends(get_controller)):
        """Get all businesses"""
        try:
            businesses = await controller.get_all_businesses()
            return JSONResponse(content=businesses)
        except Exception as e:
            logger.error(f"Error getting businesses: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/api/businesses")
    async def create_business(
        business_config: BusinessConfig,
        controller = Depends(get_controller)
    ):
        """Create a new business"""
        try:
            business = await controller.create_business(business_config.dict())
            return JSONResponse(content=business, status_code=201)
        except Exception as e:
            logger.error(f"Error creating business: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/api/businesses/{business_id}")
    async def get_business_status(
        business_id: int,
        controller = Depends(get_controller)
    ):
        """Get status of a specific business"""
        try:
            status = await controller.get_business_status(business_id)
            if not status:
                raise HTTPException(status_code=404, detail="Business not found")
            return JSONResponse(content=status)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting business status: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    # Agent management endpoints
    @app.get("/api/agents")
    async def get_agents(controller = Depends(get_controller)):
        """Get all agents"""
        try:
            agents = await controller.get_all_agents()
            return JSONResponse(content=agents)
        except Exception as e:
            logger.error(f"Error getting agents: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    # Dropshipping specific endpoints
    @app.post("/api/businesses/dropshipping")
    async def create_dropshipping_business(
        name: str,
        niche: str = "general",
        controller = Depends(get_controller)
    ):
        """Create a new dropshipping business"""
        try:
            config = {
                "name": name,
                "type": "dropshipping",
                "config": {
                    "niche": niche,
                    "target_margin": 0.3,
                    "auto_pricing": True,
                    "auto_fulfillment": True
                }
            }
            business = await controller.create_business(config)
            return JSONResponse(content=business, status_code=201)
        except Exception as e:
            logger.error(f"Error creating dropshipping business: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    return app

def get_dashboard_html():
    """Return the dashboard HTML"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Agentic OS Dashboard</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #fff;
            }
            .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
            .header { text-align: center; margin-bottom: 40px; }
            .header h1 { font-size: 3rem; margin-bottom: 10px; }
            .header p { font-size: 1.2rem; opacity: 0.9; }
            .dashboard-grid { 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
                gap: 20px; 
                margin-bottom: 40px;
            }
            .card { 
                background: rgba(255, 255, 255, 0.1); 
                backdrop-filter: blur(10px);
                border-radius: 15px; 
                padding: 25px; 
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            .card h3 { margin-bottom: 15px; font-size: 1.5rem; }
            .stat { display: flex; justify-content: space-between; margin: 10px 0; }
            .stat-value { font-weight: bold; font-size: 1.1rem; }
            .button { 
                background: rgba(255, 255, 255, 0.2); 
                border: none; 
                color: white; 
                padding: 12px 24px; 
                border-radius: 8px; 
                cursor: pointer; 
                margin: 5px;
                transition: all 0.3s ease;
            }
            .button:hover { background: rgba(255, 255, 255, 0.3); transform: translateY(-2px); }
            .button.primary { background: #4CAF50; }
            .button.primary:hover { background: #45a049; }
            .logs { 
                background: rgba(0, 0, 0, 0.3); 
                border-radius: 10px; 
                padding: 20px; 
                font-family: monospace; 
                height: 200px; 
                overflow-y: auto;
            }
            .status-indicator { 
                display: inline-block; 
                width: 12px; 
                height: 12px; 
                border-radius: 50%; 
                margin-right: 8px;
            }
            .status-healthy { background: #4CAF50; }
            .status-degraded { background: #FF9800; }
            .status-error { background: #F44336; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 Agentic OS</h1>
                <p>Autonomous Business Management System</p>
            </div>
            
            <div class="dashboard-grid">
                <div class="card">
                    <h3>System Status</h3>
                    <div class="stat">
                        <span>Health:</span>
                        <span class="stat-value">
                            <span class="status-indicator status-healthy"></span>
                            <span id="system-health">Healthy</span>
                        </span>
                    </div>
                    <div class="stat">
                        <span>Uptime:</span>
                        <span class="stat-value" id="uptime">--:--:--</span>
                    </div>
                    <div class="stat">
                        <span>Active Businesses:</span>
                        <span class="stat-value" id="active-businesses">0</span>
                    </div>
                    <div class="stat">
                        <span>Active Agents:</span>
                        <span class="stat-value" id="active-agents">0</span>
                    </div>
                </div>
                
                <div class="card">
                    <h3>Revenue Overview</h3>
                    <div class="stat">
                        <span>Total Revenue:</span>
                        <span class="stat-value" id="total-revenue">$0.00</span>
                    </div>
                    <div class="stat">
                        <span>Today's Revenue:</span>
                        <span class="stat-value">$0.00</span>
                    </div>
                    <div class="stat">
                        <span>Growth Rate:</span>
                        <span class="stat-value">+0%</span>
                    </div>
                </div>
                
                <div class="card">
                    <h3>Quick Actions</h3>
                    <button class="button primary" onclick="createDropshippingBusiness()">
                        🛒 Create Dropshipping Business
                    </button>
                    <button class="button" onclick="viewBusinesses()">
                        📊 View All Businesses
                    </button>
                    <button class="button" onclick="viewAgents()">
                        🤖 Manage Agents
                    </button>
                    <button class="button" onclick="viewLogs()">
                        📝 View System Logs
                    </button>
                </div>
                
                <div class="card">
                    <h3>Recent Activity</h3>
                    <div class="logs" id="activity-logs">
                        System initialized successfully...<br>
                        Waiting for activities...
                    </div>
                </div>
            </div>
            
            <div class="card">
                <h3>API Documentation</h3>
                <p>Access the interactive API documentation at <a href="/docs" style="color: #4CAF50;">/docs</a></p>
                <p>View the system status API at <a href="/api/status" style="color: #4CAF50;">/api/status</a></p>
            </div>
        </div>
        
        <script>
            // Update system status every 30 seconds
            async function updateStatus() {
                try {
                    const response = await fetch('/api/status');
                    const data = await response.json();
                    
                    document.getElementById('system-health').textContent = data.stats.system_health;
                    document.getElementById('uptime').textContent = data.uptime;
                    document.getElementById('active-businesses').textContent = data.stats.active_businesses;
                    document.getElementById('active-agents').textContent = data.stats.active_agents;
                    document.getElementById('total-revenue').textContent = '$' + data.stats.total_revenue.toFixed(2);
                    
                    // Update health indicator
                    const indicator = document.querySelector('.status-indicator');
                    indicator.className = 'status-indicator status-' + data.stats.system_health;
                    
                } catch (error) {
                    console.error('Error updating status:', error);
                }
            }
            
            async function createDropshippingBusiness() {
                const name = prompt('Enter business name:');
                if (name) {
                    try {
                        const response = await fetch('/api/businesses/dropshipping', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                            body: `name=${encodeURIComponent(name)}&niche=general`
                        });
                        if (response.ok) {
                            alert('Dropshipping business created successfully!');
                            updateStatus();
                        } else {
                            alert('Error creating business');
                        }
                    } catch (error) {
                        alert('Error: ' + error.message);
                    }
                }
            }
            
            function viewBusinesses() {
                window.open('/api/businesses', '_blank');
            }
            
            function viewAgents() {
                window.open('/api/agents', '_blank');
            }
            
            function viewLogs() {
                alert('Logs viewer coming soon!');
            }
            
            // Initial status update
            updateStatus();
            
            // Update status every 30 seconds
            setInterval(updateStatus, 30000);
        </script>
    </body>
    </html>
    """