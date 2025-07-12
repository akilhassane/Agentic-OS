import asyncio
import psutil
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

from agentic_os.core.logger import get_logger

class SystemMonitor:
    """
    System monitor for tracking all system metrics and performance
    """
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.logger = get_logger("SystemMonitor")
        
        self.running = False
        self.last_activity = None
        
        # Metrics collection intervals
        self.system_metrics_interval = 60  # 1 minute
        self.business_metrics_interval = 300  # 5 minutes
        
        # Cached metrics
        self.cached_metrics = {}
    
    async def start(self):
        """Start the system monitor"""
        try:
            self.logger.info("Starting System Monitor...")
            
            self.running = True
            self.last_activity = datetime.now()
            
            # Start monitoring loops
            asyncio.create_task(self._system_metrics_loop())
            asyncio.create_task(self._business_metrics_loop())
            asyncio.create_task(self._cleanup_loop())
            
            self.logger.info("✅ System Monitor started successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to start System Monitor: {e}")
            raise
    
    async def stop(self):
        """Stop the system monitor"""
        try:
            self.logger.info("Stopping System Monitor...")
            
            self.running = False
            
            self.logger.info("✅ System Monitor stopped successfully")
            
        except Exception as e:
            self.logger.error(f"Error stopping System Monitor: {e}")
    
    async def _system_metrics_loop(self):
        """Monitor system-level metrics"""
        while self.running:
            try:
                self.last_activity = datetime.now()
                
                # Collect system metrics
                await self._collect_system_metrics()
                
                # Sleep until next collection
                await asyncio.sleep(self.system_metrics_interval)
                
            except Exception as e:
                self.logger.error(f"Error in system metrics loop: {e}")
                await asyncio.sleep(30)
    
    async def _business_metrics_loop(self):
        """Monitor business-level metrics"""
        while self.running:
            try:
                # Collect business metrics
                await self._collect_business_metrics()
                
                # Sleep until next collection
                await asyncio.sleep(self.business_metrics_interval)
                
            except Exception as e:
                self.logger.error(f"Error in business metrics loop: {e}")
                await asyncio.sleep(60)
    
    async def _cleanup_loop(self):
        """Cleanup old metrics periodically"""
        while self.running:
            try:
                # Run cleanup every hour
                await asyncio.sleep(3600)
                
                # Clean up metrics older than 30 days
                await self._cleanup_old_metrics()
                
            except Exception as e:
                self.logger.error(f"Error in cleanup loop: {e}")
    
    async def _collect_system_metrics(self):
        """Collect system-level performance metrics"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            await self.db_manager.save_metric(
                business_id=0,  # System-level metric
                metric_name="cpu_usage",
                metric_value=cpu_percent
            )
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            await self.db_manager.save_metric(
                business_id=0,
                metric_name="memory_usage",
                metric_value=memory_percent
            )
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            await self.db_manager.save_metric(
                business_id=0,
                metric_name="disk_usage",
                metric_value=disk_percent
            )
            
            # Network I/O
            network = psutil.net_io_counters()
            await self.db_manager.save_metric(
                business_id=0,
                metric_name="network_bytes_sent",
                metric_value=network.bytes_sent
            )
            await self.db_manager.save_metric(
                business_id=0,
                metric_name="network_bytes_recv",
                metric_value=network.bytes_recv
            )
            
            # Cache metrics for quick access
            self.cached_metrics.update({
                "cpu_usage": cpu_percent,
                "memory_usage": memory_percent,
                "disk_usage": disk_percent,
                "network_sent": network.bytes_sent,
                "network_recv": network.bytes_recv,
                "last_update": datetime.now().isoformat()
            })
            
            self.logger.debug(f"System metrics collected - CPU: {cpu_percent}%, Memory: {memory_percent}%")
            
        except Exception as e:
            self.logger.error(f"Error collecting system metrics: {e}")
    
    async def _collect_business_metrics(self):
        """Collect business-level metrics"""
        try:
            # Get all businesses
            businesses = await self.db_manager.get_all_businesses()
            
            for business in businesses:
                business_id = business["id"]
                
                # Collect orders count
                orders = await self.db_manager.get_orders(business_id)
                orders_count = len(orders)
                
                await self.db_manager.save_metric(
                    business_id=business_id,
                    metric_name="orders_count",
                    metric_value=orders_count
                )
                
                # Calculate daily revenue
                today = datetime.now().date()
                daily_orders = [o for o in orders if datetime.fromisoformat(o["created_at"]).date() == today]
                daily_revenue = sum(order["total_amount"] for order in daily_orders)
                
                await self.db_manager.save_metric(
                    business_id=business_id,
                    metric_name="daily_revenue",
                    metric_value=daily_revenue
                )
                
                # Collect products count
                products = await self.db_manager.get_products(business_id)
                products_count = len(products)
                
                await self.db_manager.save_metric(
                    business_id=business_id,
                    metric_name="products_count",
                    metric_value=products_count
                )
            
            self.logger.debug(f"Business metrics collected for {len(businesses)} businesses")
            
        except Exception as e:
            self.logger.error(f"Error collecting business metrics: {e}")
    
    async def _cleanup_old_metrics(self):
        """Clean up old metrics to save space"""
        try:
            # This is a simplified cleanup - in a real implementation,
            # you'd use proper SQL to delete old records
            self.logger.info("Cleaning up old metrics...")
            
            # For now, just log the cleanup action
            # In a real implementation, you'd:
            # 1. Delete metrics older than retention period
            # 2. Aggregate old metrics into summary data
            # 3. Archive important historical data
            
        except Exception as e:
            self.logger.error(f"Error cleaning up old metrics: {e}")
    
    # Public interface methods
    async def get_system_metrics(self) -> dict:
        """Get current system metrics"""
        try:
            # Return cached metrics for quick access
            if self.cached_metrics and "last_update" in self.cached_metrics:
                last_update = datetime.fromisoformat(self.cached_metrics["last_update"])
                if datetime.now() - last_update < timedelta(minutes=2):
                    return self.cached_metrics
            
            # If cached metrics are stale, collect fresh ones
            await self._collect_system_metrics()
            return self.cached_metrics
            
        except Exception as e:
            self.logger.error(f"Error getting system metrics: {e}")
            return {}
    
    async def get_business_metric(self, business_id: int, metric_name: str) -> Optional[float]:
        """Get the latest value for a business metric"""
        try:
            return await self.db_manager.get_metric(business_id, metric_name)
        except Exception as e:
            self.logger.error(f"Error getting business metric: {e}")
            return None
    
    async def get_business_metrics_history(self, business_id: int, metric_name: str, hours: int = 24) -> List[dict]:
        """Get business metrics history"""
        try:
            return await self.db_manager.get_metrics_history(business_id, metric_name, limit=hours*60//5)  # Assuming 5-minute intervals
        except Exception as e:
            self.logger.error(f"Error getting business metrics history: {e}")
            return []
    
    async def get_dashboard_data(self) -> dict:
        """Get data for the main dashboard"""
        try:
            # System metrics
            system_metrics = await self.get_system_metrics()
            
            # Business summary
            businesses = await self.db_manager.get_all_businesses()
            total_businesses = len(businesses)
            active_businesses = len([b for b in businesses if b["status"] == "active"])
            
            # Revenue summary
            total_revenue = 0.0
            total_orders = 0
            
            for business in businesses:
                business_id = business["id"]
                revenue = await self.get_business_metric(business_id, "revenue")
                orders_count = await self.get_business_metric(business_id, "orders_count")
                
                if revenue:
                    total_revenue += revenue
                if orders_count:
                    total_orders += orders_count
            
            # Daily revenue
            daily_revenue = 0.0
            for business in businesses:
                business_id = business["id"]
                daily = await self.get_business_metric(business_id, "daily_revenue")
                if daily:
                    daily_revenue += daily
            
            return {
                "system": system_metrics,
                "business_summary": {
                    "total_businesses": total_businesses,
                    "active_businesses": active_businesses,
                    "total_revenue": total_revenue,
                    "total_orders": total_orders,
                    "daily_revenue": daily_revenue
                },
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting dashboard data: {e}")
            return {"error": str(e)}
    
    async def health_check(self) -> bool:
        """Check if monitor is healthy"""
        try:
            # Check if we can collect metrics
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            
            # Check if metrics are being saved
            await self.db_manager.save_metric(
                business_id=0,
                metric_name="health_check",
                metric_value=1.0
            )
            
            return True
            
        except Exception as e:
            self.logger.error(f"Monitor health check failed: {e}")
            return False
    
    def get_last_activity(self) -> Optional[str]:
        """Get last activity timestamp"""
        return self.last_activity.isoformat() if self.last_activity else None