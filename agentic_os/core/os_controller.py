import asyncio
import json
from typing import Dict, List, Optional
from datetime import datetime

from agentic_os.core.logger import get_logger
from agentic_os.agents.agent_manager import AgentManager
from agentic_os.business_modules.business_manager import BusinessManager
from agentic_os.monitoring.monitor import SystemMonitor
from agentic_os.database.db_manager import DatabaseManager

class AgenticOSController:
    """
    Main controller for the Agentic OS
    Orchestrates all agents, business modules, and monitoring systems
    """
    
    def __init__(self):
        self.logger = get_logger("OSController")
        self.running = False
        
        # Core components
        self.db_manager = DatabaseManager()
        self.agent_manager = AgentManager(self.db_manager)
        self.business_manager = BusinessManager(self.db_manager)
        self.monitor = SystemMonitor(self.db_manager)
        
        # System state
        self.system_stats = {
            "start_time": None,
            "active_businesses": 0,
            "active_agents": 0,
            "total_revenue": 0.0,
            "system_health": "healthy"
        }
        
    async def start(self):
        """Start the Agentic OS and all its components"""
        try:
            self.logger.info("Starting Agentic OS Controller...")
            
            # Initialize database
            await self.db_manager.initialize()
            
            # Start core components
            await self.agent_manager.start()
            await self.business_manager.start()
            await self.monitor.start()
            
            # Set system state
            self.running = True
            self.system_stats["start_time"] = datetime.now()
            
            # Start main control loop
            asyncio.create_task(self._main_loop())
            
            self.logger.info("✅ Agentic OS Controller started successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to start OS Controller: {e}")
            raise
    
    async def stop(self):
        """Stop the Agentic OS and all its components"""
        try:
            self.logger.info("Stopping Agentic OS Controller...")
            
            self.running = False
            
            # Stop all components
            await self.monitor.stop()
            await self.business_manager.stop()
            await self.agent_manager.stop()
            await self.db_manager.close()
            
            self.logger.info("✅ Agentic OS Controller stopped successfully")
            
        except Exception as e:
            self.logger.error(f"Error stopping OS Controller: {e}")
    
    async def _main_loop(self):
        """Main control loop for the OS"""
        while self.running:
            try:
                # Update system statistics
                await self._update_system_stats()
                
                # Perform health checks
                await self._health_check()
                
                # Auto-scale resources if needed
                await self._auto_scale()
                
                # Sleep for a bit before next iteration
                await asyncio.sleep(30)  # Run every 30 seconds
                
            except Exception as e:
                self.logger.error(f"Error in main loop: {e}")
                await asyncio.sleep(5)
    
    async def _update_system_stats(self):
        """Update system statistics"""
        try:
            # Get active businesses count
            businesses = await self.business_manager.get_all_businesses()
            self.system_stats["active_businesses"] = len([b for b in businesses if b.status == "active"])
            
            # Get active agents count
            agents = await self.agent_manager.get_all_agents()
            self.system_stats["active_agents"] = len([a for a in agents if a.status == "running"])
            
            # Calculate total revenue (placeholder for now)
            self.system_stats["total_revenue"] = await self._calculate_total_revenue()
            
        except Exception as e:
            self.logger.error(f"Error updating system stats: {e}")
    
    async def _health_check(self):
        """Perform system health checks"""
        try:
            # Check if all core components are healthy
            components_health = {
                "database": await self.db_manager.health_check(),
                "agents": await self.agent_manager.health_check(),
                "businesses": await self.business_manager.health_check(),
                "monitor": await self.monitor.health_check()
            }
            
            # Determine overall health
            if all(components_health.values()):
                self.system_stats["system_health"] = "healthy"
            else:
                self.system_stats["system_health"] = "degraded"
                unhealthy = [k for k, v in components_health.items() if not v]
                self.logger.warning(f"Unhealthy components: {unhealthy}")
                
        except Exception as e:
            self.logger.error(f"Error in health check: {e}")
            self.system_stats["system_health"] = "error"
    
    async def _auto_scale(self):
        """Auto-scale system resources based on load"""
        try:
            # Get current system load
            active_businesses = self.system_stats["active_businesses"]
            active_agents = self.system_stats["active_agents"]
            
            # Simple scaling logic
            if active_businesses > active_agents * 0.8:
                self.logger.info("High load detected, considering scaling up...")
                # Could add more agents here
            
        except Exception as e:
            self.logger.error(f"Error in auto-scaling: {e}")
    
    async def _calculate_total_revenue(self) -> float:
        """Calculate total revenue across all businesses"""
        try:
            total = 0.0
            businesses = await self.business_manager.get_all_businesses()
            
            for business in businesses:
                # Get revenue metrics for each business
                revenue = await self.monitor.get_business_metric(business.id, "revenue")
                if revenue:
                    total += revenue
            
            return total
        except Exception as e:
            self.logger.error(f"Error calculating total revenue: {e}")
            return 0.0
    
    # API methods for external access
    async def create_business(self, business_config: dict) -> dict:
        """Create a new business through the OS"""
        return await self.business_manager.create_business(business_config)
    
    async def get_business_status(self, business_id: int) -> dict:
        """Get status of a specific business"""
        return await self.business_manager.get_business_status(business_id)
    
    async def get_system_status(self) -> dict:
        """Get overall system status"""
        return {
            "status": "running" if self.running else "stopped",
            "stats": self.system_stats,
            "uptime": str(datetime.now() - self.system_stats["start_time"]) if self.system_stats["start_time"] else "0:00:00"
        }
    
    async def get_all_businesses(self) -> List[dict]:
        """Get all businesses managed by the OS"""
        return await self.business_manager.get_all_businesses()
    
    async def get_all_agents(self) -> List[dict]:
        """Get all agents managed by the OS"""
        return await self.agent_manager.get_all_agents()