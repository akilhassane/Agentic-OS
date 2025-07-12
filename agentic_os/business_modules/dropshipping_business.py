import asyncio
import random
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

from agentic_os.core.logger import get_logger

class DropshippingBusiness:
    """
    Dropshipping business module that manages dropshipping operations
    """
    
    def __init__(self, business_id: int, name: str, config: dict, db_manager):
        self.business_id = business_id
        self.name = name
        self.config = config
        self.db_manager = db_manager
        
        self.logger = get_logger(f"Dropshipping.{name}")
        
        # Business state
        self.running = False
        self.last_activity = None
        
        # Performance metrics
        self.metrics = {
            "total_revenue": 0.0,
            "total_orders": 0,
            "conversion_rate": 0.0,
            "average_order_value": 0.0,
            "profit_margin": 0.0,
            "active_products": 0
        }
        
        # Configuration defaults
        self.niche = config.get("niche", "general")
        self.target_margin = config.get("target_margin", 0.3)
        self.auto_pricing = config.get("auto_pricing", True)
        self.auto_fulfillment = config.get("auto_fulfillment", True)
        
        # Sample products for demonstration
        self.sample_products = self._get_sample_products()
    
    async def start(self):
        """Start the dropshipping business"""
        try:
            self.logger.info(f"Starting dropshipping business: {self.name}")
            
            self.running = True
            self.last_activity = datetime.now()
            
            # Initialize business operations
            await self._initialize_products()
            await self._setup_store()
            
            # Start business operations loop
            asyncio.create_task(self._operations_loop())
            
            self.logger.info(f"✅ Dropshipping business {self.name} started successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to start dropshipping business: {e}")
            raise
    
    async def stop(self):
        """Stop the dropshipping business"""
        try:
            self.logger.info(f"Stopping dropshipping business: {self.name}")
            
            self.running = False
            
            self.logger.info(f"✅ Dropshipping business {self.name} stopped successfully")
            
        except Exception as e:
            self.logger.error(f"Error stopping dropshipping business: {e}")
    
    async def _initialize_products(self):
        """Initialize products for the business"""
        try:
            # Check if we already have products
            existing_products = await self.db_manager.get_products(self.business_id)
            
            if len(existing_products) == 0:
                # Add sample products based on niche
                products_to_add = self._get_niche_products()
                
                for product in products_to_add:
                    await self.db_manager.create_product(
                        business_id=self.business_id,
                        name=product["name"],
                        description=product["description"],
                        price=product["price"],
                        cost=product["cost"],
                        supplier_info=product["supplier_info"]
                    )
                
                self.logger.info(f"Added {len(products_to_add)} products to store")
            
            # Update metrics
            await self._update_product_metrics()
            
        except Exception as e:
            self.logger.error(f"Error initializing products: {e}")
    
    async def _setup_store(self):
        """Setup the online store"""
        try:
            # Simulate store setup (in reality this would integrate with Shopify, WooCommerce, etc.)
            self.logger.info("Setting up online store...")
            
            store_config = {
                "store_name": self.name,
                "domain": f"{self.name.lower().replace(' ', '-')}.com",
                "theme": "modern-minimal",
                "payment_processors": ["stripe", "paypal"],
                "shipping_providers": ["ups", "fedex", "usps"]
            }
            
            # Save store configuration
            await self.db_manager.save_metric(
                business_id=self.business_id,
                metric_name="store_setup",
                metric_value=1.0,
                metadata=store_config
            )
            
            self.logger.info("✅ Online store setup completed")
            
        except Exception as e:
            self.logger.error(f"Error setting up store: {e}")
    
    async def _operations_loop(self):
        """Main operations loop for the business"""
        while self.running:
            try:
                self.last_activity = datetime.now()
                
                # Perform business operations
                await self._process_orders()
                await self._optimize_pricing()
                await self._manage_inventory()
                await self._analyze_performance()
                
                # Update metrics
                await self.update_metrics()
                
                # Sleep before next cycle
                await asyncio.sleep(300)  # Run every 5 minutes
                
            except Exception as e:
                self.logger.error(f"Error in operations loop: {e}")
                await asyncio.sleep(60)
    
    async def _process_orders(self):
        """Process incoming orders"""
        try:
            # Simulate receiving orders (in reality this would integrate with store platform)
            if random.random() < 0.1:  # 10% chance of new order each cycle
                await self._simulate_new_order()
            
            # Process pending orders
            orders = await self.db_manager.get_orders(self.business_id)
            pending_orders = [o for o in orders if o["status"] == "pending"]
            
            for order in pending_orders:
                if self.auto_fulfillment:
                    await self._fulfill_order(order)
                
        except Exception as e:
            self.logger.error(f"Error processing orders: {e}")
    
    async def _simulate_new_order(self):
        """Simulate a new order for demonstration"""
        try:
            products = await self.db_manager.get_products(self.business_id)
            
            if products:
                # Randomly select a product
                product = random.choice(products)
                quantity = random.randint(1, 3)
                total_amount = product["price"] * quantity
                
                # Create order
                order_id = await self.db_manager.create_order(
                    business_id=self.business_id,
                    customer_email=f"customer{random.randint(1000, 9999)}@example.com",
                    product_id=product["id"],
                    quantity=quantity,
                    total_amount=total_amount
                )
                
                self.logger.info(f"New order received: #{order_id} - ${total_amount:.2f}")
                
                # Update revenue metric
                await self.db_manager.save_metric(
                    business_id=self.business_id,
                    metric_name="order_created",
                    metric_value=total_amount
                )
                
        except Exception as e:
            self.logger.error(f"Error simulating new order: {e}")
    
    async def _fulfill_order(self, order: dict):
        """Fulfill an order"""
        try:
            # Simulate order fulfillment process
            self.logger.info(f"Fulfilling order #{order['id']}")
            
            # In reality, this would:
            # 1. Contact supplier to ship product
            # 2. Update tracking information
            # 3. Send confirmation to customer
            
            # For simulation, just mark as fulfilled
            # (In a real implementation, we'd update order status in database)
            
            # Calculate profit
            products = await self.db_manager.get_products(self.business_id)
            product = next((p for p in products if p["id"] == order["product_id"]), None)
            
            if product:
                profit = (product["price"] - product["cost"]) * order["quantity"]
                
                await self.db_manager.save_metric(
                    business_id=self.business_id,
                    metric_name="profit",
                    metric_value=profit
                )
                
                self.logger.info(f"Order #{order['id']} fulfilled - Profit: ${profit:.2f}")
            
        except Exception as e:
            self.logger.error(f"Error fulfilling order: {e}")
    
    async def _optimize_pricing(self):
        """Optimize product pricing"""
        try:
            if not self.auto_pricing:
                return
            
            products = await self.db_manager.get_products(self.business_id)
            
            for product in products:
                # Simple pricing optimization (in reality this would be more sophisticated)
                current_margin = (product["price"] - product["cost"]) / product["price"]
                
                if current_margin < self.target_margin:
                    # Increase price to meet target margin
                    new_price = product["cost"] / (1 - self.target_margin)
                    
                    # Update product price (simplified - would update in database)
                    self.logger.info(f"Optimized pricing for {product['name']}: ${product['price']:.2f} -> ${new_price:.2f}")
                
        except Exception as e:
            self.logger.error(f"Error optimizing pricing: {e}")
    
    async def _manage_inventory(self):
        """Manage inventory levels"""
        try:
            # Monitor inventory levels and add new products if needed
            products = await self.db_manager.get_products(self.business_id)
            
            if len(products) < 5:  # Maintain at least 5 products
                new_products = self._get_additional_products(1)
                
                for product in new_products:
                    await self.db_manager.create_product(
                        business_id=self.business_id,
                        name=product["name"],
                        description=product["description"],
                        price=product["price"],
                        cost=product["cost"],
                        supplier_info=product["supplier_info"]
                    )
                
                self.logger.info(f"Added {len(new_products)} new products to inventory")
            
        except Exception as e:
            self.logger.error(f"Error managing inventory: {e}")
    
    async def _analyze_performance(self):
        """Analyze business performance"""
        try:
            # Calculate performance metrics
            orders = await self.db_manager.get_orders(self.business_id)
            
            if orders:
                total_revenue = sum(order["total_amount"] for order in orders)
                total_orders = len(orders)
                average_order_value = total_revenue / total_orders if total_orders > 0 else 0
                
                # Get recent metrics
                recent_profit = await self.db_manager.get_metric(self.business_id, "profit") or 0
                profit_margin = (recent_profit / total_revenue) if total_revenue > 0 else 0
                
                # Update metrics
                self.metrics.update({
                    "total_revenue": total_revenue,
                    "total_orders": total_orders,
                    "average_order_value": average_order_value,
                    "profit_margin": profit_margin
                })
                
                # Save revenue metric
                await self.db_manager.save_metric(
                    business_id=self.business_id,
                    metric_name="revenue",
                    metric_value=total_revenue
                )
            
        except Exception as e:
            self.logger.error(f"Error analyzing performance: {e}")
    
    async def _update_product_metrics(self):
        """Update product-related metrics"""
        try:
            products = await self.db_manager.get_products(self.business_id)
            self.metrics["active_products"] = len(products)
            
        except Exception as e:
            self.logger.error(f"Error updating product metrics: {e}")
    
    def _get_sample_products(self) -> List[dict]:
        """Get sample products for different niches"""
        return {
            "electronics": [
                {"name": "Wireless Bluetooth Earbuds", "cost": 15, "price": 45, "description": "High-quality wireless earbuds with noise cancellation"},
                {"name": "Phone Camera Lens Kit", "cost": 8, "price": 29, "description": "Professional camera lens attachment for smartphones"},
                {"name": "Portable Power Bank", "cost": 12, "price": 35, "description": "10000mAh portable charger with fast charging"},
            ],
            "fitness": [
                {"name": "Resistance Bands Set", "cost": 7, "price": 25, "description": "Complete set of resistance bands for home workouts"},
                {"name": "Yoga Mat Premium", "cost": 10, "price": 35, "description": "Non-slip premium yoga mat with alignment lines"},
                {"name": "Fitness Tracker Smart", "cost": 20, "price": 60, "description": "Advanced fitness tracker with heart rate monitoring"},
            ],
            "home": [
                {"name": "LED Strip Lights", "cost": 6, "price": 22, "description": "Smart RGB LED strips with app control"},
                {"name": "Bamboo Kitchen Utensils", "cost": 5, "price": 18, "description": "Eco-friendly bamboo cooking utensil set"},
                {"name": "Aromatherapy Diffuser", "cost": 12, "price": 40, "description": "Ultrasonic essential oil diffuser with timer"},
            ],
            "general": [
                {"name": "Multi-Tool Pen", "cost": 4, "price": 16, "description": "6-in-1 tactical pen with multiple tools"},
                {"name": "Travel Organizer Bag", "cost": 8, "price": 28, "description": "Waterproof travel organizer with multiple compartments"},
                {"name": "Magnetic Phone Mount", "cost": 3, "price": 12, "description": "Universal magnetic car phone mount"},
            ]
        }
    
    def _get_niche_products(self) -> List[dict]:
        """Get products for the business niche"""
        products = self.sample_products.get(self.niche, self.sample_products["general"])
        
        # Add supplier info to each product
        for product in products:
            product["supplier_info"] = {
                "supplier_name": f"Supplier_{random.randint(100, 999)}",
                "location": random.choice(["China", "USA", "Germany", "India"]),
                "shipping_time": f"{random.randint(3, 14)} days",
                "minimum_order": random.randint(1, 10)
            }
        
        return products
    
    def _get_additional_products(self, count: int) -> List[dict]:
        """Get additional products to expand inventory"""
        all_products = []
        for niche_products in self.sample_products.values():
            all_products.extend(niche_products)
        
        # Select random products
        selected = random.sample(all_products, min(count, len(all_products)))
        
        # Add supplier info
        for product in selected:
            product["supplier_info"] = {
                "supplier_name": f"Supplier_{random.randint(100, 999)}",
                "location": random.choice(["China", "USA", "Germany", "India"]),
                "shipping_time": f"{random.randint(3, 14)} days",
                "minimum_order": random.randint(1, 10)
            }
        
        return selected
    
    # Public interface methods
    async def update_metrics(self):
        """Update business metrics"""
        await self._analyze_performance()
        await self._update_product_metrics()
    
    def is_running(self) -> bool:
        """Check if business is running"""
        return self.running
    
    def get_last_activity(self) -> Optional[str]:
        """Get last activity timestamp"""
        return self.last_activity.isoformat() if self.last_activity else None
    
    def get_status(self) -> dict:
        """Get business status"""
        return {
            "business_id": self.business_id,
            "name": self.name,
            "niche": self.niche,
            "running": self.running,
            "last_activity": self.get_last_activity(),
            "metrics": self.metrics,
            "config": {
                "target_margin": self.target_margin,
                "auto_pricing": self.auto_pricing,
                "auto_fulfillment": self.auto_fulfillment
            }
        }
    
    def get_performance_metrics(self) -> dict:
        """Get performance metrics"""
        return self.metrics.copy()