#pragma once

#include "../multi_agent_system.h"
#include "../agent_wire_protocol.h"
#include <memory>
#include <vector>
#include <map>

namespace AgenticOS {
namespace AI {

// Memory Agent - Handles memory management, caching, and data persistence
class MemoryAgent : public BaseAgent {
private:
    // Memory components
    struct MemoryEngine {
        std::unique_ptr<MemoryAllocator> memory_allocator;
        std::unique_ptr<CacheManager> cache_manager;
        std::unique_ptr<GarbageCollector> garbage_collector;
        std::unique_ptr<DataPersistence> data_persistence;
        std::unique_ptr<MemoryOptimizer> memory_optimizer;
        std::unique_ptr<MemoryMonitor> memory_monitor;
    };
    
    // Memory capabilities
    enum class MemoryCapability {
        MEMORY_ALLOCATION,
        CACHE_MANAGEMENT,
        GARBAGE_COLLECTION,
        DATA_PERSISTENCE,
        MEMORY_OPTIMIZATION,
        MEMORY_MONITORING,
        MEMORY_PROTECTION,
        VIRTUAL_MEMORY,
        SHARED_MEMORY,
        DISTRIBUTED_MEMORY,
        MEMORY_COMPRESSION,
        MEMORY_DEDUPLICATION,
        MEMORY_MIGRATION,
        MEMORY_BACKUP,
        MEMORY_RECOVERY,
        MEMORY_ANALYTICS
    };
    
    // Memory context
    struct MemoryContext {
        std::string memory_type;
        uint64_t memory_size;
        std::vector<std::string> memory_policies;
        std::vector<MemoryCapability> required_capabilities;
        float memory_threshold;
        uint64_t cleanup_interval;
        bool enable_compression;
        bool enable_backup;
    };
    
    // Core components
    std::unique_ptr<MemoryEngine> memory_engine;
    std::map<MemoryCapability, bool> capability_status;
    std::map<std::string, MemoryContext> context_cache;
    
    // Performance tracking
    struct MemoryMetrics {
        uint64_t allocations_performed;
        uint64_t cache_hits;
        uint64_t garbage_collections;
        uint64_t data_persistences;
        float memory_utilization;
        float cache_efficiency;
        std::map<MemoryCapability, uint64_t> capability_usage;
        std::vector<std::string> recent_memory_events;
    };
    
    MemoryMetrics metrics;
    
public:
    MemoryAgent(uint32_t id) : BaseAgent(id, "MemoryAgent", AgentSpecialization::MEMORY_AGENT) {
        memory_engine = std::make_unique<MemoryEngine>();
    }
    
    // Core agent functions
    KernelResult Initialize() override;
    KernelResult ExecuteTask(const std::vector<uint8_t>& task_data) override;
    void ProcessMessage(const AgentMessage& message) override;
    void LearnFromExperience(const std::vector<uint8_t>& experience_data) override;
    void AdaptToEnvironment(const std::vector<uint8_t>& environment_data) override;
    
    // Memory capabilities
    KernelResult AllocateMemory(const MemoryRequest& request, const MemoryContext& context);
    KernelResult ManageCache(const CacheRequest& request, const MemoryContext& context);
    KernelResult CollectGarbage(const GarbageCollectionRequest& request, const MemoryContext& context);
    KernelResult PersistData(const PersistenceRequest& request, const MemoryContext& context);
    KernelResult OptimizeMemory(const OptimizationRequest& request, const MemoryContext& context);
    KernelResult MonitorMemory(const MonitoringRequest& request, const MemoryContext& context);
    
    // Memory management
    KernelResult EnableCapability(MemoryCapability capability);
    KernelResult DisableCapability(MemoryCapability capability);
    bool IsCapabilityEnabled(MemoryCapability capability);
    std::vector<MemoryCapability> GetEnabledCapabilities();
    
    // Context management
    KernelResult SetMemoryContext(const std::string& context_id, const MemoryContext& context);
    KernelResult GetMemoryContext(const std::string& context_id, MemoryContext& context);
    KernelResult UpdateMemoryContext(const std::string& context_id, const std::map<std::string, std::string>& updates);
    
    // Performance monitoring
    MemoryMetrics GetMetrics() const;
    void ResetMetrics();
    void GenerateMemoryReport();
    
protected:
    // Internal memory functions
    virtual void MainLoop() override;
    virtual void ProcessTask(const std::vector<uint8_t>& task_data) override;
    virtual void HandleMessage(const AgentMessage& message) override;
    virtual void PerformLearning() override;
    virtual void UpdateState() override;
    
private:
    // Memory implementations
    KernelResult ExecuteMemoryAllocation(const std::vector<uint8_t>& allocation_data);
    KernelResult ExecuteCacheManagement(const std::vector<uint8_t>& cache_data);
    KernelResult ExecuteGarbageCollection(const std::vector<uint8_t>& gc_data);
    KernelResult ExecuteDataPersistence(const std::vector<uint8_t>& persistence_data);
    KernelResult ExecuteMemoryOptimization(const std::vector<uint8_t>& optimization_data);
    
    // Memory utility functions
    float CalculateMemoryEfficiency(const std::vector<uint8_t>& memory_data);
    void AnalyzeMemoryUsage(const std::vector<uint8_t>& usage_data);
    void UpdateMemoryModel(const std::string& memory_id, const std::vector<uint8_t>& memory_data);
    void OptimizeMemoryStrategy(const std::vector<uint8_t>& strategy_data);
    
    // Utility functions
    MemoryContext SelectBestContext(const std::string& task_description);
    void LogMemoryOperation(const std::string& operation, const std::string& details);
};

// Forward declarations for memory engine components
class MemoryAllocator;
class CacheManager;
class GarbageCollector;
class DataPersistence;
class MemoryOptimizer;
class MemoryMonitor;

// Memory data structures
struct MemoryRequest {
    std::string request_id;
    uint64_t size_required;
    std::string memory_type;
    std::map<std::string, float> allocation_parameters;
    uint64_t priority;
    bool enable_compression;
};

struct CacheRequest {
    std::string cache_id;
    std::string cache_type;
    std::vector<uint8_t> data_to_cache;
    std::map<std::string, float> cache_parameters;
    uint64_t expiration_time;
    float priority_level;
};

struct GarbageCollectionRequest {
    std::string gc_id;
    std::string gc_type;
    std::vector<std::string> memory_regions;
    std::map<std::string, float> gc_parameters;
    uint64_t timeout;
    bool enable_compaction;
};

struct PersistenceRequest {
    std::string persistence_id;
    std::string storage_type;
    std::vector<uint8_t> data_to_persist;
    std::map<std::string, float> persistence_parameters;
    std::string storage_location;
    bool enable_encryption;
};

struct OptimizationRequest {
    std::string optimization_id;
    std::string optimization_type;
    std::vector<std::string> target_memory_regions;
    std::map<std::string, float> optimization_parameters;
    float target_efficiency;
    uint64_t timeout;
};

struct MonitoringRequest {
    std::string monitoring_id;
    std::string monitoring_type;
    std::vector<std::string> memory_metrics;
    std::map<std::string, float> monitoring_parameters;
    uint64_t monitoring_interval;
    bool enable_alerts;
};

struct MemoryRegion {
    std::string region_id;
    uint64_t start_address;
    uint64_t size;
    std::string region_type;
    std::map<std::string, float> region_metadata;
    bool is_allocated;
    uint64_t last_accessed;
};

struct MemoryPolicy {
    std::string policy_id;
    std::string policy_type;
    std::map<std::string, std::string> policy_rules;
    std::vector<std::string> enforcement_actions;
    float compliance_level;
    uint64_t last_reviewed;
};

} // namespace AI
} // namespace AgenticOS