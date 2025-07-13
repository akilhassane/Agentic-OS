"""
Self-Correction System for Agentic Tasks

This module implements comprehensive self-correction capabilities for agentic tasks,
including error detection, recovery mechanisms, adaptive learning, and continuous improvement.
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

# Type definitions
T = TypeVar('T')

class ErrorSeverity(Enum):
    """Error severity levels for self-correction"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class CorrectionStrategy(Enum):
    """Self-correction strategies"""
    RETRY = "retry"
    FALLBACK = "fallback"
    ADAPT = "adapt"
    LEARN = "learn"
    ESCALATE = "escalate"
    ROLLBACK = "rollback"

class TaskState(Enum):
    """Task execution states"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CORRECTING = "correcting"
    RECOVERED = "recovered"

@dataclass
class ErrorContext:
    """Context information for error handling"""
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

@dataclass
class CorrectionAction:
    """A self-correction action"""
    action_id: str
    strategy: CorrectionStrategy
    description: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    success: Optional[bool] = None
    execution_time: float = 0.0

@dataclass
class TaskMetrics:
    """Metrics for task performance and self-correction"""
    task_id: str
    agent_id: str
    total_executions: int = 0
    successful_executions: int = 0
    failed_executions: int = 0
    correction_attempts: int = 0
    successful_corrections: int = 0
    average_execution_time: float = 0.0
    average_correction_time: float = 0.0
    last_execution_time: float = 0.0
    error_patterns: Dict[str, int] = field(default_factory=dict)
    learning_improvements: List[Dict[str, Any]] = field(default_factory=list)

class ErrorPattern:
    """Pattern recognition for errors"""
    
    def __init__(self):
        self.patterns: Dict[str, Dict[str, Any]] = {}
        self.error_frequency: Dict[str, int] = {}
        self.correlation_matrix: Dict[str, Dict[str, float]] = {}
    
    def add_error(self, error_context: ErrorContext):
        """Add an error to pattern analysis"""
        error_key = f"{error_context.error_type}:{error_context.severity.value}"
        
        if error_key not in self.error_frequency:
            self.error_frequency[error_key] = 0
        self.error_frequency[error_key] += 1
        
        # Update patterns
        if error_key not in self.patterns:
            self.patterns[error_key] = {
                "count": 0,
                "first_seen": error_context.timestamp,
                "last_seen": error_context.timestamp,
                "contexts": [],
                "recovery_success_rate": 0.0
            }
        
        pattern = self.patterns[error_key]
        pattern["count"] += 1
        pattern["last_seen"] = error_context.timestamp
        pattern["contexts"].append({
            "task_id": error_context.task_id,
            "agent_id": error_context.agent_id,
            "recovery_attempts": error_context.recovery_attempts
        })
    
    def get_common_patterns(self) -> List[Dict[str, Any]]:
        """Get most common error patterns"""
        sorted_patterns = sorted(
            self.patterns.items(),
            key=lambda x: x[1]["count"],
            reverse=True
        )
        return [
            {
                "error_key": key,
                "count": pattern["count"],
                "frequency": pattern["count"] / max(1, sum(self.error_frequency.values())),
                "recovery_rate": pattern["recovery_success_rate"]
            }
            for key, pattern in sorted_patterns[:10]
        ]

class SelfCorrectionEngine:
    """Main self-correction engine for agentic tasks"""
    
    def __init__(self):
        self.error_patterns = ErrorPattern()
        self.task_metrics: Dict[str, TaskMetrics] = {}
        self.correction_strategies: Dict[CorrectionStrategy, Callable] = {}
        self.learning_models: Dict[str, Any] = {}
        self.recovery_history: List[CorrectionAction] = []
        self._lock = threading.RLock()
        
        # Initialize default correction strategies
        self._initialize_strategies()
    
    def _initialize_strategies(self):
        """Initialize default correction strategies"""
        self.correction_strategies[CorrectionStrategy.RETRY] = self._retry_strategy
        self.correction_strategies[CorrectionStrategy.FALLBACK] = self._fallback_strategy
        self.correction_strategies[CorrectionStrategy.ADAPT] = self._adapt_strategy
        self.correction_strategies[CorrectionStrategy.LEARN] = self._learn_strategy
        self.correction_strategies[CorrectionStrategy.ESCALATE] = self._escalate_strategy
        self.correction_strategies[CorrectionStrategy.ROLLBACK] = self._rollback_strategy
    
    async def execute_with_correction(self, task_id: str, agent_id: str, 
                                    task_func: Callable, *args, **kwargs) -> Any:
        """Execute a task with self-correction capabilities"""
        start_time = time.time()
        
        # Initialize task metrics
        if task_id not in self.task_metrics:
            self.task_metrics[task_id] = TaskMetrics(task_id=task_id, agent_id=agent_id)
        
        metrics = self.task_metrics[task_id]
        metrics.total_executions += 1
        
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
            
            # Create error context
            error_context = ErrorContext(
                error_id=str(uuid.uuid4()),
                task_id=task_id,
                agent_id=agent_id,
                error_type=type(e).__name__,
                error_message=str(e),
                severity=self._determine_severity(e),
                timestamp=time.time(),
                stack_trace=traceback.format_exc()
            )
            
            # Add to pattern analysis
            self.error_patterns.add_error(error_context)
            
            # Attempt self-correction
            return await self._attempt_correction(error_context, task_func, *args, **kwargs)
    
    async def _attempt_correction(self, error_context: ErrorContext, 
                                task_func: Callable, *args, **kwargs) -> Any:
        """Attempt to correct the error using various strategies"""
        metrics = self.task_metrics[error_context.task_id]
        metrics.correction_attempts += 1
        
        # Determine correction strategy based on error type and severity
        strategy = self._select_correction_strategy(error_context)
        
        correction_action = CorrectionAction(
            action_id=str(uuid.uuid4()),
            strategy=strategy,
            description=f"Attempting {strategy.value} correction for {error_context.error_type}"
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
            
            self.recovery_history.append(correction_action)
            return result
            
        except Exception as correction_error:
            correction_action.success = False
            correction_action.execution_time = time.time() - start_time
            
            # If correction failed, try escalation
            if error_context.recovery_attempts < error_context.max_recovery_attempts:
                error_context.recovery_attempts += 1
                return await self._attempt_correction(error_context, task_func, *args, **kwargs)
            else:
                # Final escalation
                return await self._escalate_strategy(error_context, task_func, *args, **kwargs)
    
    def _select_correction_strategy(self, error_context: ErrorContext) -> CorrectionStrategy:
        """Select the best correction strategy based on error context"""
        error_type = error_context.error_type
        severity = error_context.severity
        
        # Simple rule-based strategy selection
        if severity == ErrorSeverity.LOW:
            return CorrectionStrategy.RETRY
        elif severity == ErrorSeverity.MEDIUM:
            return CorrectionStrategy.ADAPT
        elif severity == ErrorSeverity.HIGH:
            return CorrectionStrategy.FALLBACK
        elif severity == ErrorSeverity.CRITICAL:
            return CorrectionStrategy.ESCALATE
        
        # Default to retry for unknown errors
        return CorrectionStrategy.RETRY
    
    def _determine_severity(self, error: Exception) -> ErrorSeverity:
        """Determine error severity based on error type and context"""
        error_type = type(error).__name__
        
        # Network-related errors are usually medium severity
        if any(network_error in error_type.lower() for network_error in 
               ["connection", "timeout", "network", "http"]):
            return ErrorSeverity.MEDIUM
        
        # Resource errors are high severity
        if any(resource_error in error_type.lower() for resource_error in 
               ["memory", "disk", "resource", "quota"]):
            return ErrorSeverity.HIGH
        
        # Critical system errors
        if any(critical_error in error_type.lower() for critical_error in 
               ["system", "kernel", "fatal", "panic"]):
            return ErrorSeverity.CRITICAL
        
        # Default to low severity for unknown errors
        return ErrorSeverity.LOW
    
    async def _retry_strategy(self, error_context: ErrorContext, 
                            task_func: Callable, *args, **kwargs) -> Any:
        """Retry the task with exponential backoff"""
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
        """Use a fallback implementation or alternative approach"""
        # Try to find a fallback implementation
        fallback_func = getattr(task_func, 'fallback', None)
        
        if fallback_func:
            logging.info(f"Using fallback implementation for task {error_context.task_id}")
            return await fallback_func(*args, **kwargs)
        else:
            # Try with modified parameters
            modified_kwargs = kwargs.copy()
            modified_kwargs['timeout'] = modified_kwargs.get('timeout', 30) * 2
            modified_kwargs['retry_on_failure'] = True
            
            logging.info(f"Using modified parameters for task {error_context.task_id}")
            return await task_func(*args, **modified_kwargs)
    
    async def _adapt_strategy(self, error_context: ErrorContext, 
                            task_func: Callable, *args, **kwargs) -> Any:
        """Adapt the task execution based on error patterns"""
        # Analyze error patterns and adapt
        patterns = self.error_patterns.get_common_patterns()
        
        # Find similar errors and their successful resolutions
        similar_errors = [
            p for p in patterns 
            if p["error_key"].startswith(error_context.error_type)
        ]
        
        if similar_errors:
            # Apply learned adaptations
            adaptation = self._get_adaptation_for_error(error_context.error_type)
            if adaptation:
                logging.info(f"Applying adaptation for task {error_context.task_id}")
                return await adaptation(task_func, *args, **kwargs)
        
        # Default to retry with longer timeout
        kwargs['timeout'] = kwargs.get('timeout', 30) * 3
        return await task_func(*args, **kwargs)
    
    async def _learn_strategy(self, error_context: ErrorContext, 
                            task_func: Callable, *args, **kwargs) -> Any:
        """Learn from the error and improve future executions"""
        # Record the error for learning
        learning_data = {
            "error_type": error_context.error_type,
            "error_message": error_context.error_message,
            "task_id": error_context.task_id,
            "agent_id": error_context.agent_id,
            "context": error_context.context_data,
            "timestamp": error_context.timestamp
        }
        
        # Store learning data
        if error_context.task_id not in self.learning_models:
            self.learning_models[error_context.task_id] = []
        
        self.learning_models[error_context.task_id].append(learning_data)
        
        # Try to apply learned improvements
        improved_func = self._apply_learned_improvements(task_func, learning_data)
        
        logging.info(f"Applying learned improvements for task {error_context.task_id}")
        return await improved_func(*args, **kwargs)
    
    async def _escalate_strategy(self, error_context: ErrorContext, 
                               task_func: Callable, *args, **kwargs) -> Any:
        """Escalate the error to higher-level handling"""
        logging.error(f"Escalating error for task {error_context.task_id}: {error_context.error_message}")
        
        # Create escalation report
        escalation_report = {
            "error_context": error_context,
            "task_metrics": self.task_metrics.get(error_context.task_id),
            "recovery_history": [action for action in self.recovery_history 
                               if action.strategy != CorrectionStrategy.ESCALATE],
            "timestamp": time.time()
        }
        
        # Log escalation
        logging.critical(f"Task {error_context.task_id} escalated: {escalation_report}")
        
        # For now, re-raise the original error
        # In a real system, this would trigger human intervention or system-wide recovery
        raise Exception(f"Task {error_context.task_id} failed after all correction attempts")
    
    async def _rollback_strategy(self, error_context: ErrorContext, 
                               task_func: Callable, *args, **kwargs) -> Any:
        """Rollback to a previous stable state"""
        # This would typically involve reverting to a checkpoint or previous state
        logging.info(f"Rolling back task {error_context.task_id}")
        
        # For now, return a default value or re-raise
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
        # Try with different parameter combinations
        if args:
            # Try with first argument as string
            modified_args = (str(args[0]),) + args[1:]
            return await task_func(*modified_args, **kwargs)
        return await task_func(*args, **kwargs)
    
    async def _adapt_type_error(self, task_func: Callable, *args, **kwargs):
        """Adapt for type errors"""
        # Try to convert arguments to expected types
        try:
            return await task_func(*args, **kwargs)
        except TypeError:
            # Try with converted types
            converted_args = tuple(str(arg) if not isinstance(arg, (int, float, bool)) 
                                else arg for arg in args)
            return await task_func(*converted_args, **kwargs)
    
    def _apply_learned_improvements(self, task_func: Callable, learning_data: Dict[str, Any]) -> Callable:
        """Apply learned improvements to the task function"""
        # This is a simplified version - in practice, this would involve
        # more sophisticated learning algorithms
        
        async def improved_task_func(*args, **kwargs):
            # Apply learned improvements
            if learning_data.get("error_type") == "TimeoutError":
                kwargs['timeout'] = kwargs.get('timeout', 30) * 2
            
            if learning_data.get("error_type") == "ConnectionError":
                kwargs['retry_connections'] = True
            
            return await task_func(*args, **kwargs)
        
        return improved_task_func
    
    def _update_average(self, current_avg: float, new_value: float, count: int) -> float:
        """Update running average"""
        return (current_avg * (count - 1) + new_value) / count
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health metrics"""
        total_tasks = len(self.task_metrics)
        total_executions = sum(m.total_executions for m in self.task_metrics.values())
        total_successes = sum(m.successful_executions for m in self.task_metrics.values())
        total_corrections = sum(m.correction_attempts for m in self.task_metrics.values())
        successful_corrections = sum(m.successful_corrections for m in self.task_metrics.values())
        
        return {
            "total_tasks": total_tasks,
            "total_executions": total_executions,
            "success_rate": total_successes / max(1, total_executions),
            "correction_rate": total_corrections / max(1, total_executions),
            "correction_success_rate": successful_corrections / max(1, total_corrections),
            "common_error_patterns": self.error_patterns.get_common_patterns(),
            "recent_corrections": self.recovery_history[-10:] if self.recovery_history else []
        }
    
    def get_task_metrics(self, task_id: str) -> Optional[TaskMetrics]:
        """Get metrics for a specific task"""
        return self.task_metrics.get(task_id)
    
    def get_all_task_metrics(self) -> Dict[str, TaskMetrics]:
        """Get metrics for all tasks"""
        return self.task_metrics.copy()

class SelfCorrectingAgent:
    """Agent wrapper with self-correction capabilities"""
    
    def __init__(self, agent_id: str, correction_engine: SelfCorrectionEngine):
        self.agent_id = agent_id
        self.correction_engine = correction_engine
        self.task_queue: List[Dict[str, Any]] = []
        self.is_running = False
    
    async def execute_task(self, task_name: str, task_func: Callable, 
                          *args, **kwargs) -> Any:
        """Execute a task with self-correction"""
        task_id = f"{self.agent_id}_{task_name}_{uuid.uuid4().hex[:8]}"
        
        return await self.correction_engine.execute_with_correction(
            task_id, self.agent_id, task_func, *args, **kwargs
        )
    
    async def add_task(self, task_name: str, task_func: Callable, 
                      *args, **kwargs) -> str:
        """Add a task to the queue"""
        task_id = f"{self.agent_id}_{task_name}_{uuid.uuid4().hex[:8]}"
        
        self.task_queue.append({
            "task_id": task_id,
            "task_name": task_name,
            "task_func": task_func,
            "args": args,
            "kwargs": kwargs,
            "status": TaskState.PENDING
        })
        
        return task_id
    
    async def process_queue(self):
        """Process the task queue with self-correction"""
        self.is_running = True
        
        while self.is_running and self.task_queue:
            task = self.task_queue.pop(0)
            task["status"] = TaskState.RUNNING
            
            try:
                result = await self.correction_engine.execute_with_correction(
                    task["task_id"], self.agent_id, task["task_func"],
                    *task["args"], **task["kwargs"]
                )
                task["status"] = TaskState.COMPLETED
                task["result"] = result
                
            except Exception as e:
                task["status"] = TaskState.FAILED
                task["error"] = str(e)
                logging.error(f"Task {task['task_id']} failed: {e}")
    
    def stop(self):
        """Stop the agent"""
        self.is_running = False