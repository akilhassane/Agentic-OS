#pragma once

#include "../multi_agent_system.h"
#include "../agent_wire_protocol.h"
#include <memory>
#include <vector>
#include <map>

namespace AgenticOS {
namespace AI {

// Network Agent - Handles network communication, protocol handling, and connectivity management
class NetworkAgent : public BaseAgent {
private:
    // Network components
    struct NetworkEngine {
        std::unique_ptr<ProtocolHandler> protocol_handler;
        std::unique_ptr<ConnectionManager> connection_manager;
        std::unique_ptr<RoutingEngine> routing_engine;
        std::unique_ptr<BandwidthOptimizer> bandwidth_optimizer;
        std::unique_ptr<NetworkMonitor> network_monitor;
        std::unique_ptr<SecurityGateway> security_gateway;
    };
    
    // Network capabilities
    enum class NetworkCapability {
        PROTOCOL_HANDLING,
        CONNECTION_MANAGEMENT,
        ROUTING,
        BANDWIDTH_OPTIMIZATION,
        NETWORK_MONITORING,
        SECURITY_GATEWAY,
        LOAD_BALANCING,
        TRAFFIC_SHAPING,
        QUALITY_OF_SERVICE,
        NETWORK_DISCOVERY,
        AUTO_CONFIGURATION,
        FAULT_TOLERANCE,
        SCALABILITY,
        INTEROPERABILITY,
        PERFORMANCE_OPTIMIZATION,
        RELIABILITY_ENSUREMENT
    };
    
    // Network context
    struct NetworkContext {
        std::string network_type;
        std::string protocol_stack;
        std::vector<std::string> supported_protocols;
        std::vector<NetworkCapability> required_capabilities;
        float bandwidth_limit;
        uint64_t connection_timeout;
        bool enable_auto_recovery;
        bool enable_encryption;
    };
    
    // Core components
    std::unique_ptr<NetworkEngine> network_engine;
    std::map<NetworkCapability, bool> capability_status;
    std::map<std::string, NetworkContext> context_cache;
    
    // Performance tracking
    struct NetworkMetrics {
        uint64_t connections_established;
        uint64_t packets_transmitted;
        uint64_t protocols_handled;
        uint64_t routing_decisions;
        float average_latency;
        float throughput_rate;
        std::map<NetworkCapability, uint64_t> capability_usage;
        std::vector<std::string> recent_network_events;
    };
    
    NetworkMetrics metrics;
    
public:
    NetworkAgent(uint32_t id) : BaseAgent(id, "NetworkAgent", AgentSpecialization::NETWORK_AGENT) {
        network_engine = std::make_unique<NetworkEngine>();
    }
    
    // Core agent functions
    KernelResult Initialize() override;
    KernelResult ExecuteTask(const std::vector<uint8_t>& task_data) override;
    void ProcessMessage(const AgentMessage& message) override;
    void LearnFromExperience(const std::vector<uint8_t>& experience_data) override;
    void AdaptToEnvironment(const std::vector<uint8_t>& environment_data) override;
    
    // Network capabilities
    KernelResult HandleProtocol(const ProtocolData& data, const NetworkContext& context);
    KernelResult ManageConnection(const ConnectionRequest& request, const NetworkContext& context);
    KernelResult RoutePacket(const PacketData& packet, const NetworkContext& context);
    KernelResult OptimizeBandwidth(const BandwidthRequest& request, const NetworkContext& context);
    KernelResult MonitorNetwork(const NetworkData& data, const NetworkContext& context);
    KernelResult SecureGateway(const SecurityRequest& request, const NetworkContext& context);
    
    // Network management
    KernelResult EnableCapability(NetworkCapability capability);
    KernelResult DisableCapability(NetworkCapability capability);
    bool IsCapabilityEnabled(NetworkCapability capability);
    std::vector<NetworkCapability> GetEnabledCapabilities();
    
    // Context management
    KernelResult SetNetworkContext(const std::string& context_id, const NetworkContext& context);
    KernelResult GetNetworkContext(const std::string& context_id, NetworkContext& context);
    KernelResult UpdateNetworkContext(const std::string& context_id, const std::map<std::string, std::string>& updates);
    
    // Performance monitoring
    NetworkMetrics GetMetrics() const;
    void ResetMetrics();
    void GenerateNetworkReport();
    
protected:
    // Internal network functions
    virtual void MainLoop() override;
    virtual void ProcessTask(const std::vector<uint8_t>& task_data) override;
    virtual void HandleMessage(const AgentMessage& message) override;
    virtual void PerformLearning() override;
    virtual void UpdateState() override;
    
private:
    // Network implementations
    KernelResult ExecuteProtocolHandling(const std::vector<uint8_t>& protocol_data);
    KernelResult ExecuteConnectionManagement(const std::vector<uint8_t>& connection_data);
    KernelResult ExecuteRouting(const std::vector<uint8_t>& routing_data);
    KernelResult ExecuteBandwidthOptimization(const std::vector<uint8_t>& bandwidth_data);
    KernelResult ExecuteNetworkMonitoring(const std::vector<uint8_t>& monitoring_data);
    
    // Network utility functions
    float CalculateNetworkPerformance(const std::vector<uint8_t>& performance_data);
    void AnalyzeNetworkTraffic(const std::vector<uint8_t>& traffic_data);
    void UpdateNetworkModel(const std::string& network_id, const std::vector<uint8_t>& network_data);
    void OptimizeNetworkStrategy(const std::vector<uint8_t>& strategy_data);
    
    // Utility functions
    NetworkContext SelectBestContext(const std::string& task_description);
    void LogNetworkOperation(const std::string& operation, const std::string& details);
};

// Forward declarations for network engine components
class ProtocolHandler;
class ConnectionManager;
class RoutingEngine;
class BandwidthOptimizer;
class NetworkMonitor;
class SecurityGateway;

// Network data structures
struct ProtocolData {
    std::string protocol_id;
    std::string protocol_type;
    std::vector<uint8_t> protocol_data;
    std::map<std::string, float> protocol_parameters;
    uint64_t timestamp;
    std::string source_address;
    std::string destination_address;
};

struct ConnectionRequest {
    std::string connection_id;
    std::string connection_type;
    std::string source_endpoint;
    std::string destination_endpoint;
    std::map<std::string, float> connection_parameters;
    uint64_t timeout;
    bool enable_encryption;
};

struct PacketData {
    std::string packet_id;
    std::vector<uint8_t> packet_payload;
    std::string source_address;
    std::string destination_address;
    std::map<std::string, float> packet_metadata;
    uint64_t timestamp;
    uint32_t priority;
};

struct BandwidthRequest {
    std::string request_id;
    std::string request_type;
    float bandwidth_requirement;
    std::map<std::string, float> optimization_parameters;
    uint64_t duration;
    float priority_level;
};

struct NetworkData {
    std::string network_id;
    std::string network_type;
    std::vector<uint8_t> network_data;
    std::map<std::string, float> network_metrics;
    std::vector<std::string> active_connections;
    uint64_t monitoring_time;
};

struct SecurityRequest {
    std::string request_id;
    std::string security_type;
    std::vector<uint8_t> security_data;
    std::map<std::string, float> security_parameters;
    std::vector<std::string> security_policies;
    float risk_level;
};

struct NetworkTopology {
    std::string topology_id;
    std::vector<std::string> nodes;
    std::vector<std::string> connections;
    std::map<std::string, float> link_capacities;
    std::map<std::string, float> node_capacities;
    uint64_t last_updated;
};

struct NetworkPolicy {
    std::string policy_id;
    std::string policy_type;
    std::map<std::string, std::string> policy_rules;
    std::vector<std::string> enforcement_actions;
    float compliance_level;
    uint64_t last_reviewed;
};

} // namespace AI
} // namespace AgenticOS