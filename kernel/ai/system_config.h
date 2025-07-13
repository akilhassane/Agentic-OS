#pragma once

#include "multi_agent_system.h"
#include "agent_wire_protocol.h"
#include "engines/task_planning_engine.h"
#include "engines/knowledge_engine.h"
#include "neural_interface/neural_shell.h"
#include "device_integration/device_manager.h"
#include "monitoring/system_monitor.h"
#include "ui/neural_interface_ui.h"
#include <memory>
#include <vector>
#include <map>

namespace AgenticOS {
namespace AI {

// System Configuration - Handles comprehensive system initialization and configuration
class SystemConfig {
private:
    // System components
    struct SystemComponents {
        std::unique_ptr<MultiAgentSystem> multi_agent_system;
        std::unique_ptr<TaskPlanningEngine> task_planning_engine;
        std::unique_ptr<KnowledgeEngine> knowledge_engine;
        std::unique_ptr<NeuralShell> neural_shell;
        std::unique_ptr<DeviceManager> device_manager;
        std::unique_ptr<SystemMonitor> system_monitor;
        std::unique_ptr<NeuralInterfaceUI> neural_interface_ui;
    };
    
    // Configuration capabilities
    enum class ConfigCapability {
        SYSTEM_INITIALIZATION,
        COMPONENT_CONFIGURATION,
        AGENT_ORCHESTRATION,
        RESOURCE_ALLOCATION,
        STARTUP_SEQUENCE,
        SHUTDOWN_SEQUENCE,
        CONFIGURATION_MANAGEMENT,
        SYSTEM_OPTIMIZATION,
        PERFORMANCE_TUNING,
        SECURITY_CONFIGURATION,
        NETWORK_CONFIGURATION,
        STORAGE_CONFIGURATION,
        BACKUP_CONFIGURATION,
        RECOVERY_CONFIGURATION,
        MONITORING_CONFIGURATION,
        LOGGING_CONFIGURATION
    };
    
    // System context
    struct SystemContext {
        std::string system_mode;
        std::string configuration_profile;
        std::vector<std::string> enabled_components;
        std::vector<ConfigCapability> required_capabilities;
        float performance_target;
        uint64_t initialization_timeout;
        bool enable_auto_optimization;
        bool enable_auto_recovery;
    };
    
    // Core components
    std::unique_ptr<SystemComponents> system_components;
    std::map<ConfigCapability, bool> capability_status;
    std::map<std::string, SystemContext> context_cache;
    
    // Performance tracking
    struct ConfigMetrics {
        uint64_t initializations_performed;
        uint64_t configurations_applied;
        uint64_t optimizations_executed;
        uint64_t recoveries_performed;
        float average_startup_time;
        float system_stability_score;
        std::map<ConfigCapability, uint64_t> capability_usage;
        std::vector<std::string> recent_config_events;
    };
    
    ConfigMetrics metrics;
    
public:
    SystemConfig() {
        system_components = std::make_unique<SystemComponents>();
    }
    
    // Core configuration functions
    KernelResult InitializeSystem(const SystemInitRequest& request, SystemInitResult& result);
    KernelResult ConfigureComponent(const ComponentConfig& config, const SystemContext& context);
    KernelResult OrchestrateAgents(const AgentOrchestration& orchestration, OrchestrationResult& result);
    KernelResult AllocateResources(const ResourceAllocationRequest& request, ResourceAllocationResult& result);
    KernelResult OptimizeSystem(const SystemOptimization& optimization, OptimizationResult& result);
    KernelResult ManageConfiguration(const ConfigManagement& management, ConfigResult& result);
    
    // Configuration management
    KernelResult EnableCapability(ConfigCapability capability);
    KernelResult DisableCapability(ConfigCapability capability);
    bool IsCapabilityEnabled(ConfigCapability capability);
    std::vector<ConfigCapability> GetEnabledCapabilities();
    
    // Context management
    KernelResult SetSystemContext(const std::string& context_id, const SystemContext& context);
    KernelResult GetSystemContext(const std::string& context_id, SystemContext& context);
    KernelResult UpdateSystemContext(const std::string& context_id, const std::map<std::string, std::string>& updates);
    
    // Performance monitoring
    ConfigMetrics GetMetrics() const;
    void ResetMetrics();
    void GenerateConfigReport();
    
private:
    // Configuration implementations
    KernelResult ExecuteSystemInitialization(const std::vector<uint8_t>& init_data);
    KernelResult ExecuteComponentConfiguration(const std::vector<uint8_t>& config_data);
    KernelResult ExecuteAgentOrchestration(const std::vector<uint8_t>& orchestration_data);
    KernelResult ExecuteResourceAllocation(const std::vector<uint8_t>& allocation_data);
    KernelResult ExecuteSystemOptimization(const std::vector<uint8_t>& optimization_data);
    
    // Configuration utility functions
    float CalculateSystemStability(const std::vector<uint8_t>& stability_data);
    void AnalyzeSystemPerformance(const std::vector<uint8_t>& performance_data);
    void UpdateSystemModel(const std::string& model_id, const std::vector<uint8_t>& model_data);
    void OptimizeConfigurationStrategy(const std::vector<uint8_t>& strategy_data);
    
    // Utility functions
    SystemContext SelectBestContext(const std::string& task_description);
    void LogConfigOperation(const std::string& operation, const std::string& details);
};

// Configuration data structures
struct SystemInitRequest {
    std::string request_id;
    std::string system_mode;
    std::vector<std::string> required_components;
    std::map<std::string, float> init_parameters;
    uint64_t timeout;
    bool enable_auto_configuration;
};

struct SystemInitResult {
    std::string result_id;
    std::string request_id;
    bool success;
    std::vector<std::string> initialized_components;
    std::map<std::string, float> init_metrics;
    uint64_t initialization_time;
    std::string error_message;
};

struct ComponentConfig {
    std::string config_id;
    std::string component_id;
    std::string config_type;
    std::map<std::string, std::string> config_parameters;
    std::vector<std::string> config_options;
    uint64_t timeout;
    bool enable_auto_configuration;
};

struct AgentOrchestration {
    std::string orchestration_id;
    std::string orchestration_type;
    std::vector<std::string> agent_ids;
    std::map<std::string, float> orchestration_parameters;
    uint64_t timeout;
    float coordination_level;
};

struct OrchestrationResult {
    std::string result_id;
    std::string orchestration_id;
    std::map<std::string, float> orchestration_metrics;
    float coordination_score;
    uint64_t orchestration_time;
    std::vector<std::string> coordinated_agents;
};

struct ResourceAllocationRequest {
    std::string request_id;
    std::string resource_type;
    uint64_t quantity_required;
    std::map<std::string, float> allocation_parameters;
    uint64_t duration;
    float priority;
};

struct ResourceAllocationResult {
    std::string result_id;
    std::string request_id;
    std::map<std::string, float> allocation_metrics;
    uint64_t allocated_quantity;
    uint64_t allocation_time;
    std::vector<std::string> allocated_resources;
};

struct SystemOptimization {
    std::string optimization_id;
    std::string optimization_type;
    std::vector<std::string> target_components;
    std::map<std::string, float> optimization_parameters;
    float target_performance;
    uint64_t timeout;
};

struct ConfigManagement {
    std::string management_id;
    std::string management_type;
    std::vector<std::string> managed_components;
    std::map<std::string, float> management_parameters;
    uint64_t timeout;
    bool enable_auto_management;
};

struct ConfigResult {
    std::string result_id;
    std::string management_id;
    std::map<std::string, float> management_metrics;
    float management_score;
    uint64_t management_time;
    std::vector<std::string> managed_components;
};

struct SystemProfile {
    std::string profile_id;
    std::string profile_name;
    std::map<std::string, std::string> profile_settings;
    std::vector<std::string> enabled_features;
    float performance_target;
    uint64_t last_updated;
};

struct StartupSequence {
    std::string sequence_id;
    std::vector<std::string> startup_steps;
    std::map<std::string, float> step_parameters;
    uint64_t total_timeout;
    bool enable_parallel_startup;
};

} // namespace AI
} // namespace AgenticOS