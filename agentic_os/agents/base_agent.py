import asyncio
import json
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime

from agentic_os.core.logger import get_logger

class BaseAgent(ABC):
    """
    Base class for all agents in the Agentic OS
    """
    
    def __init__(self, agent_id: int, name: str, business_id: Optional[int], config: dict, db_manager):
        self.agent_id = agent_id
        self.name = name
        self.business_id = business_id
        self.config = config
        self.db_manager = db_manager
        
        self.logger = get_logger(f"Agent.{name}")
        
        # Agent state
        self.running = False
        self.healthy = True
        self.last_activity = None
        self.statistics = {
            "tasks_completed": 0,
            "errors": 0,
            "start_time": None
        }
        
        # Task queue
        self.task_queue = asyncio.Queue()
        self.current_task = None
    
    @property
    @abstractmethod
    def agent_type(self) -> str:
        """Return the agent type"""
        pass
    
    async def start(self):
        """Start the agent"""
        try:
            self.logger.info(f"Starting agent: {self.name}")
            
            self.running = True
            self.healthy = True
            self.statistics["start_time"] = datetime.now()
            
            # Initialize agent-specific components
            await self._initialize()
            
            # Start main loop
            asyncio.create_task(self._main_loop())
            
            self.logger.info(f"✅ Agent {self.name} started successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to start agent {self.name}: {e}")
            self.healthy = False
            raise
    
    async def stop(self):
        """Stop the agent"""
        try:
            self.logger.info(f"Stopping agent: {self.name}")
            
            self.running = False
            
            # Cleanup agent-specific resources
            await self._cleanup()
            
            self.logger.info(f"✅ Agent {self.name} stopped successfully")
            
        except Exception as e:
            self.logger.error(f"Error stopping agent {self.name}: {e}")
    
    async def _main_loop(self):
        """Main execution loop for the agent"""
        while self.running:
            try:
                # Update last activity
                self.last_activity = datetime.now()
                
                # Process tasks from queue
                await self._process_tasks()
                
                # Perform agent-specific work
                await self._execute_cycle()
                
                # Sleep based on agent configuration
                sleep_interval = self.config.get("cycle_interval", 30)
                await asyncio.sleep(sleep_interval)
                
            except Exception as e:
                self.logger.error(f"Error in main loop: {e}")
                self.statistics["errors"] += 1
                
                # Mark as unhealthy if too many errors
                if self.statistics["errors"] > 10:
                    self.healthy = False
                
                await asyncio.sleep(5)  # Brief pause before continuing
    
    async def _process_tasks(self):
        """Process tasks from the task queue"""
        while not self.task_queue.empty():
            try:
                task = await self.task_queue.get()
                self.current_task = task
                
                await self._execute_task(task)
                
                self.statistics["tasks_completed"] += 1
                self.current_task = None
                
            except Exception as e:
                self.logger.error(f"Error processing task: {e}")
                self.statistics["errors"] += 1
    
    async def add_task(self, task: dict):
        """Add a task to the agent's queue"""
        await self.task_queue.put(task)
        self.logger.info(f"Task added to queue: {task.get('type', 'unknown')}")
    
    # Abstract methods that subclasses must implement
    @abstractmethod
    async def _initialize(self):
        """Initialize agent-specific components"""
        pass
    
    @abstractmethod
    async def _cleanup(self):
        """Cleanup agent-specific resources"""
        pass
    
    @abstractmethod
    async def _execute_cycle(self):
        """Execute one cycle of agent work"""
        pass
    
    @abstractmethod
    async def _execute_task(self, task: dict):
        """Execute a specific task"""
        pass
    
    # Status and health methods
    def is_running(self) -> bool:
        """Check if agent is running"""
        return self.running
    
    def is_healthy(self) -> bool:
        """Check if agent is healthy"""
        return self.healthy and self.running
    
    def get_last_activity(self) -> Optional[str]:
        """Get last activity timestamp"""
        return self.last_activity.isoformat() if self.last_activity else None
    
    def get_statistics(self) -> dict:
        """Get agent statistics"""
        stats = self.statistics.copy()
        if stats["start_time"]:
            stats["uptime"] = str(datetime.now() - stats["start_time"])
        return stats
    
    def get_status(self) -> dict:
        """Get complete agent status"""
        return {
            "id": self.agent_id,
            "name": self.name,
            "type": self.agent_type,
            "business_id": self.business_id,
            "running": self.running,
            "healthy": self.healthy,
            "last_activity": self.get_last_activity(),
            "current_task": self.current_task,
            "queue_size": self.task_queue.qsize(),
            "statistics": self.get_statistics()
        }
    
    # Utility methods for logging and metrics
    async def log_info(self, message: str, business_id: Optional[int] = None):
        """Log an info message"""
        self.logger.info(message)
        # Could also save to database logs table here
    
    async def log_error(self, message: str, error: Exception = None):
        """Log an error message"""
        self.logger.error(f"{message}: {error}" if error else message)
        self.statistics["errors"] += 1
    
    async def save_metric(self, metric_name: str, value: float, metadata: dict = None):
        """Save a metric for this agent's business"""
        if self.business_id:
            await self.db_manager.save_metric(
                business_id=self.business_id,
                metric_name=metric_name,
                metric_value=value,
                metadata=metadata
            )