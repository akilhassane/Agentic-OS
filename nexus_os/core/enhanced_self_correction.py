"""
Enhanced Self-Correction Engine
Advanced error detection, prediction, and correction with ML-powered learning
"""

import asyncio
import json
import uuid
import time
import logging
import traceback
from typing import Dict, List, Any, Optional, Callable, Union, TypeVar
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
import threading
from concurrent.futures import ThreadPoolExecutor
import statistics
from collections import defaultdict, deque
import hashlib
import pickle

# Type definitions
T = TypeVar('T')

class ErrorSeverity(Enum):
    """Enhanced error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    PREDICTIVE = "predictive"  # Predicted before occurrence

class CorrectionStrategy(Enum):
    """Enhanced correction strategies"""
    RETRY = "retry"
    FALLBACK = "fallback"
    ADAPT = "adapt"
    LEARN = "learn"
    ESCALATE = "escalate"
    ROLLBACK = "rollback"
    PREDICTIVE = "predictive"  # Prevent error before it occurs
    COLLABORATIVE = "collaborative"  # Multiple services collaborate

class TaskState(Enum):
    """Enhanced task execution states"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CORRECTING = "correcting"
    RECOVERED = "recovered"
    PREDICTING = "predicting"  # Predicting potential issues
    COLLABORATING = "collaborating"  # Collaborating with other services

@dataclass
class PredictiveContext:
    """Context for predictive error detection"""
    service_id: str
    task_pattern: str
    resource_usage: Dict[str, float]
    performance_metrics: Dict[str, float]
    historical_errors: List[str]
    confidence_score: float
    prediction_time: float

@dataclass
class ErrorContext:
    """Enhanced error context with predictive capabilities"""
    error_id: str
    task_id: str
    agent_id: str
    error_type: str
    error_message: str
    severity: ErrorSeverity
    timestamp: float
    stack_trace: str
    context_data: Dict[str, Any] = field(default_factory=dict)
    recovery_attempts: int = 0
    max_recovery_attempts: int = 3
    predictive_context: Optional[PredictiveContext] = None
    cross_service_correlation: List[str] = field(default_factory=list)
    learning_priority: int = 1

@dataclass
class CorrectionAction:
    """Enhanced correction action with learning"""
    action_id: str
    strategy: CorrectionStrategy
    description: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    success: Optional[bool] = None
    execution_time: float = 0.0
    learning_outcome: Dict[str, Any] = field(default_factory=dict)
    collaboration_services: List[str] = field(default_factory=list)

@dataclass
class TaskMetrics:
    """Enhanced task metrics with predictive analytics"""
    task_id: str
    agent_id: str
    total_executions: int = 0
    successful_executions: int = 0
    failed_executions: int = 0
    correction_attempts: int = 0
    successful_corrections: int = 0
    predictive_corrections: int = 0
    average_execution_time: float = 0.0
    average_correction_time: float = 0.0
    last_execution_time: float = 0.0
    error_patterns: Dict[str, int] = field(default_factory=dict)
    learning_improvements: List[Dict[str, Any]] = field(default_factory=list)
    prediction_accuracy: float = 0.0
    collaboration_success_rate: float = 0.0

class PredictiveErrorDetector:
    """ML-powered predictive error detection"""
    
    def __init__(self):
        self.error_patterns: Dict[str, Dict[str, Any]] = {}
        self.prediction_models: Dict[str, Any] = {}
        self.historical_data: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.confidence_threshold = 0.7
        self._lock = threading.RLock()
    
    def add_error_pattern(self, error_context: ErrorContext):
        """Add error pattern for learning"""
        pattern_key = self._generate_pattern_key(error_context)
        
        with self._lock:
            if pattern_key not in self.error_patterns:
                self.error_patterns[pattern_key] = {
                    "count": 0,
                    "first_seen": error_context.timestamp,
                    "last_seen": error_context.timestamp,
                    "contexts": [],
                    "recovery_success_rate": 0.0,
                    "prediction_accuracy": 0.0
                }
            
            pattern = self.error_patterns[pattern_key]
            pattern["count"] += 1
            pattern["last_seen"] = error_context.timestamp
            pattern["contexts"].append({
                "task_id": error_context.task_id,
                "agent_id": error_context.agent_id,
                "recovery_attempts": error_context.recovery_attempts,
                "context_data": error_context.context_data
            })
    
    def predict_errors(self, service_id: str, task_pattern: str, 
                      resource_usage: Dict[str, float]) -> List[PredictiveContext]:
        """Predict potential errors based on patterns"""
        predictions = []
        
        with self._lock:
            for pattern_key, pattern in self.error_patterns.items():
                if pattern["count"] < 3:  # Need minimum data for prediction
                    continue
                
                # Calculate prediction confidence
                confidence = self._calculate_prediction_confidence(
                    pattern, service_id, task_pattern, resource_usage
                )
                
                if confidence > self.confidence_threshold:
                    predictions.append(PredictiveContext(
                        service_id=service_id,
                        task_pattern=task_pattern,
                        resource_usage=resource_usage,
                        performance_metrics=self._get_performance_metrics(service_id),
                        historical_errors=[pattern_key],
                        confidence_score=confidence,
                        prediction_time=time.time()
                    ))
        
        return predictions
    
    def _generate_pattern_key(self, error_context: ErrorContext) -> str:
        """Generate unique pattern key for error"""
        pattern_data = {
            "error_type": error_context.error_type,
            "severity": error_context.severity.value,
            "context_hash": hashlib.md5(
                json.dumps(error_context.context_data, sort_keys=True).encode()
            ).hexdigest()[:8]
        }
        return hashlib.md5(json.dumps(pattern_data, sort_keys=True).encode()).hexdigest()
    
    def _calculate_prediction_confidence(self, pattern: Dict[str, Any], 
                                       service_id: str, task_pattern: str,
                                       resource_usage: Dict[str, float]) -> float:
        """Calculate confidence score for error prediction"""
        # Simplified confidence calculation
        # In production, use ML models for accurate prediction
        
        base_confidence = min(pattern["count"] / 10.0, 1.0)  # More occurrences = higher confidence
        
        # Factor in recent occurrences
        recent_count = sum(1 for ctx in pattern["contexts"] 
                         if time.time() - ctx.get("timestamp", 0) < 3600)  # Last hour
        recent_factor = min(recent_count / 5.0, 1.0)
        
        # Factor in resource usage patterns
        resource_factor = 0.5  # Simplified - in production analyze resource patterns
        
        # Combine factors
        confidence = (base_confidence * 0.4 + recent_factor * 0.4 + resource_factor * 0.2)
        
        return min(confidence, 1.0)
    
    def _get_performance_metrics(self, service_id: str) -> Dict[str, float]:
        """Get performance metrics for service"""
        # Simplified - in production get real metrics
        return {
            "cpu_usage": 0.5,
            "memory_usage": 0.6,
            "response_time": 0.1,
            "error_rate": 0.02
        }

class CrossServiceErrorCorrelator:
    """Correlate errors across multiple services"""
    
    def __init__(self):
        self.service_dependencies: Dict[str, List[str]] = {}
        self.error_correlations: Dict[str, List[str]] = defaultdict(list)
        self.correlation_patterns: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.RLock()
    
    def add_service_dependency(self, service_id: str, dependencies: List[str]):
        """Add service dependencies for correlation analysis"""
        with self._lock:
            self.service_dependencies[service_id] = dependencies
    
    def correlate_error(self, error_context: ErrorContext) -> List[str]:
        """Find correlated errors across services"""
        correlated_errors = []
        
        with self._lock:
            # Check direct dependencies
            dependencies = self.service_dependencies.get(error_context.agent_id, [])
            for dep in dependencies:
                if self._has_recent_error(dep):
                    correlated_errors.append(dep)
            
            # Check correlation patterns
            pattern_key = f"{error_context.error_type}:{error_context.severity.value}"
            if pattern_key in self.correlation_patterns:
                pattern = self.correlation_patterns[pattern_key]
                for service_id in pattern.get("affected_services", []):
                    if service_id != error_context.agent_id:
                        correlated_errors.append(service_id)
        
        return correlated_errors
    
    def _has_recent_error(self, service_id: str) -> bool:
        """Check if service has recent errors"""
        # Simplified - in production check actual error logs
        return False
    
    def update_correlation_pattern(self, error_type: str, severity: str, 
                                 affected_services: List[str]):
        """Update correlation pattern"""
        pattern_key = f"{error_type}:{severity}"
        with self._lock:
            self.correlation_patterns[pattern_key] = {
                "affected_services": affected_services,
                "last_updated": time.time()
            }

class AdvancedLearningEngine:
    """Advanced learning engine with multiple algorithms"""
    
    def __init__(self):
        self.learning_models: Dict[str, Any] = {}
        self.training_data: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.model_performance: Dict[str, Dict[str, float]] = {}
        self._lock = threading.RLock()
    
    def learn_from_error(self, error_context: ErrorContext, 
                        correction_action: CorrectionAction):
        """Learn from error and correction action"""
        learning_data = {
            "error_type": error_context.error_type,
            "error_message": error_context.error_message,
            "severity": error_context.severity.value,
            "correction_strategy": correction_action.strategy.value,
            "success": correction_action.success,
            "execution_time": correction_action.execution_time,
            "context_data": error_context.context_data,
            "timestamp": error_context.timestamp
        }
        
        with self._lock:
            model_key = f"{error_context.agent_id}_{error_context.error_type}"
            self.training_data[model_key].append(learning_data)
            
            # Update model if enough data
            if len(self.training_data[model_key]) >= 10:
                self._update_model(model_key)
    
    def get_optimal_strategy(self, error_context: ErrorContext) -> CorrectionStrategy:
        """Get optimal correction strategy based on learning"""
        model_key = f"{error_context.agent_id}_{error_context.error_type}"
        
        with self._lock:
            if model_key in self.learning_models:
                # Use learned model to select strategy
                return self._predict_strategy(model_key, error_context)
            else:
                # Fall back to default strategy selection
                return self._default_strategy_selection(error_context)
    
    def _update_model(self, model_key: str):
        """Update learning model with new data"""
        data = self.training_data[model_key]
        
        # Calculate success rates for each strategy
        strategy_success = defaultdict(lambda: {"success": 0, "total": 0})
        
        for entry in data:
            strategy = entry["correction_strategy"]
            strategy_success[strategy]["total"] += 1
            if entry["success"]:
                strategy_success[strategy]["success"] += 1
        
        # Find best performing strategy
        best_strategy = None
        best_rate = 0.0
        
        for strategy, stats in strategy_success.items():
            if stats["total"] >= 3:  # Minimum samples
                success_rate = stats["success"] / stats["total"]
                if success_rate > best_rate:
                    best_rate = success_rate
                    best_strategy = strategy
        
        # Store model
        self.learning_models[model_key] = {
            "best_strategy": best_strategy,
            "success_rate": best_rate,
            "last_updated": time.time()
        }
        
        # Update performance metrics
        self.model_performance[model_key] = {
            "accuracy": best_rate,
            "last_updated": time.time()
        }
    
    def _predict_strategy(self, model_key: str, error_context: ErrorContext) -> CorrectionStrategy:
        """Predict optimal strategy using learned model"""
        model = self.learning_models.get(model_key)
        if not model:
            return self._default_strategy_selection(error_context)
        
        best_strategy = model.get("best_strategy")
        if best_strategy:
            try:
                return CorrectionStrategy(best_strategy)
            except ValueError:
                pass
        
        return self._default_strategy_selection(error_context)
    
    def _default_strategy_selection(self, error_context: ErrorContext) -> CorrectionStrategy:
        """Default strategy selection logic"""
        severity = error_context.severity
        
        if severity == ErrorSeverity.LOW:
            return CorrectionStrategy.RETRY
        elif severity == ErrorSeverity.MEDIUM:
            return CorrectionStrategy.ADAPT
        elif severity == ErrorSeverity.HIGH:
            return CorrectionStrategy.FALLBACK
        elif severity == ErrorSeverity.CRITICAL:
            return CorrectionStrategy.ESCALATE
        elif severity == ErrorSeverity.PREDICTIVE:
            return CorrectionStrategy.PREDICTIVE
        else:
            return CorrectionStrategy.RETRY

class EnhancedSelfCorrectionEngine:
    """Enhanced self-correction engine with predictive capabilities"""
    
    def __init__(self):
        self.error_patterns = PredictiveErrorDetector()
        self.cross_service_correlator = CrossServiceErrorCorrelator()
        self.learning_engine = AdvancedLearningEngine()
        self.task_metrics: Dict[str, TaskMetrics] = {}
        self.correction_strategies: Dict[CorrectionStrategy, Callable] = {}
        self.learning_models: Dict[str, Any] = {}
        self.recovery_history: List[CorrectionAction] = []
        self.predictive_corrections: List[PredictiveContext] = []
        self._lock = threading.RLock()
        
        # Initialize enhanced correction strategies
        self._initialize_strategies()
    
    def _initialize_strategies(self):
        """Initialize enhanced correction strategies"""
        self.correction_strategies[CorrectionStrategy.RETRY] = self._retry_strategy
        self.correction_strategies[CorrectionStrategy.FALLBACK] = self._fallback_strategy
        self.correction_strategies[CorrectionStrategy.ADAPT] = self._adapt_strategy
        self.correction_strategies[CorrectionStrategy.LEARN] = self._learn_strategy
        self.correction_strategies[CorrectionStrategy.ESCALATE] = self._escalate_strategy
        self.correction_strategies[CorrectionStrategy.ROLLBACK] = self._rollback_strategy
        self.correction_strategies[CorrectionStrategy.PREDICTIVE] = self._predictive_strategy
        self.correction_strategies[CorrectionStrategy.COLLABORATIVE] = self._collaborative_strategy
    
    async def execute_with_correction(self, task_id: str, agent_id: str, 
                                    task_func: Callable, *args, **kwargs) -> Any:
        """Execute task with enhanced self-correction"""
        start_time = time.time()
        
        # Initialize task metrics
        if task_id not in self.task_metrics:
            self.task_metrics[task_id] = TaskMetrics(task_id=task_id, agent_id=agent_id)
        
        metrics = self.task_metrics[task_id]
        metrics.total_executions += 1
        
        # Check for predictive errors
        predictions = self.error_patterns.predict_errors(
            agent_id, task_id, self._get_resource_usage()
        )
        
        if predictions:
            # Apply predictive corrections
            for prediction in predictions:
                await self._apply_predictive_correction(prediction, task_func, *args, **kwargs)
                metrics.predictive_corrections += 1
        
        try:
            # Execute the task
            result = await task_func(*args, **kwargs)
            
            # Record success
            metrics.successful_executions += 1
            metrics.last_execution_time = time.time() - start_time
            metrics.average_execution_time = self._update_average(
                metrics.average_execution_time, 
                metrics.last_execution_time, 
                metrics.successful_executions
            )
            
            return result
            
        except Exception as e:
            # Record failure
            metrics.failed_executions += 1
            metrics.last_execution_time = time.time() - start_time
            
            # Create enhanced error context
            error_context = ErrorContext(
                error_id=str(uuid.uuid4()),
                task_id=task_id,
                agent_id=agent_id,
                error_type=type(e).__name__,
                error_message=str(e),
                severity=self._determine_severity(e),
                timestamp=time.time(),
                stack_trace=traceback.format_exc(),
                context_data=self._get_error_context(e, *args, **kwargs)
            )
            
            # Add cross-service correlation
            correlated_services = self.cross_service_correlator.correlate_error(error_context)
            error_context.cross_service_correlation = correlated_services
            
            # Add to pattern analysis
            self.error_patterns.add_error_pattern(error_context)
            
            # Attempt enhanced correction
            return await self._attempt_enhanced_correction(error_context, task_func, *args, **kwargs)
    
    async def _attempt_enhanced_correction(self, error_context: ErrorContext, 
                                         task_func: Callable, *args, **kwargs) -> Any:
        """Attempt enhanced correction with learning"""
        metrics = self.task_metrics[error_context.task_id]
        metrics.correction_attempts += 1
        
        # Get optimal strategy using learning engine
        strategy = self.learning_engine.get_optimal_strategy(error_context)
        
        correction_action = CorrectionAction(
            action_id=str(uuid.uuid4()),
            strategy=strategy,
            description=f"Enhanced {strategy.value} correction for {error_context.error_type}"
        )
        
        start_time = time.time()
        
        try:
            # Execute correction strategy
            if strategy in self.correction_strategies:
                result = await self.correction_strategies[strategy](
                    error_context, task_func, *args, **kwargs
                )
                correction_action.success = True
                metrics.successful_corrections += 1
            else:
                raise ValueError(f"Unknown correction strategy: {strategy}")
            
            correction_action.execution_time = time.time() - start_time
            metrics.average_correction_time = self._update_average(
                metrics.average_correction_time,
                correction_action.execution_time,
                metrics.correction_attempts
            )
            
            # Learn from the correction
            self.learning_engine.learn_from_error(error_context, correction_action)
            
            self.recovery_history.append(correction_action)
            return result
            
        except Exception as correction_error:
            correction_action.success = False
            correction_action.execution_time = time.time() - start_time
            
            # Learn from failed correction
            self.learning_engine.learn_from_error(error_context, correction_action)
            
            # If correction failed, try escalation
            if error_context.recovery_attempts < error_context.max_recovery_attempts:
                error_context.recovery_attempts += 1
                return await self._attempt_enhanced_correction(error_context, task_func, *args, **kwargs)
            else:
                # Final escalation
                return await self._escalate_strategy(error_context, task_func, *args, **kwargs)
    
    async def _predictive_strategy(self, error_context: ErrorContext, 
                                 task_func: Callable, *args, **kwargs) -> Any:
        """Predictive correction strategy"""
        # Apply preventive measures based on prediction
        logging.info(f"Applying predictive correction for {error_context.task_id}")
        
        # Modify parameters based on prediction
        modified_kwargs = kwargs.copy()
        modified_kwargs['timeout'] = modified_kwargs.get('timeout', 30) * 2
        modified_kwargs['retry_on_failure'] = True
        modified_kwargs['predictive_mode'] = True
        
        return await task_func(*args, **modified_kwargs)
    
    async def _collaborative_strategy(self, error_context: ErrorContext, 
                                    task_func: Callable, *args, **kwargs) -> Any:
        """Collaborative correction strategy"""
        # Collaborate with other services to resolve the error
        logging.info(f"Applying collaborative correction for {error_context.task_id}")
        
        # Get correlated services
        correlated_services = error_context.cross_service_correlation
        
        if correlated_services:
            # Try to resolve through collaboration
            for service_id in correlated_services:
                try:
                    # Attempt collaborative resolution
                    result = await self._resolve_collaboratively(service_id, task_func, *args, **kwargs)
                    return result
                except Exception as e:
                    logging.warning(f"Collaborative resolution failed with {service_id}: {e}")
                    continue
        
        # Fall back to standard correction
        return await self._adapt_strategy(error_context, task_func, *args, **kwargs)
    
    async def _resolve_collaboratively(self, service_id: str, task_func: Callable, 
                                     *args, **kwargs) -> Any:
        """Resolve error through service collaboration"""
        # Simplified collaborative resolution
        # In production, implement actual service-to-service communication
        
        # Modify task for collaborative execution
        modified_kwargs = kwargs.copy()
        modified_kwargs['collaborative_service'] = service_id
        modified_kwargs['collaborative_mode'] = True
        
        return await task_func(*args, **modified_kwargs)
    
    async def _apply_predictive_correction(self, prediction: PredictiveContext, 
                                         task_func: Callable, *args, **kwargs):
        """Apply predictive correction before error occurs"""
        logging.info(f"Applying predictive correction: {prediction.confidence_score:.2f} confidence")
        
        # Store prediction for analysis
        self.predictive_corrections.append(prediction)
        
        # Apply preventive measures
        modified_kwargs = kwargs.copy()
        modified_kwargs['predictive_mode'] = True
        modified_kwargs['resource_limits'] = prediction.resource_usage
        
        # Execute with preventive measures
        await task_func(*args, **modified_kwargs)
    
    def _get_resource_usage(self) -> Dict[str, float]:
        """Get current resource usage"""
        # Simplified - in production get real resource metrics
        return {
            "cpu": 0.5,
            "memory": 0.6,
            "disk": 0.3,
            "network": 0.2
        }
    
    def _get_error_context(self, error: Exception, *args, **kwargs) -> Dict[str, Any]:
        """Get enhanced error context"""
        return {
            "error_type": type(error).__name__,
            "args": str(args),
            "kwargs": str(kwargs),
            "timestamp": time.time()
        }
    
    # Keep existing strategy implementations with enhancements
    async def _retry_strategy(self, error_context: ErrorContext, 
                            task_func: Callable, *args, **kwargs) -> Any:
        """Enhanced retry strategy"""
        max_retries = 3
        base_delay = 1.0
        
        for attempt in range(max_retries):
            try:
                delay = base_delay * (2 ** attempt)
                await asyncio.sleep(delay)
                
                logging.info(f"Retrying task {error_context.task_id} (attempt {attempt + 1})")
                return await task_func(*args, **kwargs)
                
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                logging.warning(f"Retry attempt {attempt + 1} failed: {e}")
    
    async def _fallback_strategy(self, error_context: ErrorContext, 
                               task_func: Callable, *args, **kwargs) -> Any:
        """Enhanced fallback strategy"""
        fallback_func = getattr(task_func, 'fallback', None)
        
        if fallback_func:
            logging.info(f"Using fallback implementation for task {error_context.task_id}")
            return await fallback_func(*args, **kwargs)
        else:
            modified_kwargs = kwargs.copy()
            modified_kwargs['timeout'] = modified_kwargs.get('timeout', 30) * 2
            modified_kwargs['retry_on_failure'] = True
            
            logging.info(f"Using modified parameters for task {error_context.task_id}")
            return await task_func(*args, **modified_kwargs)
    
    async def _adapt_strategy(self, error_context: ErrorContext, 
                            task_func: Callable, *args, **kwargs) -> Any:
        """Enhanced adapt strategy"""
        patterns = self.error_patterns.error_patterns
        
        similar_errors = [
            p for p in patterns.values() 
            if p["count"] > 2 and error_context.error_type in str(p)
        ]
        
        if similar_errors:
            adaptation = self._get_adaptation_for_error(error_context.error_type)
            if adaptation:
                logging.info(f"Applying adaptation for task {error_context.task_id}")
                return await adaptation(task_func, *args, **kwargs)
        
        kwargs['timeout'] = kwargs.get('timeout', 30) * 3
        return await task_func(*args, **kwargs)
    
    async def _learn_strategy(self, error_context: ErrorContext, 
                            task_func: Callable, *args, **kwargs) -> Any:
        """Enhanced learn strategy"""
        learning_data = {
            "error_type": error_context.error_type,
            "error_message": error_context.error_message,
            "task_id": error_context.task_id,
            "agent_id": error_context.agent_id,
            "context": error_context.context_data,
            "timestamp": error_context.timestamp
        }
        
        if error_context.task_id not in self.learning_models:
            self.learning_models[error_context.task_id] = []
        
        self.learning_models[error_context.task_id].append(learning_data)
        
        improved_func = self._apply_learned_improvements(task_func, learning_data)
        
        logging.info(f"Applying learned improvements for task {error_context.task_id}")
        return await improved_func(*args, **kwargs)
    
    async def _escalate_strategy(self, error_context: ErrorContext, 
                               task_func: Callable, *args, **kwargs) -> Any:
        """Enhanced escalate strategy"""
        logging.error(f"Escalating error for task {error_context.task_id}: {error_context.error_message}")
        
        escalation_report = {
            "error_context": error_context,
            "task_metrics": self.task_metrics.get(error_context.task_id),
            "recovery_history": [action for action in self.recovery_history 
                               if action.strategy != CorrectionStrategy.ESCALATE],
            "predictive_corrections": len(self.predictive_corrections),
            "timestamp": time.time()
        }
        
        logging.critical(f"Task {error_context.task_id} escalated: {escalation_report}")
        
        raise Exception(f"Task {error_context.task_id} failed after all correction attempts")
    
    async def _rollback_strategy(self, error_context: ErrorContext, 
                               task_func: Callable, *args, **kwargs) -> Any:
        """Enhanced rollback strategy"""
        logging.info(f"Rolling back task {error_context.task_id}")
        
        # In production, implement actual rollback logic
        raise Exception(f"Rollback not implemented for task {error_context.task_id}")
    
    def _get_adaptation_for_error(self, error_type: str) -> Optional[Callable]:
        """Get adaptation function for a specific error type"""
        adaptations = {
            "ConnectionError": self._adapt_connection_error,
            "TimeoutError": self._adapt_timeout_error,
            "ValueError": self._adapt_value_error,
            "TypeError": self._adapt_type_error
        }
        return adaptations.get(error_type)
    
    async def _adapt_connection_error(self, task_func: Callable, *args, **kwargs):
        """Adapt for connection errors"""
        kwargs['retry_connections'] = True
        kwargs['connection_timeout'] = kwargs.get('connection_timeout', 60) * 2
        return await task_func(*args, **kwargs)
    
    async def _adapt_timeout_error(self, task_func: Callable, *args, **kwargs):
        """Adapt for timeout errors"""
        kwargs['timeout'] = kwargs.get('timeout', 30) * 3
        kwargs['enable_timeout_retry'] = True
        return await task_func(*args, **kwargs)
    
    async def _adapt_value_error(self, task_func: Callable, *args, **kwargs):
        """Adapt for value errors"""
        if args:
            modified_args = (str(args[0]),) + args[1:]
            return await task_func(*modified_args, **kwargs)
        return await task_func(*args, **kwargs)
    
    async def _adapt_type_error(self, task_func: Callable, *args, **kwargs):
        """Adapt for type errors"""
        try:
            return await task_func(*args, **kwargs)
        except TypeError:
            converted_args = tuple(str(arg) if not isinstance(arg, (int, float, bool)) 
                                else arg for arg in args)
            return await task_func(*converted_args, **kwargs)
    
    def _apply_learned_improvements(self, task_func: Callable, learning_data: Dict[str, Any]) -> Callable:
        """Apply learned improvements to the task function"""
        async def improved_task_func(*args, **kwargs):
            if learning_data.get("error_type") == "TimeoutError":
                kwargs['timeout'] = kwargs.get('timeout', 30) * 2
            
            if learning_data.get("error_type") == "ConnectionError":
                kwargs['retry_connections'] = True
            
            return await task_func(*args, **kwargs)
        
        return improved_task_func
    
    def _determine_severity(self, error: Exception) -> ErrorSeverity:
        """Determine error severity based on error type and context"""
        error_type = type(error).__name__
        
        if any(network_error in error_type.lower() for network_error in 
               ["connection", "timeout", "network", "http"]):
            return ErrorSeverity.MEDIUM
        
        if any(resource_error in error_type.lower() for resource_error in 
               ["memory", "disk", "resource", "quota"]):
            return ErrorSeverity.HIGH
        
        if any(critical_error in error_type.lower() for critical_error in 
               ["system", "kernel", "fatal", "panic"]):
            return ErrorSeverity.CRITICAL
        
        return ErrorSeverity.LOW
    
    def _update_average(self, current_avg: float, new_value: float, count: int) -> float:
        """Update running average"""
        return (current_avg * (count - 1) + new_value) / count
    
    def get_enhanced_system_health(self) -> Dict[str, Any]:
        """Get enhanced system health metrics"""
        total_tasks = len(self.task_metrics)
        total_executions = sum(m.total_executions for m in self.task_metrics.values())
        total_successes = sum(m.successful_executions for m in self.task_metrics.values())
        total_corrections = sum(m.correction_attempts for m in self.task_metrics.values())
        successful_corrections = sum(m.successful_corrections for m in self.task_metrics.values())
        predictive_corrections = sum(m.predictive_corrections for m in self.task_metrics.values())
        
        return {
            "total_tasks": total_tasks,
            "total_executions": total_executions,
            "success_rate": total_successes / max(1, total_executions),
            "correction_rate": total_corrections / max(1, total_executions),
            "correction_success_rate": successful_corrections / max(1, total_corrections),
            "predictive_corrections": predictive_corrections,
            "prediction_accuracy": sum(m.prediction_accuracy for m in self.task_metrics.values()) / max(1, total_tasks),
            "collaboration_success_rate": sum(m.collaboration_success_rate for m in self.task_metrics.values()) / max(1, total_tasks),
            "learning_models": len(self.learning_engine.learning_models),
            "error_patterns": len(self.error_patterns.error_patterns),
            "predictive_corrections_applied": len(self.predictive_corrections),
            "recent_corrections": self.recovery_history[-10:] if self.recovery_history else []
        }
    
    def get_task_metrics(self, task_id: str) -> Optional[TaskMetrics]:
        """Get metrics for a specific task"""
        return self.task_metrics.get(task_id)
    
    def get_all_task_metrics(self) -> Dict[str, TaskMetrics]:
        """Get metrics for all tasks"""
        return self.task_metrics.copy()