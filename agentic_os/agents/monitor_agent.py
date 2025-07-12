import asyncio
import random
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

from agentic_os.agents.base_agent import BaseAgent

class MonitorAgent(BaseAgent):
    """
    Monitor agent that tracks system and business performance
    """
    
    @property
    def agent_type(self) -> str:
        return "monitor"
    
    async def _initialize(self):
        """Initialize monitor-specific components"""
        try:
            self.logger.info("Initializing Monitor Agent...")
            
            # Initialize monitoring components
            self.alert_threshold_cpu = self.config.get("alert_threshold_cpu", 80)
            self.alert_threshold_memory = self.config.get("alert_threshold_memory", 85)
            self.alert_threshold_disk = self.config.get("alert_threshold_disk", 90)
            
            # Performance tracking
            self.monitoring_metrics = {
                "alerts_generated": 0,
                "anomalies_detected": 0,
                "reports_created": 0,
                "optimizations_suggested": 0
            }
            
            # Alert history
            self.recent_alerts = []
            
            self.logger.info("✅ Monitor Agent initialized")
            
        except Exception as e:
            self.logger.error(f"Error initializing monitor agent: {e}")
            raise
    
    async def _cleanup(self):
        """Cleanup monitor-specific resources"""
        try:
            self.logger.info("Cleaning up Monitor Agent resources...")
            # Cleanup monitoring connections, etc.
        except Exception as e:
            self.logger.error(f"Error cleaning up monitor agent: {e}")
    
    async def _execute_cycle(self):
        """Execute one cycle of monitoring work"""
        try:
            # System monitoring
            await self._monitor_system_health()
            
            # Business monitoring
            await self._monitor_business_performance()
            
            # Anomaly detection
            await self._detect_anomalies()
            
            # Generate reports
            await self._generate_reports()
            
            # Clean up old alerts
            await self._cleanup_old_alerts()
            
        except Exception as e:
            self.logger.error(f"Error in monitor agent cycle: {e}")
    
    async def _execute_task(self, task: dict):
        """Execute a specific monitoring task"""
        try:
            task_type = task.get("type")
            
            if task_type == "system_check":
                await self._perform_system_check()
            elif task_type == "business_analysis":
                await self._analyze_business_performance(task.get("business_id"))
            elif task_type == "generate_report":
                await self._generate_custom_report(task.get("report_config", {}))
            elif task_type == "alert_check":
                await self._check_alerts(task.get("alert_config", {}))
            else:
                self.logger.warning(f"Unknown task type: {task_type}")
            
        except Exception as e:
            self.logger.error(f"Error executing monitor task: {e}")
    
    async def _monitor_system_health(self):
        """Monitor overall system health"""
        try:
            # Simulate checking system metrics
            if random.random() < 0.3:  # 30% chance each cycle
                await self._simulate_system_check()
                
        except Exception as e:
            self.logger.error(f"Error monitoring system health: {e}")
    
    async def _simulate_system_check(self):
        """Simulate system health check"""
        try:
            # Simulate system metrics
            cpu_usage = random.uniform(20, 95)
            memory_usage = random.uniform(30, 90)
            disk_usage = random.uniform(10, 85)
            
            # Check for alerts
            alerts = []
            
            if cpu_usage > self.alert_threshold_cpu:
                alerts.append({
                    "type": "high_cpu_usage",
                    "value": cpu_usage,
                    "threshold": self.alert_threshold_cpu,
                    "severity": "warning" if cpu_usage < 90 else "critical"
                })
            
            if memory_usage > self.alert_threshold_memory:
                alerts.append({
                    "type": "high_memory_usage",
                    "value": memory_usage,
                    "threshold": self.alert_threshold_memory,
                    "severity": "warning" if memory_usage < 95 else "critical"
                })
            
            if disk_usage > self.alert_threshold_disk:
                alerts.append({
                    "type": "high_disk_usage",
                    "value": disk_usage,
                    "threshold": self.alert_threshold_disk,
                    "severity": "critical"
                })
            
            # Process alerts
            for alert in alerts:
                await self._process_alert(alert)
            
            # Save monitoring metrics
            await self.save_metric(
                "system_health_score",
                100 - max(cpu_usage, memory_usage, disk_usage),
                metadata={
                    "cpu_usage": cpu_usage,
                    "memory_usage": memory_usage,
                    "disk_usage": disk_usage,
                    "alerts_count": len(alerts)
                }
            )
            
            if alerts:
                self.logger.warning(f"⚠️ System health check found {len(alerts)} alerts")
            else:
                self.logger.debug("✅ System health check passed")
            
        except Exception as e:
            self.logger.error(f"Error in system check simulation: {e}")
    
    async def _monitor_business_performance(self):
        """Monitor business performance metrics"""
        try:
            # Simulate business performance monitoring
            if random.random() < 0.4:  # 40% chance each cycle
                await self._simulate_business_monitoring()
                
        except Exception as e:
            self.logger.error(f"Error monitoring business performance: {e}")
    
    async def _simulate_business_monitoring(self):
        """Simulate business performance monitoring"""
        try:
            if not self.business_id:
                return
            
            # Simulate business metrics analysis
            revenue_trend = random.choice(["increasing", "stable", "decreasing"])
            conversion_rate = random.uniform(0.01, 0.10)
            customer_satisfaction = random.uniform(3.0, 5.0)
            order_fulfillment_rate = random.uniform(0.85, 0.99)
            
            # Generate performance insights
            insights = []
            
            if revenue_trend == "decreasing":
                insights.append("Revenue showing downward trend - investigate pricing and marketing")
            
            if conversion_rate < 0.03:
                insights.append("Low conversion rate detected - optimize product pages and checkout")
            
            if customer_satisfaction < 4.0:
                insights.append("Customer satisfaction below target - review support quality")
            
            if order_fulfillment_rate < 0.90:
                insights.append("Order fulfillment issues detected - check supplier performance")
            
            # Save business monitoring results
            await self.save_metric(
                "business_performance_score",
                (conversion_rate * 10 + customer_satisfaction * 20 + order_fulfillment_rate * 100) / 3,
                metadata={
                    "revenue_trend": revenue_trend,
                    "conversion_rate": conversion_rate,
                    "customer_satisfaction": customer_satisfaction,
                    "order_fulfillment_rate": order_fulfillment_rate,
                    "insights": insights
                }
            )
            
            if insights:
                self.logger.info(f"📊 Business analysis found {len(insights)} insights")
            
        except Exception as e:
            self.logger.error(f"Error in business monitoring simulation: {e}")
    
    async def _detect_anomalies(self):
        """Detect anomalies in system and business metrics"""
        try:
            # Simulate anomaly detection
            if random.random() < 0.15:  # 15% chance each cycle
                await self._simulate_anomaly_detection()
                self.monitoring_metrics["anomalies_detected"] += 1
                
        except Exception as e:
            self.logger.error(f"Error in anomaly detection: {e}")
    
    async def _simulate_anomaly_detection(self):
        """Simulate anomaly detection"""
        try:
            anomaly_types = [
                "unusual_traffic_spike",
                "unexpected_error_rate",
                "abnormal_response_time",
                "suspicious_order_pattern",
                "payment_failure_spike"
            ]
            
            anomaly_type = random.choice(anomaly_types)
            severity = random.choice(["low", "medium", "high"])
            confidence = random.uniform(0.6, 0.95)
            
            anomaly_data = {
                "type": anomaly_type,
                "severity": severity,
                "confidence": confidence,
                "detected_at": datetime.now().isoformat(),
                "business_id": self.business_id
            }
            
            # Save anomaly detection
            await self.save_metric(
                "anomaly_detection",
                confidence,
                metadata=anomaly_data
            )
            
            self.logger.warning(f"🔍 Anomaly detected: {anomaly_type} (Severity: {severity})")
            
        except Exception as e:
            self.logger.error(f"Error simulating anomaly detection: {e}")
    
    async def _generate_reports(self):
        """Generate performance reports"""
        try:
            # Simulate report generation
            if random.random() < 0.05:  # 5% chance each cycle
                await self._simulate_report_generation()
                self.monitoring_metrics["reports_created"] += 1
                
        except Exception as e:
            self.logger.error(f"Error generating reports: {e}")
    
    async def _simulate_report_generation(self):
        """Simulate report generation"""
        try:
            report_types = [
                "daily_performance",
                "weekly_summary",
                "business_health",
                "system_utilization",
                "cost_analysis"
            ]
            
            report_type = random.choice(report_types)
            data_points = random.randint(50, 200)
            insights_count = random.randint(3, 10)
            
            report_data = {
                "report_type": report_type,
                "data_points_analyzed": data_points,
                "insights_generated": insights_count,
                "generated_at": datetime.now().isoformat(),
                "business_id": self.business_id
            }
            
            # Save report generation metric
            await self.save_metric(
                "report_generation",
                insights_count,
                metadata=report_data
            )
            
            self.logger.info(f"📈 Generated {report_type} report with {insights_count} insights")
            
        except Exception as e:
            self.logger.error(f"Error simulating report generation: {e}")
    
    async def _process_alert(self, alert: dict):
        """Process and store an alert"""
        try:
            alert["timestamp"] = datetime.now().isoformat()
            alert["business_id"] = self.business_id
            
            # Add to recent alerts
            self.recent_alerts.append(alert)
            
            # Save alert metric
            await self.save_metric(
                f"alert_{alert['type']}",
                alert["value"],
                metadata=alert
            )
            
            self.monitoring_metrics["alerts_generated"] += 1
            
            self.logger.warning(f"🚨 Alert: {alert['type']} = {alert['value']:.1f} (threshold: {alert['threshold']})")
            
        except Exception as e:
            self.logger.error(f"Error processing alert: {e}")
    
    async def _cleanup_old_alerts(self):
        """Remove old alerts from memory"""
        try:
            # Keep only alerts from the last hour
            cutoff_time = datetime.now() - timedelta(hours=1)
            
            self.recent_alerts = [
                alert for alert in self.recent_alerts
                if datetime.fromisoformat(alert["timestamp"]) > cutoff_time
            ]
            
        except Exception as e:
            self.logger.error(f"Error cleaning up old alerts: {e}")
    
    # Task-specific methods
    async def _perform_system_check(self):
        """Perform a comprehensive system check"""
        try:
            self.logger.info("Performing comprehensive system check...")
            await self._simulate_system_check()
            
        except Exception as e:
            self.logger.error(f"Error performing system check: {e}")
    
    async def _analyze_business_performance(self, business_id: Optional[int] = None):
        """Analyze performance for a specific business"""
        try:
            target_business_id = business_id or self.business_id
            self.logger.info(f"Analyzing performance for business {target_business_id}")
            await self._simulate_business_monitoring()
            
        except Exception as e:
            self.logger.error(f"Error analyzing business performance: {e}")
    
    async def _generate_custom_report(self, report_config: dict):
        """Generate a custom report"""
        try:
            self.logger.info(f"Generating custom report: {report_config.get('type', 'unknown')}")
            await self._simulate_report_generation()
            
        except Exception as e:
            self.logger.error(f"Error generating custom report: {e}")
    
    async def _check_alerts(self, alert_config: dict):
        """Check for specific alert conditions"""
        try:
            self.logger.info("Checking alert conditions...")
            await self._simulate_system_check()
            
        except Exception as e:
            self.logger.error(f"Error checking alerts: {e}")
    
    def get_statistics(self) -> dict:
        """Get agent-specific statistics"""
        stats = super().get_statistics()
        stats.update({
            "monitoring_metrics": self.monitoring_metrics,
            "recent_alerts_count": len(self.recent_alerts),
            "alert_thresholds": {
                "cpu": self.alert_threshold_cpu,
                "memory": self.alert_threshold_memory,
                "disk": self.alert_threshold_disk
            }
        })
        return stats