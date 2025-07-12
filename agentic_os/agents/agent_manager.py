import asyncio
import json
from typing import Dict, List, Optional, Any
from datetime import datetime

from agentic_os.core.logger import get_logger
from agentic_os.agents.base_agent import BaseAgent
from agentic_os.agents.dropshipping_agent import DropshippingAgent
from agentic_os.agents.monitor_agent import MonitorAgent

class AgentManager:
    """
    Manages all AI agents in the Agentic OS
    """
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.logger = get_logger("AgentManager")
        
        # Active agents registry
        self.active_agents: Dict[int, BaseAgent] = {}
        
        # Agent type registry
        self.agent_types = {
            "dropshipping": DropshippingAgent,
            "monitor": MonitorAgent,
        }
        
        self.running = False
    
    async def start(self):
        """Start the agent manager"""
        try:
            self.logger.info("Starting Agent Manager...")
            
            # Load existing agents from database
            await self._load_existing_agents()
            
            # Start monitoring loop
            self.running = True
            asyncio.create_task(self._monitoring_loop())
            
            self.logger.info("✅ Agent Manager started successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to start Agent Manager: {e}")
            raise
    
    async def stop(self):
        """Stop the agent manager and all agents"""
        try:
            self.logger.info("Stopping Agent Manager...")
            
            self.running = False
            
            # Stop all active agents
            for agent_id, agent in self.active_agents.items():
                await agent.stop()
            
            self.active_agents.clear()
            
            self.logger.info("✅ Agent Manager stopped successfully")
            
        except Exception as e:
            self.logger.error(f"Error stopping Agent Manager: {e}")
    
    async def _load_existing_agents(self):
        """Load existing agents from database and start them"""
        try:
            agents = await self.db_manager.get_all_agents()
            
            for agent_data in agents:
                if agent_data["status"] == "running":
                    await self._start_agent(agent_data)
                    
        except Exception as e:
            self.logger.error(f"Error loading existing agents: {e}")
    
    async def _monitoring_loop(self):
        """Monitor all active agents"""
        while self.running:
            try:
                # Check agent health and restart if needed
                for agent_id, agent in list(self.active_agents.items()):
                    if not agent.is_healthy():
                        self.logger.warning(f"Agent {agent_id} is unhealthy, restarting...")
                        await self._restart_agent(agent_id)
                
                # Sleep before next check
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(5)
    
    async def create_agent(self, name: str, agent_type: str, business_id: Optional[int] = None, config: dict = None) -> int:
        """Create a new agent"""
        try:
            if agent_type not in self.agent_types:
                raise ValueError(f"Unknown agent type: {agent_type}")
            
            # Create agent record in database
            agent_id = await self.db_manager.create_agent(
                name=name,
                agent_type=agent_type,
                business_id=business_id,
                config=config or {}
            )
            
            # Create and start the agent
            agent_data = {
                "id": agent_id,
                "name": name,
                "type": agent_type,
                "business_id": business_id,
                "status": "idle",
                "config": config or {}
            }
            
            await self._start_agent(agent_data)
            
            self.logger.info(f"Created and started agent: {name} (ID: {agent_id})")
            return agent_id
            
        except Exception as e:
            self.logger.error(f"Error creating agent: {e}")
            raise
    
    async def _start_agent(self, agent_data: dict):
        """Start an agent instance"""
        try:
            agent_class = self.agent_types[agent_data["type"]]
            
            # Create agent instance
            agent = agent_class(
                agent_id=agent_data["id"],
                name=agent_data["name"],
                business_id=agent_data["business_id"],
                config=agent_data["config"],
                db_manager=self.db_manager
            )
            
            # Start the agent
            await agent.start()
            
            # Add to active agents
            self.active_agents[agent_data["id"]] = agent
            
            # Update status in database
            await self.db_manager.update_agent_status(agent_data["id"], "running")
            
            self.logger.info(f"Started agent: {agent_data['name']} (ID: {agent_data['id']})")
            
        except Exception as e:
            self.logger.error(f"Error starting agent {agent_data['id']}: {e}")
            await self.db_manager.update_agent_status(agent_data["id"], "error")
    
    async def _restart_agent(self, agent_id: int):
        """Restart an agent"""
        try:
            # Stop the current agent
            if agent_id in self.active_agents:
                await self.active_agents[agent_id].stop()
                del self.active_agents[agent_id]
            
            # Get agent data from database
            agents = await self.db_manager.get_all_agents()
            agent_data = next((a for a in agents if a["id"] == agent_id), None)
            
            if agent_data:
                await self._start_agent(agent_data)
            
        except Exception as e:
            self.logger.error(f"Error restarting agent {agent_id}: {e}")
    
    async def stop_agent(self, agent_id: int):
        """Stop a specific agent"""
        try:
            if agent_id in self.active_agents:
                await self.active_agents[agent_id].stop()
                del self.active_agents[agent_id]
                
                # Update status in database
                await self.db_manager.update_agent_status(agent_id, "stopped")
                
                self.logger.info(f"Stopped agent: {agent_id}")
            
        except Exception as e:
            self.logger.error(f"Error stopping agent {agent_id}: {e}")
    
    async def get_agent_status(self, agent_id: int) -> Optional[dict]:
        """Get status of a specific agent"""
        if agent_id in self.active_agents:
            agent = self.active_agents[agent_id]
            return {
                "id": agent_id,
                "name": agent.name,
                "type": agent.agent_type,
                "status": "running" if agent.is_running() else "stopped",
                "health": "healthy" if agent.is_healthy() else "unhealthy",
                "last_activity": agent.get_last_activity(),
                "statistics": agent.get_statistics()
            }
        return None
    
    async def get_all_agents(self) -> List[dict]:
        """Get status of all agents"""
        agents = []
        
        # Get all agents from database
        db_agents = await self.db_manager.get_all_agents()
        
        for agent_data in db_agents:
            agent_id = agent_data["id"]
            
            if agent_id in self.active_agents:
                # Active agent
                agent = self.active_agents[agent_id]
                status = {
                    "id": agent_id,
                    "name": agent.name,
                    "type": agent.agent_type,
                    "business_id": agent.business_id,
                    "status": "running" if agent.is_running() else "stopped",
                    "health": "healthy" if agent.is_healthy() else "unhealthy",
                    "last_activity": agent.get_last_activity(),
                    "statistics": agent.get_statistics(),
                    "created_at": agent_data["created_at"]
                }
            else:
                # Inactive agent
                status = {
                    "id": agent_id,
                    "name": agent_data["name"],
                    "type": agent_data["type"],
                    "business_id": agent_data["business_id"],
                    "status": agent_data["status"],
                    "health": "unknown",
                    "last_activity": None,
                    "statistics": {},
                    "created_at": agent_data["created_at"]
                }
            
            agents.append(status)
        
        return agents
    
    async def health_check(self) -> bool:
        """Check if agent manager is healthy"""
        try:
            # Check if all agents are responding
            unhealthy_count = 0
            
            for agent in self.active_agents.values():
                if not agent.is_healthy():
                    unhealthy_count += 1
            
            # Consider healthy if less than 20% of agents are unhealthy
            total_agents = len(self.active_agents)
            if total_agents == 0:
                return True
            
            unhealthy_ratio = unhealthy_count / total_agents
            return unhealthy_ratio < 0.2
            
        except Exception as e:
            self.logger.error(f"Agent manager health check failed: {e}")
            return False
    
    def get_active_agent_count(self) -> int:
        """Get count of active agents"""
        return len(self.active_agents)
    
    def get_agent_types(self) -> List[str]:
        """Get list of available agent types"""
        return list(self.agent_types.keys())