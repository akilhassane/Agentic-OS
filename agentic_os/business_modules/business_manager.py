import asyncio
import json
from typing import Dict, List, Optional, Any
from datetime import datetime

from agentic_os.core.logger import get_logger
from agentic_os.business_modules.dropshipping_business import DropshippingBusiness

class BusinessManager:
    """
    Manages all business operations in the Agentic OS
    """
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.logger = get_logger("BusinessManager")
        
        # Active businesses registry
        self.active_businesses: Dict[int, Any] = {}
        
        # Business type registry
        self.business_types = {
            "dropshipping": DropshippingBusiness,
        }
        
        self.running = False
    
    async def start(self):
        """Start the business manager"""
        try:
            self.logger.info("Starting Business Manager...")
            
            # Load existing businesses from database
            await self._load_existing_businesses()
            
            # Start monitoring loop
            self.running = True
            asyncio.create_task(self._monitoring_loop())
            
            self.logger.info("✅ Business Manager started successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to start Business Manager: {e}")
            raise
    
    async def stop(self):
        """Stop the business manager and all businesses"""
        try:
            self.logger.info("Stopping Business Manager...")
            
            self.running = False
            
            # Stop all active businesses
            for business_id, business in self.active_businesses.items():
                await business.stop()
            
            self.active_businesses.clear()
            
            self.logger.info("✅ Business Manager stopped successfully")
            
        except Exception as e:
            self.logger.error(f"Error stopping Business Manager: {e}")
    
    async def _load_existing_businesses(self):
        """Load existing businesses from database and start them"""
        try:
            businesses = await self.db_manager.get_all_businesses()
            
            for business_data in businesses:
                if business_data["status"] == "active":
                    await self._start_business(business_data)
                    
        except Exception as e:
            self.logger.error(f"Error loading existing businesses: {e}")
    
    async def _monitoring_loop(self):
        """Monitor all active businesses"""
        while self.running:
            try:
                # Check business health and performance
                for business_id, business in list(self.active_businesses.items()):
                    if business.is_running():
                        # Update business metrics
                        await business.update_metrics()
                
                # Sleep before next check
                await asyncio.sleep(300)  # Check every 5 minutes
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(30)
    
    async def create_business(self, business_config: dict) -> dict:
        """Create a new business"""
        try:
            business_type = business_config["type"]
            
            if business_type not in self.business_types:
                raise ValueError(f"Unknown business type: {business_type}")
            
            # Create business record in database
            business_id = await self.db_manager.create_business(
                name=business_config["name"],
                business_type=business_type,
                config=business_config.get("config", {})
            )
            
            # Get the created business data
            business_data = await self.db_manager.get_business(business_id)
            
            # Start the business
            await self._start_business(business_data)
            
            self.logger.info(f"Created and started business: {business_config['name']} (ID: {business_id})")
            
            return {
                "id": business_id,
                "name": business_config["name"],
                "type": business_type,
                "status": "active",
                "config": business_config.get("config", {}),
                "created_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error creating business: {e}")
            raise
    
    async def _start_business(self, business_data: dict):
        """Start a business instance"""
        try:
            business_class = self.business_types[business_data["type"]]
            
            # Create business instance
            business = business_class(
                business_id=business_data["id"],
                name=business_data["name"],
                config=business_data["config"],
                db_manager=self.db_manager
            )
            
            # Start the business
            await business.start()
            
            # Add to active businesses
            self.active_businesses[business_data["id"]] = business
            
            self.logger.info(f"Started business: {business_data['name']} (ID: {business_data['id']})")
            
        except Exception as e:
            self.logger.error(f"Error starting business {business_data['id']}: {e}")
            await self.db_manager.update_business_status(business_data["id"], "error")
    
    async def get_business_status(self, business_id: int) -> Optional[dict]:
        """Get status of a specific business"""
        try:
            # Get business data from database
            business_data = await self.db_manager.get_business(business_id)
            
            if not business_data:
                return None
            
            # Get runtime status if business is active
            if business_id in self.active_businesses:
                business = self.active_businesses[business_id]
                runtime_status = business.get_status()
                
                # Merge database data with runtime status
                status = {
                    **business_data,
                    "runtime_status": runtime_status,
                    "is_running": business.is_running(),
                    "last_activity": business.get_last_activity()
                }
            else:
                status = {
                    **business_data,
                    "runtime_status": None,
                    "is_running": False,
                    "last_activity": None
                }
            
            return status
            
        except Exception as e:
            self.logger.error(f"Error getting business status: {e}")
            return None
    
    async def get_all_businesses(self) -> List[dict]:
        """Get all businesses"""
        try:
            businesses = await self.db_manager.get_all_businesses()
            
            # Enhance with runtime information
            enhanced_businesses = []
            for business_data in businesses:
                business_id = business_data["id"]
                
                if business_id in self.active_businesses:
                    business = self.active_businesses[business_id]
                    enhanced_data = {
                        **business_data,
                        "is_running": business.is_running(),
                        "last_activity": business.get_last_activity(),
                        "performance": business.get_performance_metrics()
                    }
                else:
                    enhanced_data = {
                        **business_data,
                        "is_running": False,
                        "last_activity": None,
                        "performance": {}
                    }
                
                enhanced_businesses.append(enhanced_data)
            
            return enhanced_businesses
            
        except Exception as e:
            self.logger.error(f"Error getting all businesses: {e}")
            return []
    
    async def stop_business(self, business_id: int):
        """Stop a specific business"""
        try:
            if business_id in self.active_businesses:
                await self.active_businesses[business_id].stop()
                del self.active_businesses[business_id]
                
                # Update status in database
                await self.db_manager.update_business_status(business_id, "stopped")
                
                self.logger.info(f"Stopped business: {business_id}")
            
        except Exception as e:
            self.logger.error(f"Error stopping business {business_id}: {e}")
    
    async def restart_business(self, business_id: int):
        """Restart a business"""
        try:
            # Stop the current business if running
            if business_id in self.active_businesses:
                await self.active_businesses[business_id].stop()
                del self.active_businesses[business_id]
            
            # Get business data from database
            business_data = await self.db_manager.get_business(business_id)
            
            if business_data and business_data["status"] != "deleted":
                await self._start_business(business_data)
                await self.db_manager.update_business_status(business_id, "active")
            
        except Exception as e:
            self.logger.error(f"Error restarting business {business_id}: {e}")
    
    async def health_check(self) -> bool:
        """Check if business manager is healthy"""
        try:
            # Check if businesses are responding
            error_count = 0
            
            for business in self.active_businesses.values():
                if not business.is_running():
                    error_count += 1
            
            # Consider healthy if less than 30% of businesses have errors
            total_businesses = len(self.active_businesses)
            if total_businesses == 0:
                return True
            
            error_ratio = error_count / total_businesses
            return error_ratio < 0.3
            
        except Exception as e:
            self.logger.error(f"Business manager health check failed: {e}")
            return False
    
    def get_active_business_count(self) -> int:
        """Get count of active businesses"""
        return len(self.active_businesses)
    
    def get_business_types(self) -> List[str]:
        """Get list of available business types"""
        return list(self.business_types.keys())