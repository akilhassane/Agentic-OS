"""
Self-Correcting Agent Service

This module provides agent services with built-in self-correction capabilities,
integrating with The Wire architecture for robust and adaptive task execution.
"""

import asyncio
import json
import uuid
import time
import logging
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field

from .the_wire import (
    WireService, ServiceMetadata, ServiceType, ServiceEndpoint, 
    ServiceRequest, ServiceResponse, TheWire
)
from .self_correction import (
    SelfCorrectionEngine, SelfCorrectingAgent, ErrorSeverity, 
    CorrectionStrategy, TaskState
)

@dataclass
class AgentCapability:
    """Agent capability definition"""
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    error_handling: Dict[str, Any] = field(default_factory=dict)
    learning_enabled: bool = True

class SelfCorrectingAgentService(WireService):
    """Base class for self-correcting agent services"""
    
    def __init__(self, metadata: ServiceMetadata, wire: TheWire):
        super().__init__(metadata, wire)
        
        # Initialize self-correction engine
        self.correction_engine = SelfCorrectionEngine()
        self.agent = SelfCorrectingAgent(metadata.service_id, self.correction_engine)
        
        # Agent capabilities
        self.capabilities: List[AgentCapability] = []
        self.learning_enabled = True
        self.adaptation_enabled = True
        
        # Add self-correction endpoints
        self.add_endpoint(ServiceEndpoint(
            method="POST",
            path="/execute_with_correction",
            handler=self.execute_with_correction,
            description="Execute a task with self-correction capabilities"
        ))
        
        self.add_endpoint(ServiceEndpoint(
            method="GET",
            path="/health_metrics",
            handler=self.get_health_metrics,
            description="Get agent health and correction metrics"
        ))
        
        self.add_endpoint(ServiceEndpoint(
            method="POST",
            path="/learn_from_error",
            handler=self.learn_from_error,
            description="Learn from a specific error pattern"
        ))
        
        self.add_endpoint(ServiceEndpoint(
            method="GET",
            path="/capabilities",
            handler=self.get_capabilities,
            description="Get agent capabilities"
        ))
    
    async def initialize(self) -> bool:
        """Initialize the self-correcting agent"""
        logging.info(f"Initializing self-correcting agent: {self.metadata.name}")
        
        # Initialize capabilities
        await self._initialize_capabilities()
        
        # Start background learning process
        asyncio.create_task(self._background_learning())
        
        return True
    
    async def shutdown(self) -> bool:
        """Shutdown the self-correcting agent"""
        logging.info(f"Shutting down self-correcting agent: {self.metadata.name}")
        self.agent.stop()
        return True
    
    async def health_check(self) -> bool:
        """Check if the agent is healthy"""
        health_metrics = self.correction_engine.get_system_health()
        success_rate = health_metrics.get("success_rate", 0.0)
        
        # Agent is healthy if success rate is above 80%
        return success_rate >= 0.8
    
    async def execute_with_correction(self, request: ServiceRequest) -> Dict[str, Any]:
        """Execute a task with self-correction capabilities"""
        data = request.data if request.data else {}
        
        task_name = data.get("task_name", "unknown_task")
        task_func_name = data.get("task_func", "default_task")
        task_args = data.get("args", [])
        task_kwargs = data.get("kwargs", {})
        
        # Get the task function
        task_func = getattr(self, task_func_name, None)
        if not task_func:
            return {
                "error": f"Task function '{task_func_name}' not found",
                "agent_id": self.metadata.service_id,
                "status": "error"
            }
        
        try:
            # Execute with self-correction
            result = await self.agent.execute_task(
                task_name, task_func, *task_args, **task_kwargs
            )
            
            return {
                "result": result,
                "agent_id": self.metadata.service_id,
                "task_name": task_name,
                "status": "success",
                "correction_applied": False  # Will be updated by correction engine
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "agent_id": self.metadata.service_id,
                "task_name": task_name,
                "status": "failed"
            }
    
    async def get_health_metrics(self, request: ServiceRequest) -> Dict[str, Any]:
        """Get agent health and correction metrics"""
        health_metrics = self.correction_engine.get_system_health()
        
        return {
            "agent_id": self.metadata.service_id,
            "agent_name": self.metadata.name,
            "health_metrics": health_metrics,
            "capabilities": [cap.name for cap in self.capabilities],
            "learning_enabled": self.learning_enabled,
            "adaptation_enabled": self.adaptation_enabled,
            "timestamp": time.time()
        }
    
    async def learn_from_error(self, request: ServiceRequest) -> Dict[str, Any]:
        """Learn from a specific error pattern"""
        data = request.data if request.data else {}
        
        error_type = data.get("error_type")
        error_message = data.get("error_message")
        task_id = data.get("task_id")
        context = data.get("context", {})
        
        if not all([error_type, error_message, task_id]):
            return {
                "error": "Missing required fields: error_type, error_message, task_id",
                "status": "error"
            }
        
        # Record the error for learning
        learning_data = {
            "error_type": error_type,
            "error_message": error_message,
            "task_id": task_id,
            "agent_id": self.metadata.service_id,
            "context": context,
            "timestamp": time.time()
        }
        
        # Store in learning models
        if task_id and task_id not in self.correction_engine.learning_models:
            self.correction_engine.learning_models[task_id] = []
        
        if task_id:
            self.correction_engine.learning_models[task_id].append(learning_data)
        
        return {
            "status": "success",
            "message": f"Learned from error: {error_type}",
            "learning_data": learning_data,
            "total_learning_entries": len(self.correction_engine.learning_models[task_id])
        }
    
    async def get_capabilities(self, request: ServiceRequest) -> Dict[str, Any]:
        """Get agent capabilities"""
        return {
            "agent_id": self.metadata.service_id,
            "agent_name": self.metadata.name,
            "capabilities": [
                {
                    "name": cap.name,
                    "description": cap.description,
                    "input_schema": cap.input_schema,
                    "output_schema": cap.output_schema,
                    "learning_enabled": cap.learning_enabled
                }
                for cap in self.capabilities
            ],
            "total_capabilities": len(self.capabilities)
        }
    
    async def _initialize_capabilities(self):
        """Initialize agent capabilities - to be overridden by subclasses"""
        pass
    
    async def _background_learning(self):
        """Background learning process"""
        while True:
            try:
                # Analyze recent errors and patterns
                health_metrics = self.correction_engine.get_system_health()
                common_patterns = health_metrics.get("common_error_patterns", [])
                
                # Apply learning improvements
                for pattern in common_patterns:
                    if pattern.get("count", 0) > 5:  # Only learn from frequent patterns
                        await self._apply_pattern_learning(pattern)
                
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                logging.error(f"Background learning error: {e}")
                await asyncio.sleep(30)
    
    async def _apply_pattern_learning(self, pattern: Dict[str, Any]):
        """Apply learning from error patterns"""
        error_key = pattern.get("error_key", "")
        error_type = error_key.split(":")[0] if ":" in error_key else error_key
        
        # Apply specific learning based on error type
        if "timeout" in error_type.lower():
            await self._learn_timeout_handling(pattern)
        elif "connection" in error_type.lower():
            await self._learn_connection_handling(pattern)
        elif "value" in error_type.lower():
            await self._learn_value_validation(pattern)
    
    async def _learn_timeout_handling(self, pattern: Dict[str, Any]):
        """Learn better timeout handling"""
        logging.info(f"Learning timeout handling from pattern: {pattern}")
        # In a real implementation, this would update timeout strategies
    
    async def _learn_connection_handling(self, pattern: Dict[str, Any]):
        """Learn better connection handling"""
        logging.info(f"Learning connection handling from pattern: {pattern}")
        # In a real implementation, this would update connection strategies
    
    async def _learn_value_validation(self, pattern: Dict[str, Any]):
        """Learn better value validation"""
        logging.info(f"Learning value validation from pattern: {pattern}")
        # In a real implementation, this would update validation strategies

class SelfCorrectingCodeGeneratorAgent(SelfCorrectingAgentService):
    """Self-correcting code generation agent"""
    
    def __init__(self, wire: TheWire):
        metadata = ServiceMetadata(
            service_id=f"self-correcting-codegen-{uuid.uuid4().hex[:8]}",
            name="Self-Correcting Code Generator Agent",
            service_type=ServiceType.AI_AGENT,
            version="1.0.0",
            description="AI agent specialized in generating code with self-correction",
            tags={"capability": "code-generation", "self-correcting": "true"}
        )
        super().__init__(metadata, wire)
        
        # Add code-specific endpoints
        self.add_endpoint(ServiceEndpoint(
            method="POST",
            path="/generate_code",
            handler=self.generate_code,
            description="Generate code with self-correction"
        ))
        
        self.add_endpoint(ServiceEndpoint(
            method="POST",
            path="/review_code",
            handler=self.review_code,
            description="Review code with self-correction"
        ))
        
        self.add_endpoint(ServiceEndpoint(
            method="POST",
            path="/refactor_code",
            handler=self.refactor_code,
            description="Refactor code with self-correction"
        ))
    
    async def _initialize_capabilities(self):
        """Initialize code generation capabilities"""
        self.capabilities = [
            AgentCapability(
                name="code_generation",
                description="Generate code from requirements",
                input_schema={
                    "type": "object",
                    "properties": {
                        "requirements": {"type": "string"},
                        "language": {"type": "string"},
                        "framework": {"type": "string"}
                    }
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "code": {"type": "string"},
                        "language": {"type": "string"},
                        "confidence": {"type": "number"}
                    }
                },
                error_handling={
                    "syntax_error": "retry_with_different_approach",
                    "timeout": "increase_timeout",
                    "memory_error": "reduce_complexity"
                }
            ),
            AgentCapability(
                name="code_review",
                description="Review and suggest improvements for code",
                input_schema={
                    "type": "object",
                    "properties": {
                        "code": {"type": "string"},
                        "language": {"type": "string"}
                    }
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "issues": {"type": "array"},
                        "score": {"type": "number"},
                        "suggestions": {"type": "array"}
                    }
                }
            )
        ]
    
    async def generate_code(self, request: ServiceRequest) -> Dict[str, Any]:
        """Generate code with self-correction"""
        data = request.data if request.data else {}
        requirements = data.get("requirements", "")
        language = data.get("language", "python")
        framework = data.get("framework", "")
        
        # Execute with self-correction
        result = await self.agent.execute_task(
            "generate_code", self._generate_code_impl,
            requirements, language, framework
        )
        
        return {
            "code": result.get("code", ""),
            "language": language,
            "confidence": result.get("confidence", 0.0),
            "agent_id": self.metadata.service_id,
            "correction_applied": result.get("correction_applied", False)
        }
    
    async def _generate_code_impl(self, requirements: str, language: str, framework: str) -> Dict[str, Any]:
        """Implementation of code generation with potential errors"""
        # Simulate code generation with potential errors
        await asyncio.sleep(0.2)
        
        # Simulate different types of errors
        if "complex" in requirements.lower():
            raise TimeoutError("Code generation timeout for complex requirements")
        
        if "invalid" in requirements.lower():
            raise ValueError("Invalid requirements provided")
        
        if "memory" in requirements.lower():
            raise MemoryError("Insufficient memory for code generation")
        
        # Successful generation
        generated_code = f"""
# Generated by {self.metadata.name}
# Requirements: {requirements}
# Language: {language}
# Framework: {framework}

def generated_function():
    '''Generated function based on requirements'''
    # Implementation would be here
    pass
"""
        
        return {
            "code": generated_code,
            "language": language,
            "confidence": 0.85
        }
    
    async def review_code(self, request: ServiceRequest) -> Dict[str, Any]:
        """Review code with self-correction"""
        data = request.data if request.data else {}
        code = data.get("code", "")
        language = data.get("language", "python")
        
        # Execute with self-correction
        result = await self.agent.execute_task(
            "review_code", self._review_code_impl,
            code, language
        )
        
        return {
            "issues": result.get("issues", []),
            "score": result.get("score", 0.0),
            "suggestions": result.get("suggestions", []),
            "agent_id": self.metadata.service_id,
            "correction_applied": result.get("correction_applied", False)
        }
    
    async def _review_code_impl(self, code: str, language: str) -> Dict[str, Any]:
        """Implementation of code review with potential errors"""
        await asyncio.sleep(0.1)
        
        # Simulate errors
        if "syntax_error" in code.lower():
            raise SyntaxError("Invalid syntax in code")
        
        if "timeout" in code.lower():
            raise TimeoutError("Code review timeout")
        
        # Successful review
        return {
            "issues": [
                {"type": "style", "message": "Consider using more descriptive variable names"},
                {"type": "performance", "message": "This loop could be optimized"}
            ],
            "score": 8.5,
            "suggestions": ["Add error handling", "Include unit tests"]
        }
    
    async def refactor_code(self, request: ServiceRequest) -> Dict[str, Any]:
        """Refactor code with self-correction"""
        data = request.data if request.data else {}
        code = data.get("code", "")
        language = data.get("language", "python")
        
        # Execute with self-correction
        result = await self.agent.execute_task(
            "refactor_code", self._refactor_code_impl,
            code, language
        )
        
        return {
            "refactored_code": result.get("refactored_code", ""),
            "improvements": result.get("improvements", []),
            "agent_id": self.metadata.service_id,
            "correction_applied": result.get("correction_applied", False)
        }
    
    async def _refactor_code_impl(self, code: str, language: str) -> Dict[str, Any]:
        """Implementation of code refactoring with potential errors"""
        await asyncio.sleep(0.3)
        
        # Simulate errors
        if "complex" in code.lower():
            raise TimeoutError("Refactoring timeout for complex code")
        
        # Successful refactoring
        refactored_code = f"""
# Refactored by {self.metadata.name}
# Original code length: {len(code)}
# Language: {language}

{code}

# Refactoring improvements applied
"""
        
        return {
            "refactored_code": refactored_code,
            "improvements": ["Improved readability", "Reduced complexity"]
        }

class SelfCorrectingDataAnalysisAgent(SelfCorrectingAgentService):
    """Self-correcting data analysis agent"""
    
    def __init__(self, wire: TheWire):
        metadata = ServiceMetadata(
            service_id=f"self-correcting-data-{uuid.uuid4().hex[:8]}",
            name="Self-Correcting Data Analysis Agent",
            service_type=ServiceType.AI_AGENT,
            version="1.0.0",
            description="AI agent specialized in data analysis with self-correction",
            tags={"capability": "data-analysis", "self-correcting": "true"}
        )
        super().__init__(metadata, wire)
        
        # Add data analysis endpoints
        self.add_endpoint(ServiceEndpoint(
            method="POST",
            path="/analyze_data",
            handler=self.analyze_data,
            description="Analyze data with self-correction"
        ))
        
        self.add_endpoint(ServiceEndpoint(
            method="POST",
            path="/detect_anomalies",
            handler=self.detect_anomalies,
            description="Detect anomalies with self-correction"
        ))
    
    async def _initialize_capabilities(self):
        """Initialize data analysis capabilities"""
        self.capabilities = [
            AgentCapability(
                name="data_analysis",
                description="Analyze datasets and extract insights",
                input_schema={
                    "type": "object",
                    "properties": {
                        "data": {"type": "array"},
                        "analysis_type": {"type": "string"}
                    }
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "insights": {"type": "array"},
                        "confidence": {"type": "number"},
                        "visualizations": {"type": "array"}
                    }
                },
                error_handling={
                    "data_error": "validate_and_clean",
                    "memory_error": "reduce_dataset_size",
                    "timeout": "increase_timeout"
                }
            )
        ]
    
    async def analyze_data(self, request: ServiceRequest) -> Dict[str, Any]:
        """Analyze data with self-correction"""
        data = request.data if request.data else {}
        dataset = data.get("data", [])
        analysis_type = data.get("analysis_type", "general")
        
        # Execute with self-correction
        result = await self.agent.execute_task(
            "analyze_data", self._analyze_data_impl,
            dataset, analysis_type
        )
        
        return {
            "insights": result.get("insights", []),
            "confidence": result.get("confidence", 0.0),
            "visualizations": result.get("visualizations", []),
            "agent_id": self.metadata.service_id,
            "correction_applied": result.get("correction_applied", False)
        }
    
    async def _analyze_data_impl(self, dataset: List[Any], analysis_type: str) -> Dict[str, Any]:
        """Implementation of data analysis with potential errors"""
        await asyncio.sleep(0.2)
        
        # Simulate errors
        if len(dataset) > 10000:
            raise MemoryError("Dataset too large for analysis")
        
        if "invalid" in str(dataset).lower():
            raise ValueError("Invalid data format")
        
        if "timeout" in analysis_type.lower():
            raise TimeoutError("Analysis timeout")
        
        # Successful analysis
        return {
            "insights": [
                "Data shows positive trend",
                "Correlation coefficient: 0.75",
                "Outliers detected: 3"
            ],
            "confidence": 0.88,
            "visualizations": ["trend_chart", "correlation_matrix"]
        }
    
    async def detect_anomalies(self, request: ServiceRequest) -> Dict[str, Any]:
        """Detect anomalies with self-correction"""
        data = request.data if request.data else {}
        dataset = data.get("data", [])
        threshold = data.get("threshold", 0.05)
        
        # Execute with self-correction
        result = await self.agent.execute_task(
            "detect_anomalies", self._detect_anomalies_impl,
            dataset, threshold
        )
        
        return {
            "anomalies": result.get("anomalies", []),
            "anomaly_score": result.get("anomaly_score", 0.0),
            "confidence": result.get("confidence", 0.0),
            "agent_id": self.metadata.service_id,
            "correction_applied": result.get("correction_applied", False)
        }
    
    async def _detect_anomalies_impl(self, dataset: List[Any], threshold: float) -> Dict[str, Any]:
        """Implementation of anomaly detection with potential errors"""
        await asyncio.sleep(0.15)
        
        # Simulate errors
        if len(dataset) == 0:
            raise ValueError("Empty dataset provided")
        
        if threshold < 0 or threshold > 1:
            raise ValueError("Invalid threshold value")
        
        # Successful detection
        return {
            "anomalies": [{"index": 5, "value": 150, "score": 0.95}],
            "anomaly_score": 0.92,
            "confidence": 0.85
        }