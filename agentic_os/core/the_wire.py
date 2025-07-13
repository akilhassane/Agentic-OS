"""
The Wire - Dynamic Agent-Based Service Architecture
Inspired by AWS, Azure, and Google Cloud service architectures

This module implements a dynamic service mesh where every agent becomes a service
that can be called, integrated, and orchestrated like cloud services but with
AI capabilities and dynamic adaptation.
"""

import asyncio
import json
import uuid
import time
import weakref
from typing import Dict, List, Any, Optional, Callable, Union, TypeVar, Generic
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
import threading
from concurrent.futures import ThreadPoolExecutor, Future
import logging

# Type definitions
T = TypeVar('T')
ServiceResponse = TypeVar('ServiceResponse')

class ServiceState(Enum):
    """Service lifecycle states"""
    INITIALIZING = "initializing"
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    MAINTENANCE = "maintenance"
    TERMINATED = "terminated"

class ServiceType(Enum):
    """Types of services in the Wire"""
    COMPUTE = "compute"
    STORAGE = "storage"
    NETWORK = "network"
    AI_AGENT = "ai_agent"
    API_GATEWAY = "api_gateway"
    MESSAGE_QUEUE = "message_queue"
    DATABASE = "database"
    ORCHESTRATOR = "orchestrator"
    MONITOR = "monitor"
    SECURITY = "security"

@dataclass
class ServiceMetadata:
    """Metadata for a service in the Wire"""
    service_id: str
    name: str
    service_type: ServiceType
    version: str
    description: str
    tags: Dict[str, str] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)

@dataclass
class ServiceEndpoint:
    """Service endpoint definition"""
    method: str
    path: str
    handler: Callable
    input_schema: Optional[Dict] = None
    output_schema: Optional[Dict] = None
    rate_limit: Optional[int] = None
    authentication_required: bool = False
    description: str = ""

@dataclass
class ServiceRequest:
    """Request to a service"""
    request_id: str
    source_service_id: str
    target_service_id: str
    method: str
    path: str
    data: Any = None
    headers: Dict[str, str] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)

@dataclass
class ServiceResponse:
    """Response from a service"""
    request_id: str
    status_code: int
    data: Any = None
    headers: Dict[str, str] = field(default_factory=dict)
    error: Optional[str] = None
    execution_time: float = 0.0
    timestamp: float = field(default_factory=time.time)

class ServiceDiscovery:
    """Service discovery and registry for the Wire"""
    
    def __init__(self):
        self._services: Dict[str, 'WireService'] = {}
        self._service_metadata: Dict[str, ServiceMetadata] = {}
        self._service_endpoints: Dict[str, List[ServiceEndpoint]] = {}
        self._service_health: Dict[str, ServiceState] = {}
        self._lock = threading.RLock()
        
    def register_service(self, service: 'WireService') -> bool:
        """Register a service in the Wire"""
        with self._lock:
            service_id = service.metadata.service_id
            self._services[service_id] = service
            self._service_metadata[service_id] = service.metadata
            self._service_endpoints[service_id] = service.get_endpoints()
            self._service_health[service_id] = ServiceState.HEALTHY
            
            logging.info(f"Service registered: {service.metadata.name} ({service_id})")
            return True
    
    def unregister_service(self, service_id: str) -> bool:
        """Unregister a service from the Wire"""
        with self._lock:
            if service_id in self._services:
                service_name = self._service_metadata[service_id].name
                del self._services[service_id]
                del self._service_metadata[service_id]
                del self._service_endpoints[service_id]
                del self._service_health[service_id]
                
                logging.info(f"Service unregistered: {service_name} ({service_id})")
                return True
            return False
    
    def discover_services(self, service_type: Optional[ServiceType] = None, 
                         tags: Optional[Dict[str, str]] = None) -> List[ServiceMetadata]:
        """Discover services by type and tags"""
        with self._lock:
            services = []
            for metadata in self._service_metadata.values():
                if service_type and metadata.service_type != service_type:
                    continue
                if tags:
                    if not all(metadata.tags.get(k) == v for k, v in tags.items()):
                        continue
                services.append(metadata)
            return services
    
    def get_service(self, service_id: str) -> Optional['WireService']:
        """Get a service by ID"""
        return self._services.get(service_id)
    
    def get_service_health(self, service_id: str) -> Optional[ServiceState]:
        """Get service health status"""
        return self._service_health.get(service_id)
    
    def update_service_health(self, service_id: str, state: ServiceState):
        """Update service health status"""
        with self._lock:
            if service_id in self._service_health:
                self._service_health[service_id] = state

class LoadBalancer:
    """Load balancer for distributing requests across service instances"""
    
    def __init__(self, discovery: ServiceDiscovery):
        self.discovery = discovery
        self._round_robin_counters: Dict[str, int] = {}
        
    def select_service_instance(self, service_type: ServiceType, 
                              tags: Optional[Dict[str, str]] = None) -> Optional[str]:
        """Select a healthy service instance using round-robin"""
        services = self.discovery.discover_services(service_type, tags)
        healthy_services = [
            s for s in services 
            if self.discovery.get_service_health(s.service_id) == ServiceState.HEALTHY
        ]
        
        if not healthy_services:
            return None
        
        # Round-robin selection
        key = f"{service_type.value}:{json.dumps(tags or {}, sort_keys=True)}"
        counter = self._round_robin_counters.get(key, 0)
        selected = healthy_services[counter % len(healthy_services)]
        self._round_robin_counters[key] = counter + 1
        
        return selected.service_id

class CircuitBreaker:
    """Circuit breaker pattern for service resilience"""
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 60.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self._failure_counts: Dict[str, int] = {}
        self._last_failure_times: Dict[str, float] = {}
        self._circuit_states: Dict[str, str] = {}  # CLOSED, OPEN, HALF_OPEN
        
    def can_execute(self, service_id: str) -> bool:
        """Check if request can be executed based on circuit breaker state"""
        state = self._circuit_states.get(service_id, "CLOSED")
        
        if state == "CLOSED":
            return True
        elif state == "OPEN":
            # Check if recovery timeout has passed
            last_failure = self._last_failure_times.get(service_id, 0)
            if time.time() - last_failure > self.recovery_timeout:
                self._circuit_states[service_id] = "HALF_OPEN"
                return True
            return False
        elif state == "HALF_OPEN":
            return True
        
        return False
    
    def record_success(self, service_id: str):
        """Record successful execution"""
        self._failure_counts[service_id] = 0
        self._circuit_states[service_id] = "CLOSED"
    
    def record_failure(self, service_id: str):
        """Record failed execution"""
        self._failure_counts[service_id] = self._failure_counts.get(service_id, 0) + 1
        self._last_failure_times[service_id] = time.time()
        
        if self._failure_counts[service_id] >= self.failure_threshold:
            self._circuit_states[service_id] = "OPEN"

class MessageBroker:
    """Message broker for asynchronous communication between services"""
    
    def __init__(self):
        self._topics: Dict[str, List[Callable]] = {}
        self._message_queue = asyncio.Queue()
        self._running = False
        
    async def start(self):
        """Start the message broker"""
        self._running = True
        asyncio.create_task(self._process_messages())
    
    async def stop(self):
        """Stop the message broker"""
        self._running = False
    
    def subscribe(self, topic: str, handler: Callable):
        """Subscribe to a topic"""
        if topic not in self._topics:
            self._topics[topic] = []
        self._topics[topic].append(handler)
    
    def unsubscribe(self, topic: str, handler: Callable):
        """Unsubscribe from a topic"""
        if topic in self._topics:
            try:
                self._topics[topic].remove(handler)
            except ValueError:
                pass
    
    async def publish(self, topic: str, message: Any):
        """Publish a message to a topic"""
        await self._message_queue.put((topic, message))
    
    async def _process_messages(self):
        """Process messages from the queue"""
        while self._running:
            try:
                topic, message = await asyncio.wait_for(
                    self._message_queue.get(), timeout=1.0
                )
                
                handlers = self._topics.get(topic, [])
                for handler in handlers:
                    try:
                        if asyncio.iscoroutinefunction(handler):
                            await handler(message)
                        else:
                            handler(message)
                    except Exception as e:
                        logging.error(f"Error in message handler: {e}")
                        
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logging.error(f"Error processing message: {e}")

class WireService(ABC):
    """Base class for all services in the Wire"""
    
    def __init__(self, metadata: ServiceMetadata, wire: 'TheWire'):
        self.metadata = metadata
        self.wire = wire
        self._endpoints: List[ServiceEndpoint] = []
        self._state = ServiceState.INITIALIZING
        self._executor = ThreadPoolExecutor(max_workers=10)
        
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the service"""
        pass
    
    @abstractmethod
    async def shutdown(self) -> bool:
        """Shutdown the service"""
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """Perform health check"""
        pass
    
    def add_endpoint(self, endpoint: ServiceEndpoint):
        """Add an endpoint to the service"""
        self._endpoints.append(endpoint)
    
    def get_endpoints(self) -> List[ServiceEndpoint]:
        """Get all endpoints for this service"""
        return self._endpoints.copy()
    
    async def handle_request(self, request: ServiceRequest) -> ServiceResponse:
        """Handle incoming request"""
        start_time = time.time()
        
        try:
            # Find matching endpoint
            endpoint = None
            for ep in self._endpoints:
                if ep.method == request.method and ep.path == request.path:
                    endpoint = ep
                    break
            
            if not endpoint:
                return ServiceResponse(
                    request_id=request.request_id,
                    status_code=404,
                    error="Endpoint not found",
                    execution_time=time.time() - start_time
                )
            
            # Execute handler
            if asyncio.iscoroutinefunction(endpoint.handler):
                result = await endpoint.handler(request)
            else:
                # Run sync handler in executor
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    self._executor, endpoint.handler, request
                )
            
            return ServiceResponse(
                request_id=request.request_id,
                status_code=200,
                data=result,
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            logging.error(f"Error handling request: {e}")
            return ServiceResponse(
                request_id=request.request_id,
                status_code=500,
                error=str(e),
                execution_time=time.time() - start_time
            )

class TheWire:
    """
    The Wire - Main orchestrator for the dynamic agent-based service architecture
    
    Inspired by AWS, Azure, and Google Cloud, The Wire provides:
    - Service discovery and registration
    - Load balancing and failover
    - Circuit breaker patterns
    - Message broker for async communication
    - Service mesh capabilities
    - Dynamic scaling and adaptation
    """
    
    def __init__(self):
        self.discovery = ServiceDiscovery()
        self.load_balancer = LoadBalancer(self.discovery)
        self.circuit_breaker = CircuitBreaker()
        self.message_broker = MessageBroker()
        self._running = False
        
    async def start(self):
        """Start The Wire"""
        self._running = True
        await self.message_broker.start()
        logging.info("The Wire started successfully")
    
    async def stop(self):
        """Stop The Wire"""
        self._running = False
        await self.message_broker.stop()
        logging.info("The Wire stopped")
    
    def register_service(self, service: WireService) -> bool:
        """Register a service with The Wire"""
        return self.discovery.register_service(service)
    
    def unregister_service(self, service_id: str) -> bool:
        """Unregister a service from The Wire"""
        return self.discovery.unregister_service(service_id)
    
    async def call_service(self, target_service_id: str, method: str, 
                          path: str, data: Any = None, 
                          source_service_id: str = "system") -> ServiceResponse:
        """Call a service method"""
        
        # Check circuit breaker
        if not self.circuit_breaker.can_execute(target_service_id):
            return ServiceResponse(
                request_id=str(uuid.uuid4()),
                status_code=503,
                error="Service unavailable (circuit breaker open)"
            )
        
        # Get service
        service = self.discovery.get_service(target_service_id)
        if not service:
            return ServiceResponse(
                request_id=str(uuid.uuid4()),
                status_code=404,
                error="Service not found"
            )
        
        # Create request
        request = ServiceRequest(
            request_id=str(uuid.uuid4()),
            source_service_id=source_service_id,
            target_service_id=target_service_id,
            method=method,
            path=path,
            data=data
        )
        
        try:
            # Handle request
            response = await service.handle_request(request)
            
            # Record success/failure for circuit breaker
            if response.status_code < 500:
                self.circuit_breaker.record_success(target_service_id)
            else:
                self.circuit_breaker.record_failure(target_service_id)
            
            return response
            
        except Exception as e:
            self.circuit_breaker.record_failure(target_service_id)
            return ServiceResponse(
                request_id=request.request_id,
                status_code=500,
                error=str(e)
            )
    
    async def call_service_by_type(self, service_type: ServiceType, method: str,
                                  path: str, data: Any = None,
                                  tags: Optional[Dict[str, str]] = None,
                                  source_service_id: str = "system") -> ServiceResponse:
        """Call a service by type using load balancing"""
        
        # Select service instance
        service_id = self.load_balancer.select_service_instance(service_type, tags)
        if not service_id:
            return ServiceResponse(
                request_id=str(uuid.uuid4()),
                status_code=503,
                error="No healthy service instances available"
            )
        
        return await self.call_service(service_id, method, path, data, source_service_id)
    
    async def publish_event(self, topic: str, event: Any):
        """Publish an event to the message broker"""
        await self.message_broker.publish(topic, event)
    
    def subscribe_to_events(self, topic: str, handler: Callable):
        """Subscribe to events from the message broker"""
        self.message_broker.subscribe(topic, handler)
    
    def discover_services(self, service_type: Optional[ServiceType] = None,
                         tags: Optional[Dict[str, str]] = None) -> List[ServiceMetadata]:
        """Discover services"""
        return self.discovery.discover_services(service_type, tags)
    
    async def health_check_all_services(self) -> Dict[str, bool]:
        """Perform health checks on all services"""
        results = {}
        
        for service_id, service in self.discovery._services.items():
            try:
                is_healthy = await service.health_check()
                results[service_id] = is_healthy
                
                # Update service health in discovery
                if is_healthy:
                    self.discovery.update_service_health(service_id, ServiceState.HEALTHY)
                else:
                    self.discovery.update_service_health(service_id, ServiceState.UNHEALTHY)
                    
            except Exception as e:
                logging.error(f"Health check failed for service {service_id}: {e}")
                results[service_id] = False
                self.discovery.update_service_health(service_id, ServiceState.UNHEALTHY)
        
        return results