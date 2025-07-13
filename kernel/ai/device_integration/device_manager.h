#pragma once

#include "../multi_agent_system.h"
#include "../agent_wire_protocol.h"
#include <memory>
#include <vector>
#include <map>

namespace AgenticOS {
namespace AI {

// Device Manager - Handles hardware integration, device communication, and peripheral management
class DeviceManager {
private:
    // Device integration components
    struct DeviceEngine {
        std::unique_ptr<HardwareInterface> hardware_interface;
        std::unique_ptr<DeviceCommunicator> device_communicator;
        std::unique_ptr<PeripheralManager> peripheral_manager;
        std::unique_ptr<DriverManager> driver_manager;
        std::unique_ptr<DeviceMonitor> device_monitor;
        std::unique_ptr<DeviceOptimizer> device_optimizer;
    };
    
    // Device capabilities
    enum class DeviceCapability {
        HARDWARE_INTERFACE,
        DEVICE_COMMUNICATION,
        PERIPHERAL_MANAGEMENT,
        DRIVER_MANAGEMENT,
        DEVICE_MONITORING,
        DEVICE_OPTIMIZATION,
        PLUG_AND_PLAY,
        HOT_SWAPPING,
        DEVICE_DISCOVERY,
        DEVICE_CONFIGURATION,
        DEVICE_MAINTENANCE,
        DEVICE_SECURITY,
        DEVICE_BACKUP,
        DEVICE_RECOVERY,
        DEVICE_ANALYTICS,
        DEVICE_LEARNING
    };
    
    // Device context
    struct DeviceContext {
        std::string device_type;
        std::string device_protocol;
        std::vector<std::string> supported_devices;
        std::vector<DeviceCapability> required_capabilities;
        float performance_threshold;
        uint64_t communication_timeout;
        bool enable_auto_configuration;
        bool enable_auto_recovery;
    };
    
    // Core components
    std::unique_ptr<DeviceEngine> device_engine;
    std::map<DeviceCapability, bool> capability_status;
    std::map<std::string, DeviceContext> context_cache;
    
    // Performance tracking
    struct DeviceMetrics {
        uint64_t devices_managed;
        uint64_t communications_handled;
        uint64_t peripherals_configured;
        uint64_t drivers_loaded;
        float average_response_time;
        float device_reliability;
        std::map<DeviceCapability, uint64_t> capability_usage;
        std::vector<std::string> recent_device_events;
    };
    
    DeviceMetrics metrics;
    
public:
    DeviceManager() {
        device_engine = std::make_unique<DeviceEngine>();
    }
    
    // Core device functions
    KernelResult Initialize();
    KernelResult RegisterDevice(const DeviceInfo& device, const DeviceContext& context);
    KernelResult CommunicateWithDevice(const DeviceCommunication& communication, DeviceResponse& response);
    KernelResult ConfigurePeripheral(const PeripheralConfig& config, const DeviceContext& context);
    KernelResult LoadDriver(const DriverRequest& request, DriverResult& result);
    KernelResult MonitorDevice(const DeviceMonitoring& monitoring, DeviceStatus& status);
    
    // Device management
    KernelResult EnableCapability(DeviceCapability capability);
    KernelResult DisableCapability(DeviceCapability capability);
    bool IsCapabilityEnabled(DeviceCapability capability);
    std::vector<DeviceCapability> GetEnabledCapabilities();
    
    // Context management
    KernelResult SetDeviceContext(const std::string& context_id, const DeviceContext& context);
    KernelResult GetDeviceContext(const std::string& context_id, DeviceContext& context);
    KernelResult UpdateDeviceContext(const std::string& context_id, const std::map<std::string, std::string>& updates);
    
    // Performance monitoring
    DeviceMetrics GetMetrics() const;
    void ResetMetrics();
    void GenerateDeviceReport();
    
private:
    // Device implementations
    KernelResult ExecuteDeviceRegistration(const std::vector<uint8_t>& device_data);
    KernelResult ExecuteDeviceCommunication(const std::vector<uint8_t>& communication_data);
    KernelResult ExecutePeripheralConfiguration(const std::vector<uint8_t>& config_data);
    KernelResult ExecuteDriverLoading(const std::vector<uint8_t>& driver_data);
    KernelResult ExecuteDeviceMonitoring(const std::vector<uint8_t>& monitoring_data);
    
    // Device utility functions
    float CalculateDevicePerformance(const std::vector<uint8_t>& device_data);
    void AnalyzeDevicePatterns(const std::vector<uint8_t>& pattern_data);
    void UpdateDeviceModel(const std::string& device_id, const std::vector<uint8_t>& device_data);
    void OptimizeDeviceStrategy(const std::vector<uint8_t>& strategy_data);
    
    // Utility functions
    DeviceContext SelectBestContext(const std::string& task_description);
    void LogDeviceOperation(const std::string& operation, const std::string& details);
};

// Forward declarations for device engine components
class HardwareInterface;
class DeviceCommunicator;
class PeripheralManager;
class DriverManager;
class DeviceMonitor;
class DeviceOptimizer;

// Device data structures
struct DeviceInfo {
    std::string device_id;
    std::string device_type;
    std::string device_name;
    std::string device_protocol;
    std::map<std::string, float> device_parameters;
    std::vector<std::string> device_capabilities;
    float device_version;
    uint64_t registration_time;
};

struct DeviceCommunication {
    std::string communication_id;
    std::string device_id;
    std::string communication_type;
    std::vector<uint8_t> communication_data;
    std::map<std::string, float> communication_parameters;
    uint64_t timeout;
    float priority;
};

struct DeviceResponse {
    std::string response_id;
    std::string communication_id;
    std::vector<uint8_t> response_data;
    std::map<std::string, float> response_metrics;
    bool success;
    std::string error_message;
    uint64_t response_time;
};

struct PeripheralConfig {
    std::string config_id;
    std::string peripheral_id;
    std::string config_type;
    std::map<std::string, std::string> config_parameters;
    std::vector<std::string> config_options;
    uint64_t timeout;
    bool enable_auto_configuration;
};

struct DriverRequest {
    std::string request_id;
    std::string device_id;
    std::string driver_type;
    std::vector<uint8_t> driver_data;
    std::map<std::string, float> driver_parameters;
    uint64_t timeout;
    bool enable_auto_installation;
};

struct DriverResult {
    std::string result_id;
    std::string request_id;
    bool success;
    std::vector<uint8_t> driver_data;
    std::map<std::string, float> driver_metrics;
    std::string error_message;
    uint64_t installation_time;
};

struct DeviceMonitoring {
    std::string monitoring_id;
    std::string device_id;
    std::string monitoring_type;
    std::vector<std::string> monitoring_metrics;
    std::map<std::string, float> monitoring_parameters;
    uint64_t monitoring_interval;
    bool enable_alerts;
};

struct DeviceStatus {
    std::string status_id;
    std::string device_id;
    std::string status_type;
    std::map<std::string, float> status_metrics;
    bool is_operational;
    std::string health_status;
    uint64_t last_updated;
};

struct HardwareInterface {
    std::string interface_id;
    std::string interface_type;
    std::vector<std::string> supported_protocols;
    std::map<std::string, float> interface_parameters;
    float interface_speed;
    uint64_t last_accessed;
};

struct DeviceDriver {
    std::string driver_id;
    std::string device_type;
    std::string driver_version;
    std::vector<uint8_t> driver_binary;
    std::map<std::string, float> driver_parameters;
    float compatibility_score;
    uint64_t last_updated;
};

} // namespace AI
} // namespace AgenticOS