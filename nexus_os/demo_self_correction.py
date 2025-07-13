#!/usr/bin/env python3
"""
Self-Correction Demo

This script demonstrates the self-correction capabilities of AgenticOS,
showing how agents can automatically detect, correct, and learn from errors.
"""

import asyncio
import logging
import time
from typing import Dict, Any

from core.the_wire import TheWire
from core.self_correcting_agent_service import (
    SelfCorrectingCodeGeneratorAgent, 
    SelfCorrectingDataAnalysisAgent
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class SelfCorrectionDemo:
    """Demo class for showcasing self-correction capabilities"""
    
    def __init__(self):
        self.wire = TheWire()
        self.code_agent = None
        self.data_agent = None
        
    async def setup(self):
        """Setup the demo environment"""
        print("🚀 Setting up Self-Correction Demo...")
        
        # Start The Wire
        await self.wire.start()
        
        # Create self-correcting agents
        self.code_agent = SelfCorrectingCodeGeneratorAgent(self.wire)
        self.data_agent = SelfCorrectingDataAnalysisAgent(self.wire)
        
        # Register agents
        self.wire.register_service(self.code_agent)
        self.wire.register_service(self.data_agent)
        
        # Initialize agents
        await self.code_agent.initialize()
        await self.data_agent.initialize()
        
        print("✅ Demo setup complete!")
    
    async def demo_code_generation_errors(self):
        """Demonstrate code generation with various error scenarios"""
        print("\n🔧 Demo: Code Generation with Self-Correction")
        print("=" * 50)
        
        # Test 1: Normal code generation
        print("\n1. Normal code generation:")
        if self.code_agent and self.code_agent.metadata:
            result = await self.wire.call_service(
                self.code_agent.metadata.service_id,
                "POST", "/generate_code",
                {
                    "requirements": "Create a simple calculator function",
                    "language": "python",
                    "framework": ""
                }
            )
            print(f"✅ Success: {result.data.get('code', '')[:100]}...")
        
        # Test 2: Timeout error (should be corrected)
        print("\n2. Complex requirements (timeout error):")
        if self.code_agent and self.code_agent.metadata:
            result = await self.wire.call_service(
                self.code_agent.metadata.service_id,
                "POST", "/generate_code",
                {
                    "requirements": "Create a complex machine learning algorithm with deep neural networks",
                    "language": "python",
                    "framework": "tensorflow"
                }
            )
            print(f"🔄 Corrected: {result.data.get('status', 'unknown')}")
        
        # Test 3: Invalid requirements (should be corrected)
        print("\n3. Invalid requirements:")
        if self.code_agent and self.code_agent.metadata:
            result = await self.wire.call_service(
                self.code_agent.metadata.service_id,
                "POST", "/generate_code",
                {
                    "requirements": "invalid requirements that should fail",
                    "language": "python",
                    "framework": ""
                }
            )
            print(f"🔄 Corrected: {result.data.get('status', 'unknown')}")
        
        # Test 4: Memory error (should be corrected)
        print("\n4. Memory-intensive requirements:")
        if self.code_agent and self.code_agent.metadata:
            result = await self.wire.call_service(
                self.code_agent.metadata.service_id,
                "POST", "/generate_code",
                {
                    "requirements": "Create a massive data processing system with memory intensive operations",
                    "language": "python",
                    "framework": ""
                }
            )
            print(f"🔄 Corrected: {result.data.get('status', 'unknown')}")
    
    async def demo_data_analysis_errors(self):
        """Demonstrate data analysis with various error scenarios"""
        print("\n📊 Demo: Data Analysis with Self-Correction")
        print("=" * 50)
        
        # Test 1: Normal data analysis
        print("\n1. Normal data analysis:")
        if self.data_agent and self.data_agent.metadata:
            result = await self.wire.call_service(
                self.data_agent.metadata.service_id,
                "POST", "/analyze_data",
                {
                    "data": [1, 2, 3, 4, 5],
                    "analysis_type": "trend"
                }
            )
            print(f"✅ Success: {len(result.data.get('insights', []))} insights found")
        
        # Test 2: Large dataset (memory error)
        print("\n2. Large dataset (memory error):")
        large_dataset = list(range(15000))  # Large dataset
        if self.data_agent and self.data_agent.metadata:
            result = await self.wire.call_service(
                self.data_agent.metadata.service_id,
                "POST", "/analyze_data",
                {
                    "data": large_dataset,
                    "analysis_type": "comprehensive"
                }
            )
            print(f"🔄 Corrected: {result.data.get('status', 'unknown')}")
        
        # Test 3: Invalid data format
        print("\n3. Invalid data format:")
        if self.data_agent and self.data_agent.metadata:
            result = await self.wire.call_service(
                self.data_agent.metadata.service_id,
                "POST", "/analyze_data",
                {
                    "data": ["invalid", "data", "format"],
                    "analysis_type": "statistical"
                }
            )
            print(f"🔄 Corrected: {result.data.get('status', 'unknown')}")
        
        # Test 4: Timeout analysis
        print("\n4. Timeout analysis:")
        if self.data_agent and self.data_agent.metadata:
            result = await self.wire.call_service(
                self.data_agent.metadata.service_id,
                "POST", "/analyze_data",
                {
                    "data": [1, 2, 3, 4, 5],
                    "analysis_type": "timeout_analysis"
                }
            )
            print(f"🔄 Corrected: {result.data.get('status', 'unknown')}")
    
    async def demo_anomaly_detection(self):
        """Demonstrate anomaly detection with error correction"""
        print("\n🔍 Demo: Anomaly Detection with Self-Correction")
        print("=" * 50)
        
        # Test 1: Normal anomaly detection
        print("\n1. Normal anomaly detection:")
        if self.data_agent and self.data_agent.metadata:
            result = await self.wire.call_service(
                self.data_agent.metadata.service_id,
                "POST", "/detect_anomalies",
                {
                    "data": [1, 2, 3, 100, 4, 5],  # 100 is an anomaly
                    "threshold": 0.1
                }
            )
            print(f"✅ Success: {len(result.data.get('anomalies', []))} anomalies detected")
        
        # Test 2: Empty dataset
        print("\n2. Empty dataset:")
        if self.data_agent and self.data_agent.metadata:
            result = await self.wire.call_service(
                self.data_agent.metadata.service_id,
                "POST", "/detect_anomalies",
                {
                    "data": [],
                    "threshold": 0.1
                }
            )
            print(f"🔄 Corrected: {result.data.get('status', 'unknown')}")
        
        # Test 3: Invalid threshold
        print("\n3. Invalid threshold:")
        if self.data_agent and self.data_agent.metadata:
            result = await self.wire.call_service(
                self.data_agent.metadata.service_id,
                "POST", "/detect_anomalies",
                {
                    "data": [1, 2, 3, 4, 5],
                    "threshold": 1.5  # Invalid threshold > 1
                }
            )
            print(f"🔄 Corrected: {result.data.get('status', 'unknown')}")
    
    async def demo_health_monitoring(self):
        """Demonstrate health monitoring and metrics"""
        print("\n📈 Demo: Health Monitoring and Metrics")
        print("=" * 50)
        
        # Get code agent health
        print("\n1. Code Generator Agent Health:")
        if self.code_agent and self.code_agent.metadata:
            health = await self.wire.call_service(
                self.code_agent.metadata.service_id,
                "GET", "/health_metrics",
                {}
            )
            health_data = health.data
            print(f"   Agent: {health_data.get('agent_name')}")
            print(f"   Success Rate: {health_data.get('health_metrics', {}).get('success_rate', 0):.2%}")
            print(f"   Correction Rate: {health_data.get('health_metrics', {}).get('correction_rate', 0):.2%}")
            print(f"   Capabilities: {len(health_data.get('capabilities', []))}")
        
        # Get data agent health
        print("\n2. Data Analysis Agent Health:")
        if self.data_agent and self.data_agent.metadata:
            health = await self.wire.call_service(
                self.data_agent.metadata.service_id,
                "GET", "/health_metrics",
                {}
            )
            health_data = health.data
            print(f"   Agent: {health_data.get('agent_name')}")
            print(f"   Success Rate: {health_data.get('health_metrics', {}).get('success_rate', 0):.2%}")
            print(f"   Correction Rate: {health_data.get('health_metrics', {}).get('correction_rate', 0):.2%}")
            print(f"   Capabilities: {len(health_data.get('capabilities', []))}")
        
        # Get capabilities
        print("\n3. Agent Capabilities:")
        if self.code_agent and self.code_agent.metadata:
            capabilities = await self.wire.call_service(
                self.code_agent.metadata.service_id,
                "GET", "/capabilities",
                {}
            )
            caps_data = capabilities.data
            print(f"   Code Agent: {caps_data.get('total_capabilities')} capabilities")
            for cap in caps_data.get('capabilities', []):
                print(f"     - {cap.get('name')}: {cap.get('description')}")
    
    async def demo_learning_from_errors(self):
        """Demonstrate learning from specific errors"""
        print("\n🧠 Demo: Learning from Errors")
        print("=" * 50)
        
        # Learn from a specific error pattern
        print("\n1. Learning from timeout error:")
        if self.code_agent and self.code_agent.metadata:
            learning_result = await self.wire.call_service(
                self.code_agent.metadata.service_id,
                "POST", "/learn_from_error",
                {
                    "error_type": "TimeoutError",
                    "error_message": "Code generation timeout for complex requirements",
                    "task_id": "generate_code_complex",
                    "context": {
                        "requirements": "complex machine learning algorithm",
                        "language": "python",
                        "framework": "tensorflow"
                    }
                }
            )
            print(f"✅ Learning: {learning_result.data.get('message')}")
        
        # Learn from another error pattern
        print("\n2. Learning from memory error:")
        if self.code_agent and self.code_agent.metadata:
            learning_result = await self.wire.call_service(
                self.code_agent.metadata.service_id,
                "POST", "/learn_from_error",
                {
                    "error_type": "MemoryError",
                    "error_message": "Insufficient memory for code generation",
                    "task_id": "generate_code_memory",
                    "context": {
                        "requirements": "massive data processing system",
                        "language": "python",
                        "framework": ""
                    }
                }
            )
            print(f"✅ Learning: {learning_result.data.get('message')}")
    
    async def run_comprehensive_demo(self):
        """Run the complete self-correction demo"""
        print("🤖 AgenticOS Self-Correction Demo")
        print("=" * 60)
        print("This demo showcases how agents can automatically:")
        print("  • Detect errors and failures")
        print("  • Apply appropriate correction strategies")
        print("  • Learn from errors to improve future performance")
        print("  • Monitor health and performance metrics")
        print("=" * 60)
        
        try:
            # Setup
            await self.setup()
            
            # Run demos
            await self.demo_code_generation_errors()
            await self.demo_data_analysis_errors()
            await self.demo_anomaly_detection()
            await self.demo_health_monitoring()
            await self.demo_learning_from_errors()
            
            print("\n🎉 Demo completed successfully!")
            print("\nKey Features Demonstrated:")
            print("  ✅ Automatic error detection and classification")
            print("  ✅ Intelligent correction strategy selection")
            print("  ✅ Retry mechanisms with exponential backoff")
            print("  ✅ Fallback strategies for different error types")
            print("  ✅ Adaptive learning from error patterns")
            print("  ✅ Real-time health monitoring and metrics")
            print("  ✅ Continuous improvement through learning")
            
        except Exception as e:
            print(f"❌ Demo error: {e}")
            logging.error(f"Demo error: {e}")
        
        finally:
            # Cleanup
            await self.cleanup()
    
    async def cleanup(self):
        """Cleanup demo resources"""
        print("\n🧹 Cleaning up demo resources...")
        
        if self.code_agent:
            await self.code_agent.shutdown()
        
        if self.data_agent:
            await self.data_agent.shutdown()
        
        await self.wire.stop()
        print("✅ Cleanup complete!")

async def main():
    """Main demo function"""
    demo = SelfCorrectionDemo()
    await demo.run_comprehensive_demo()

if __name__ == "__main__":
    asyncio.run(main())