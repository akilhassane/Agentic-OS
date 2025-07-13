"""
Tests for Network Service - Component 013
Comprehensive test suite for network_service functionality
"""

import pytest
import asyncio
import time
from unittest.mock import Mock, patch
from typing import Dict, Any

from .network_service_013 import NetworkService, NetworkServiceConfig, create_network_service

class TestNetworkService:
    """Test suite for NetworkService"""
    
    @pytest.fixture
    def config(self):
        """Create test configuration"""
        return NetworkServiceConfig(
            component_id=f"test_network_service_013",
            enabled=True,
            max_workers=2,
            timeout=10.0,
            retry_attempts=2
        )
    
    @pytest.fixture
    def component(self, config):
        """Create test component"""
        return NetworkService(config)
    
    def test_component_initialization(self, component):
        """Test component initialization"""
        assert component.config.component_id == f"test_network_service_013"
        assert component.status.value == "idle"
        assert component.metrics == {}
    
    @pytest.mark.asyncio
    async def test_process_task(self, component):
        """Test task processing"""
        task_data = {"test": "data", "index": 13}
        result = await component.process_task(task_data)
        
        assert result["status"] == "completed"
        assert "processing_time" in result
        assert "confidence" in result
        assert result["metadata"]["component"] == "network_service"
    
    @pytest.mark.asyncio
    async def test_optimize_performance(self, component):
        """Test performance optimization"""
        optimizations = await component.optimize_performance()
        
        assert "cpu_optimization" in optimizations
        assert "memory_optimization" in optimizations
        assert "estimated_improvement" in optimizations
    
    def test_get_status(self, component):
        """Test status retrieval"""
        status = component.get_status()
        
        assert status["component_id"] == component.config.component_id
        assert "status" in status
        assert "metrics" in status
        assert "config" in status
    
    def test_factory_function(self):
        """Test factory function"""
        component = create_network_service("factory_test_013")
        
        assert isinstance(component, NetworkService)
        assert component.config.component_id == "factory_test_013"

class TestNetworkServiceIntegration:
    """Integration tests for NetworkService"""
    
    @pytest.mark.asyncio
    async def test_end_to_end_processing(self):
        """Test end-to-end processing workflow"""
        config = NetworkServiceConfig(
            component_id=f"integration_test_013",
            enabled=True
        )
        component = NetworkService(config)
        
        # Process multiple tasks
        tasks = [{"data": f"task_{i}", "index": i} for i in range(3)]
        results = []
        
        for task in tasks:
            result = await component.process_task(task)
            results.append(result)
        
        assert len(results) == 3
        assert all(r["status"] == "completed" for r in results)
        
        # Check metrics
        status = component.get_status()
        assert status["metrics"]["total_tasks"] == 3
        assert status["metrics"]["successful_tasks"] == 3

if __name__ == "__main__":
    pytest.main([__file__])
