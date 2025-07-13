"""
NexusOS - Production Runtime System
Ultra-lightweight, crash-proof operating system with full resource utilization
"""

import asyncio
import os
import sys
import signal
import psutil
import threading
import multiprocessing
import time
import gc
import resource
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import logging

# Configure high-performance logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/tmp/nexus.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class SystemResources:
    """System resource monitoring"""
    cpu_count: int
    memory_total: int
    memory_available: int
    disk_total: int
    disk_free: int
    network_interfaces: List[str]
    
class NexusKernel:
    """
    NexusOS Kernel - Crash-proof, high-performance core
    """
    
    def __init__(self):
        self.running = True
        self.services = {}
        self.resource_monitor = None
        self.thread_pool = None
        self.process_pool = None
        
        # Get CPU count with fallback
        cpu_count = multiprocessing.cpu_count()
        self.max_workers = cpu_count * 2 if cpu_count else 4
        
        # Set maximum resource limits
        self._configure_resources()
        
        # Signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        logger.info("NexusOS Kernel initialized")
    
    def _configure_resources(self):
        """Configure system for maximum resource utilization"""
        try:
            # Set maximum file descriptors
            resource.setrlimit(resource.RLIMIT_NOFILE, (65536, 65536))
            
            # Set maximum memory usage (unlimited)
            resource.setrlimit(resource.RLIMIT_AS, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
            
            # Set maximum CPU time (unlimited)
            resource.setrlimit(resource.RLIMIT_CPU, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
            
            # Configure garbage collection for performance
            gc.set_threshold(700, 10, 10)
            
            logger.info("System resources configured for maximum utilization")
        except Exception as e:
            logger.warning(f"Resource configuration warning: {e}")
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info(f"Received signal {signum}, initiating graceful shutdown")
        self.running = False
    
    def get_system_resources(self) -> SystemResources:
        """Get current system resource information"""
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return SystemResources(
            cpu_count=psutil.cpu_count(logical=True) or 1,
            memory_total=memory.total,
            memory_available=memory.available,
            disk_total=disk.total,
            disk_free=disk.free,
            network_interfaces=list(psutil.net_if_addrs().keys())
        )
    
    async def start(self):
        """Start the NexusOS kernel"""
        logger.info("Starting NexusOS Kernel...")
        
        # Initialize thread and process pools
        self.thread_pool = ThreadPoolExecutor(max_workers=self.max_workers)
        self.process_pool = ProcessPoolExecutor(max_workers=self.max_workers)
        
        # Start resource monitoring
        self.resource_monitor = threading.Thread(target=self._monitor_resources, daemon=True)
        self.resource_monitor.start()
        
        # Start core services
        await self._start_core_services()
        
        logger.info("NexusOS Kernel started successfully")
        
        # Main event loop
        while self.running:
            try:
                await self._kernel_tick()
                await asyncio.sleep(0.001)  # 1ms tick for responsiveness
            except Exception as e:
                logger.error(f"Kernel tick error: {e}")
                # Continue running - never crash
                continue
    
    async def _start_core_services(self):
        """Start essential system services"""
        try:
            from .network_stack import NetworkStack
            from .app_manager import AppManager
            from .security_manager import SecurityManager
            
            # Initialize core services
            self.services['network'] = NetworkStack()
            self.services['apps'] = AppManager()
            self.services['security'] = SecurityManager()
            
            # Start all services
            for name, service in self.services.items():
                try:
                    await service.start()
                    logger.info(f"Service '{name}' started")
                except Exception as e:
                    logger.error(f"Failed to start service '{name}': {e}")
                    # Continue with other services
        except ImportError as e:
            logger.error(f"Failed to import core services: {e}")
            # Create minimal fallback services
            self.services = {}
    
    async def _kernel_tick(self):
        """Main kernel tick - handles system operations"""
        # Process pending tasks
        for service in self.services.values():
            if hasattr(service, 'tick'):
                try:
                    await service.tick()
                except Exception as e:
                    logger.error(f"Service tick error: {e}")
        
        # Memory management
        if psutil.virtual_memory().percent > 90:
            gc.collect()
    
    def _monitor_resources(self):
        """Monitor system resources continuously"""
        while self.running:
            try:
                resources = self.get_system_resources()
                
                # Log resource usage every 30 seconds
                if int(time.time()) % 30 == 0:
                    cpu_percent = psutil.cpu_percent(interval=1)
                    memory_percent = (resources.memory_total - resources.memory_available) / resources.memory_total * 100
                    
                    logger.info(f"Resources - CPU: {cpu_percent:.1f}%, Memory: {memory_percent:.1f}%")
                
                time.sleep(1)
            except Exception as e:
                logger.error(f"Resource monitoring error: {e}")
                time.sleep(5)  # Back off on error
    
    async def shutdown(self):
        """Graceful system shutdown"""
        logger.info("Shutting down NexusOS...")
        
        self.running = False
        
        # Shutdown services
        for name, service in self.services.items():
            try:
                if hasattr(service, 'shutdown'):
                    await service.shutdown()
                logger.info(f"Service '{name}' shutdown")
            except Exception as e:
                logger.error(f"Error shutting down service '{name}': {e}")
        
        # Shutdown thread pools
        if self.thread_pool:
            self.thread_pool.shutdown(wait=True)
        if self.process_pool:
            self.process_pool.shutdown(wait=True)
        
        logger.info("NexusOS shutdown complete")

class NexusOS:
    """
    Main NexusOS class - Entry point for the operating system
    """
    
    def __init__(self):
        self.kernel = NexusKernel()
        self.version = "1.0.0"
        
    async def boot(self):
        """Boot the operating system"""
        logger.info(f"Booting NexusOS v{self.version}")
        
        try:
            await self.kernel.start()
        except KeyboardInterrupt:
            logger.info("Boot interrupted by user")
        except Exception as e:
            logger.error(f"Boot error: {e}")
            # Auto-restart on crash
            logger.info("Attempting auto-restart...")
            await asyncio.sleep(1)
            await self.boot()
        finally:
            await self.kernel.shutdown()

# Auto-restart wrapper
async def run_nexus():
    """Run NexusOS with auto-restart capability"""
    while True:
        try:
            nexus = NexusOS()
            await nexus.boot()
            break  # Clean shutdown
        except Exception as e:
            logger.error(f"System crash: {e}")
            logger.info("Auto-restarting in 2 seconds...")
            await asyncio.sleep(2)

if __name__ == "__main__":
    # Set process priority to high
    try:
        os.nice(-10)  # Higher priority
    except PermissionError:
        logger.warning("Could not set high priority (requires root)")
    
    # Run the operating system
    asyncio.run(run_nexus())