"""
Wire Demo - Comprehensive demonstration of The Wire architecture

This demo shows how AI agents can be dynamically created, registered as services,
and integrated with each other through The Wire architecture.
"""

import asyncio
import json
import logging
import time
from typing import Dict, List, Any

from .the_wire import TheWire, ServiceType
from .agent_services import (
    CodeGeneratorAgent, DataAnalysisAgent, ConversationalAgent, TaskOrchestratorAgent
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WireDemo:
    """Demonstration of The Wire architecture with AI agents"""
    
    def __init__(self):
        self.wire = TheWire()
        self.agents = []
        
    async def setup_demo(self):
        """Set up the demo environment"""
        logger.info("Setting up The Wire demo...")
        
        # Start The Wire
        await self.wire.start()
        
        # Create and register AI agents
        await self.create_agents()
        
        logger.info("Demo setup complete!")
    
    async def create_agents(self):
        """Create and register various AI agents"""
        logger.info("Creating AI agents...")
        
        # Create different types of agents
        code_agent = CodeGeneratorAgent(self.wire)
        data_agent = DataAnalysisAgent(self.wire)
        chat_agent = ConversationalAgent(self.wire)
        orchestrator = TaskOrchestratorAgent(self.wire)
        
        agents = [code_agent, data_agent, chat_agent, orchestrator]
        
        # Initialize and register each agent
        for agent in agents:
            await agent.initialize()
            self.wire.register_service(agent)
            self.agents.append(agent)
            logger.info(f"Registered agent: {agent.metadata.name}")
    
    async def demo_service_discovery(self):
        """Demonstrate service discovery capabilities"""
        logger.info("\n=== Service Discovery Demo ===")
        
        # Discover all services
        all_services = self.wire.discover_services()
        logger.info(f"Total services discovered: {len(all_services)}")
        
        for service in all_services:
            logger.info(f"  - {service.name} ({service.service_type.value}) - {service.description}")
        
        # Discover AI agents specifically
        ai_agents = self.wire.discover_services(ServiceType.AI_AGENT)
        logger.info(f"\nAI Agents found: {len(ai_agents)}")
        
        # Discover by tags
        code_services = self.wire.discover_services(tags={"capability": "code-generation"})
        logger.info(f"Code generation services: {len(code_services)}")
    
    async def demo_direct_service_calls(self):
        """Demonstrate direct service calls"""
        logger.info("\n=== Direct Service Calls Demo ===")
        
        # Find a conversational agent
        chat_agents = self.wire.discover_services(ServiceType.AI_AGENT, {"capability": "conversation"})
        if chat_agents:
            agent_id = chat_agents[0].service_id
            
            # Start a conversation
            response = await self.wire.call_service(
                target_service_id=agent_id,
                method="POST",
                path="/start_conversation",
                data={"message": "Hello, I need help with a project"}
            )
            
            logger.info(f"Conversation started: {response.data}")
            
            # Continue the conversation
            if response.status_code == 200 and response.data:
                conversation_id = response.data.get("conversation_id")
                
                continue_response = await self.wire.call_service(
                    target_service_id=agent_id,
                    method="POST", 
                    path="/continue_conversation",
                    data={
                        "conversation_id": conversation_id,
                        "message": "I want to build a web application"
                    }
                )
                
                logger.info(f"Conversation continued: {continue_response.data}")
    
    async def demo_service_by_type_calls(self):
        """Demonstrate calling services by type with load balancing"""
        logger.info("\n=== Service by Type Calls Demo ===")
        
        # Call any AI agent for analysis
        response = await self.wire.call_service_by_type(
            service_type=ServiceType.AI_AGENT,
            method="POST",
            path="/analyze",
            data={"content": "This is sample data to analyze"}
        )
        
        logger.info(f"Analysis response: {response.data}")
        
        # Call code generation service specifically
        code_response = await self.wire.call_service_by_type(
            service_type=ServiceType.AI_AGENT,
            method="POST",
            path="/generate_code",
            data={
                "requirements": "Create a function that calculates fibonacci numbers",
                "language": "python"
            },
            tags={"capability": "code-generation"}
        )
        
        if code_response.status_code == 200:
            logger.info(f"Generated code:\n{code_response.data.get('code', 'No code generated')}")
    
    async def demo_orchestrated_workflow(self):
        """Demonstrate complex workflow orchestration"""
        logger.info("\n=== Orchestrated Workflow Demo ===")
        
        # Find orchestrator
        orchestrators = self.wire.discover_services(ServiceType.ORCHESTRATOR)
        if orchestrators:
            orchestrator_id = orchestrators[0].service_id
            
            # Define a complex workflow
            workflow = {
                "name": "AI-Powered Development Workflow",
                "steps": [
                    {
                        "id": "analyze_requirements",
                        "service_type": "ai_agent",
                        "action": "analyze",
                        "description": "Analyze project requirements"
                    },
                    {
                        "id": "generate_code",
                        "service_type": "ai_agent", 
                        "action": "generate_code",
                        "description": "Generate initial code structure"
                    },
                    {
                        "id": "review_code",
                        "service_type": "ai_agent",
                        "action": "review_code", 
                        "description": "Review generated code"
                    },
                    {
                        "id": "analyze_data_patterns",
                        "service_type": "ai_agent",
                        "action": "analyze_dataset",
                        "description": "Analyze data patterns"
                    }
                ]
            }
            
            # Execute workflow
            workflow_response = await self.wire.call_service(
                target_service_id=orchestrator_id,
                method="POST",
                path="/execute_workflow",
                data={"workflow": workflow}
            )
            
            logger.info(f"Workflow execution: {workflow_response.data}")
    
    async def demo_event_driven_communication(self):
        """Demonstrate event-driven communication between services"""
        logger.info("\n=== Event-Driven Communication Demo ===")
        
        # Set up event handlers
        def handle_code_generated(event):
            logger.info(f"Event received - Code generated: {event}")
        
        def handle_analysis_complete(event):
            logger.info(f"Event received - Analysis complete: {event}")
        
        # Subscribe to events
        self.wire.subscribe_to_events("code.generated", handle_code_generated)
        self.wire.subscribe_to_events("analysis.complete", handle_analysis_complete)
        
        # Publish some events
        await self.wire.publish_event("code.generated", {
            "agent_id": "code-generator-123",
            "language": "python",
            "lines_of_code": 42
        })
        
        await self.wire.publish_event("analysis.complete", {
            "agent_id": "data-analyst-456", 
            "insights_found": 5,
            "confidence": 0.87
        })
        
        # Wait for events to be processed
        await asyncio.sleep(0.5)
    
    async def demo_service_integration(self):
        """Demonstrate how services can integrate with each other"""
        logger.info("\n=== Service Integration Demo ===")
        
        # Simulate a complex task that requires multiple services
        task_description = "Build a data analysis dashboard with AI insights"
        
        # Step 1: Decompose the task using orchestrator
        orchestrators = self.wire.discover_services(ServiceType.ORCHESTRATOR)
        if orchestrators:
            decompose_response = await self.wire.call_service(
                target_service_id=orchestrators[0].service_id,
                method="POST",
                path="/decompose_task",
                data={"task": task_description}
            )
            
            logger.info(f"Task decomposition: {decompose_response.data}")
            
            if decompose_response.status_code == 200:
                subtasks = decompose_response.data.get("subtasks", [])
                
                # Step 2: Execute each subtask using appropriate services
                for subtask in subtasks[:2]:  # Execute first 2 subtasks for demo
                    logger.info(f"Executing subtask: {subtask['description']}")
                    
                    # Route to appropriate service based on subtask requirements
                    if "code" in subtask["description"].lower():
                        # Use code generation service
                        response = await self.wire.call_service_by_type(
                            service_type=ServiceType.AI_AGENT,
                            method="POST",
                            path="/generate_code",
                            data={"requirements": subtask["description"]},
                            tags={"capability": "code-generation"}
                        )
                    elif "data" in subtask["description"].lower():
                        # Use data analysis service
                        response = await self.wire.call_service_by_type(
                            service_type=ServiceType.AI_AGENT,
                            method="POST",
                            path="/analyze_dataset",
                            data={"dataset": [1, 2, 3, 4, 5]},
                            tags={"capability": "data-analysis"}
                        )
                    else:
                        # Use general analysis
                        response = await self.wire.call_service_by_type(
                            service_type=ServiceType.AI_AGENT,
                            method="POST",
                            path="/analyze",
                            data={"content": subtask["description"]}
                        )
                    
                    logger.info(f"Subtask result: {response.status_code} - {response.data}")
    
    async def demo_health_monitoring(self):
        """Demonstrate health monitoring of services"""
        logger.info("\n=== Health Monitoring Demo ===")
        
        # Check health of all services
        health_results = await self.wire.health_check_all_services()
        
        logger.info("Service health status:")
        for service_id, is_healthy in health_results.items():
            service_name = next(
                (s.name for s in self.wire.discover_services() if s.service_id == service_id),
                "Unknown"
            )
            status = "✅ Healthy" if is_healthy else "❌ Unhealthy"
            logger.info(f"  {service_name}: {status}")
    
    async def demo_performance_metrics(self):
        """Demonstrate performance monitoring"""
        logger.info("\n=== Performance Metrics Demo ===")
        
        # Execute multiple requests and measure performance
        start_time = time.time()
        
        tasks = []
        for i in range(5):
            task = self.wire.call_service_by_type(
                service_type=ServiceType.AI_AGENT,
                method="GET",
                path="/capabilities"
            )
            tasks.append(task)
        
        # Execute requests concurrently
        responses = await asyncio.gather(*tasks)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        successful_requests = sum(1 for r in responses if r.status_code == 200)
        
        logger.info(f"Performance metrics:")
        logger.info(f"  Total requests: {len(tasks)}")
        logger.info(f"  Successful requests: {successful_requests}")
        logger.info(f"  Total time: {total_time:.3f} seconds")
        logger.info(f"  Average time per request: {total_time/len(tasks):.3f} seconds")
        logger.info(f"  Requests per second: {len(tasks)/total_time:.2f}")
    
    async def run_full_demo(self):
        """Run the complete demonstration"""
        logger.info("🚀 Starting The Wire Comprehensive Demo")
        logger.info("=" * 60)
        
        try:
            # Setup
            await self.setup_demo()
            
            # Run all demo scenarios
            await self.demo_service_discovery()
            await self.demo_direct_service_calls()
            await self.demo_service_by_type_calls()
            await self.demo_orchestrated_workflow()
            await self.demo_event_driven_communication()
            await self.demo_service_integration()
            await self.demo_health_monitoring()
            await self.demo_performance_metrics()
            
            logger.info("\n🎉 Demo completed successfully!")
            
        except Exception as e:
            logger.error(f"Demo failed: {e}")
            raise
        finally:
            # Cleanup
            await self.cleanup()
    
    async def cleanup(self):
        """Clean up demo resources"""
        logger.info("\nCleaning up demo resources...")
        
        # Unregister all agents
        for agent in self.agents:
            await agent.shutdown()
            self.wire.unregister_service(agent.metadata.service_id)
        
        # Stop The Wire
        await self.wire.stop()
        
        logger.info("Cleanup complete!")

async def main():
    """Main demo function"""
    demo = WireDemo()
    await demo.run_full_demo()

if __name__ == "__main__":
    asyncio.run(main())