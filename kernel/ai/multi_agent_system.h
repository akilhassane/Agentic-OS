#pragma once

#include <cstdint>
#include <atomic>
#include <vector>
#include <memory>
#include <map>
#include <queue>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <functional>
#include <string>
#include "../common/kernel_types.h"

namespace AgenticOS {
namespace AI {

// Agent Specialization Types - covers all human capabilities
enum class AgentSpecialization : uint32_t {
    // Cognitive Agents
    REASONING_AGENT = 0x0001,
    PROBLEM_SOLVING_AGENT = 0x0002,
    CREATIVE_AGENT = 0x0003,
    LEARNING_AGENT = 0x0004,
    MEMORY_AGENT = 0x0005,
    PATTERN_RECOGNITION_AGENT = 0x0006,
    DECISION_MAKING_AGENT = 0x0007,
    PLANNING_AGENT = 0x0008,
    
    // Communication Agents
    LANGUAGE_AGENT = 0x0100,
    TRANSLATION_AGENT = 0x0101,
    SPEECH_AGENT = 0x0102,
    WRITING_AGENT = 0x0103,
    READING_AGENT = 0x0104,
    CONVERSATION_AGENT = 0x0105,
    EMOTION_AGENT = 0x0106,
    
    // Physical Interface Agents
    MOTOR_CONTROL_AGENT = 0x0200,
    MANIPULATION_AGENT = 0x0201,
    NAVIGATION_AGENT = 0x0202,
    COORDINATION_AGENT = 0x0203,
    FINE_MOTOR_AGENT = 0x0204,
    
    // Sensory Agents
    VISION_AGENT = 0x0300,
    AUDIO_AGENT = 0x0301,
    MULTIMODAL_AGENT = 0x0302,
    SENSOR_FUSION_AGENT = 0x0303,
    
    // Social Agents
    SOCIAL_INTERACTION_AGENT = 0x0400,
    EMPATHY_AGENT = 0x0401,
    CULTURAL_AGENT = 0x0402,
    RELATIONSHIP_AGENT = 0x0403,
    
    // Creative Agents
    ART_AGENT = 0x0500,
    MUSIC_AGENT = 0x0501,
    STORYTELLING_AGENT = 0x0502,
    DESIGN_AGENT = 0x0503,
    INNOVATION_AGENT = 0x0504,
    
    // Technical Agents
    PROGRAMMING_AGENT = 0x0600,
    SYSTEM_ADMIN_AGENT = 0x0601,
    DATA_ANALYSIS_AGENT = 0x0602,
    RESEARCH_AGENT = 0x0603,
    ENGINEERING_AGENT = 0x0604,
    
    // Business Agents
    PROJECT_MANAGEMENT_AGENT = 0x0700,
    FINANCIAL_AGENT = 0x0701,
    MARKETING_AGENT = 0x0702,
    SALES_AGENT = 0x0703,
    CUSTOMER_SERVICE_AGENT = 0x0704,
    
    // Personal Agents
    PERSONAL_ASSISTANT_AGENT = 0x0800,
    EDUCATION_AGENT = 0x0801,
    ENTERTAINMENT_AGENT = 0x0802,
    HEALTH_AGENT = 0x0803,
    LIFESTYLE_AGENT = 0x0804,
    
    // Meta Agents
    SELF_IMPROVEMENT_AGENT = 0x0900,
    CAPABILITY_LEARNING_AGENT = 0x0901,
    ADAPTATION_AGENT = 0x0902,
    EVOLUTION_AGENT = 0x0903,
    
    // Specialized Domain Agents
    MEDICAL_AGENT = 0x0A00,
    LEGAL_AGENT = 0x0A01,
    SCIENTIFIC_AGENT = 0x0A02,
    ASTRONOMY_AGENT = 0x0A03,
    CHEMISTRY_AGENT = 0x0A04,
    PHYSICS_AGENT = 0x0A05,
    BIOLOGY_AGENT = 0x0A06,
    MATHEMATICS_AGENT = 0x0A07,
    HISTORY_AGENT = 0x0A08,
    GEOGRAPHY_AGENT = 0x0A09,
    LITERATURE_AGENT = 0x0A0A,
    PHILOSOPHY_AGENT = 0x0A0B,
    PSYCHOLOGY_AGENT = 0x0A0C,
    SOCIOLOGY_AGENT = 0x0A0D,
    ECONOMICS_AGENT = 0x0A0E,
    POLITICAL_AGENT = 0x0A0F,
    
    // Industry-Specific Agents
    MANUFACTURING_AGENT = 0x0B00,
    AGRICULTURE_AGENT = 0x0B01,
    CONSTRUCTION_AGENT = 0x0B02,
    TRANSPORTATION_AGENT = 0x0B03,
    ENERGY_AGENT = 0x0B04,
    TELECOMMUNICATIONS_AGENT = 0x0B05,
    FINANCIAL_SERVICES_AGENT = 0x0B06,
    HEALTHCARE_AGENT = 0x0B07,
    EDUCATION_SECTOR_AGENT = 0x0B08,
    ENTERTAINMENT_INDUSTRY_AGENT = 0x0B09,
    RETAIL_AGENT = 0x0B0A,
    HOSPITALITY_AGENT = 0x0B0B,
    REAL_ESTATE_AGENT = 0x0B0C,
    INSURANCE_AGENT = 0x0B0D,
    LEGAL_SERVICES_AGENT = 0x0B0E,
    
    // Specialized Task Agents
    WEB_BROWSING_AGENT = 0x0C00,
    EMAIL_AGENT = 0x0C01,
    CALENDAR_AGENT = 0x0C02,
    FILE_MANAGEMENT_AGENT = 0x0C03,
    NETWORK_AGENT = 0x0C04,
    SECURITY_AGENT = 0x0C05,
    BACKUP_AGENT = 0x0C06,
    UPDATE_AGENT = 0x0C07,
    MONITORING_AGENT = 0x0C08,
    OPTIMIZATION_AGENT = 0x0C09,
    
    // Integration Agents
    API_INTEGRATION_AGENT = 0x0D00,
    DATABASE_AGENT = 0x0D01,
    CLOUD_SERVICES_AGENT = 0x0D02,
    IOT_AGENT = 0x0D03,
    ROBOTICS_AGENT = 0x0D04,
    AUTOMATION_AGENT = 0x0D05,
    WORKFLOW_AGENT = 0x0D06,
    ORCHESTRATION_AGENT = 0x0D07,
    
    // Quality Assurance Agents
    TESTING_AGENT = 0x0E00,
    VALIDATION_AGENT = 0x0E01,
    VERIFICATION_AGENT = 0x0E02,
    QUALITY_CONTROL_AGENT = 0x0E03,
    COMPLIANCE_AGENT = 0x0E04,
    AUDIT_AGENT = 0x0E05,
    
    // Emergency and Safety Agents
    EMERGENCY_AGENT = 0x0F00,
    SAFETY_AGENT = 0x0F01,
    CRISIS_MANAGEMENT_AGENT = 0x0F02,
    RECOVERY_AGENT = 0x0F03,
    DIAGNOSTIC_AGENT = 0x0F04,
    
    // Unknown/Custom
    UNKNOWN_AGENT = 0xFFFF,
    CUSTOM_AGENT = 0xFFFE
};

// Agent State
enum class AgentState : uint8_t {
    IDLE = 0,
    ACTIVE = 1,
    BUSY = 2,
    LEARNING = 3,
    EVOLVING = 4,
    ERROR = 5,
    RECOVERING = 6,
    TERMINATED = 7
};

// Agent Priority Levels
enum class AgentPriority : uint8_t {
    CRITICAL = 0,
    HIGH = 1,
    NORMAL = 2,
    LOW = 3,
    BACKGROUND = 4
};

// Agent Communication Protocol
struct AgentMessage {
    uint64_t message_id;
    uint32_t sender_agent_id;
    uint32_t receiver_agent_id;
    std::string message_type;
    std::vector<uint8_t> payload;
    uint64_t timestamp;
    AgentPriority priority;
    bool requires_response;
    uint64_t response_timeout;
};

// Agent Capability Definition
struct AgentCapability {
    uint32_t capability_id;
    std::string name;
    std::string description;
    std::vector<AgentSpecialization> specializations;
    std::vector<std::string> supported_operations;
    std::vector<std::string> required_resources;
    float success_rate;
    uint64_t execution_count;
    uint64_t average_execution_time;
    bool is_evolving;
    std::vector<uint8_t> implementation_data;
};

// Agent Performance Metrics
struct AgentMetrics {
    uint32_t agent_id;
    uint64_t tasks_completed;
    uint64_t tasks_failed;
    float success_rate;
    uint64_t total_execution_time;
    uint64_t average_response_time;
    uint64_t memory_usage;
    float cpu_usage;
    uint64_t network_usage;
    uint64_t learning_iterations;
    float adaptation_score;
    std::vector<std::string> recent_activities;
};

// Base Agent Class - all agents inherit from this
class BaseAgent {
protected:
    uint32_t agent_id;
    std::string agent_name;
    AgentSpecialization specialization;
    AgentState current_state;
    AgentPriority priority;
    
    // Capabilities
    std::vector<AgentCapability> capabilities;
    std::map<std::string, std::function<KernelResult(const std::vector<uint8_t>&)>> operations;
    
    // Communication
    std::queue<AgentMessage> message_queue;
    std::mutex message_mutex;
    std::condition_variable message_cv;
    
    // Performance tracking
    AgentMetrics metrics;
    std::atomic<uint64_t> tasks_executed;
    std::atomic<uint64_t> tasks_succeeded;
    
    // Learning and adaptation
    std::atomic<bool> learning_enabled;
    std::atomic<uint64_t> learning_iterations;
    std::vector<uint8_t> knowledge_base;
    
    // Threading
    std::thread agent_thread;
    std::atomic<bool> running;
    std::mutex state_mutex;
    
public:
    BaseAgent(uint32_t id, const std::string& name, AgentSpecialization spec) :
        agent_id(id),
        agent_name(name),
        specialization(spec),
        current_state(AgentState::IDLE),
        priority(AgentPriority::NORMAL),
        tasks_executed(0),
        tasks_succeeded(0),
        learning_enabled(true),
        learning_iterations(0),
        running(false) {}
    
    virtual ~BaseAgent() {
        Stop();
    }
    
    // Core agent functions
    virtual KernelResult Initialize() = 0;
    virtual KernelResult ExecuteTask(const std::vector<uint8_t>& task_data) = 0;
    virtual void ProcessMessage(const AgentMessage& message) = 0;
    virtual void LearnFromExperience(const std::vector<uint8_t>& experience_data) = 0;
    virtual void AdaptToEnvironment(const std::vector<uint8_t>& environment_data) = 0;
    
    // Agent lifecycle
    KernelResult Start();
    void Stop();
    void Pause();
    void Resume();
    
    // Communication
    KernelResult SendMessage(const AgentMessage& message);
    std::vector<AgentMessage> GetPendingMessages();
    void BroadcastMessage(const std::string& message_type, const std::vector<uint8_t>& payload);
    
    // Capability management
    KernelResult AddCapability(const AgentCapability& capability);
    KernelResult RemoveCapability(uint32_t capability_id);
    std::vector<AgentCapability> GetCapabilities() const;
    bool HasCapability(const std::string& capability_name) const;
    
    // Performance monitoring
    AgentMetrics GetMetrics() const;
    void UpdateMetrics();
    void ResetMetrics();
    
    // Learning and evolution
    void EnableLearning(bool enable);
    void SetLearningRate(float rate);
    void EvolveCapabilities();
    void ShareKnowledge(const std::vector<uint8_t>& knowledge);
    
    // Getters
    uint32_t GetAgentID() const { return agent_id; }
    std::string GetAgentName() const { return agent_name; }
    AgentSpecialization GetSpecialization() const { return specialization; }
    AgentState GetState() const { return current_state; }
    AgentPriority GetPriority() const { return priority; }
    
    // Setters
    void SetPriority(AgentPriority new_priority) { priority = new_priority; }
    void SetState(AgentState new_state);
    
protected:
    // Internal helper functions
    virtual void MainLoop();
    virtual void ProcessTask(const std::vector<uint8_t>& task_data);
    virtual void HandleMessage(const AgentMessage& message);
    virtual void PerformLearning();
    virtual void UpdateState();
    
    // Utility functions
    uint64_t GetCurrentTimeUS();
    void LogInfo(const std::string& message);
    void LogError(const std::string& message);
    void LogWarning(const std::string& message);
    
private:
    void InitializeMetrics();
    void UpdatePerformanceMetrics();
};

// Multi-Agent Coordinator - manages all agents
class MultiAgentCoordinator {
private:
    // Agent registry
    std::map<uint32_t, std::unique_ptr<BaseAgent>> agents;
    std::map<AgentSpecialization, std::vector<uint32_t>> specialization_map;
    std::mutex agent_registry_mutex;
    
    // Task distribution
    struct TaskAssignment {
        uint64_t task_id;
        std::vector<uint32_t> assigned_agents;
        std::vector<uint32_t> required_capabilities;
        TaskExecutionState state;
        float progress;
        uint64_t deadline;
        std::vector<uint8_t> result;
    };
    
    std::map<uint64_t, TaskAssignment> active_tasks;
    std::queue<uint64_t> task_queue;
    std::mutex task_mutex;
    
    // Communication hub
    std::map<uint32_t, std::queue<AgentMessage>> message_hubs;
    std::mutex message_mutex;
    
    // Coordination algorithms
    std::unique_ptr<TaskPlanner> task_planner;
    std::unique_ptr<ResourceManager> resource_manager;
    std::unique_ptr<LoadBalancer> load_balancer;
    std::unique_ptr<ConflictResolver> conflict_resolver;
    
    // Performance monitoring
    struct CoordinatorMetrics {
        uint64_t total_agents;
        uint64_t active_agents;
        uint64_t total_tasks;
        uint64_t completed_tasks;
        float overall_success_rate;
        uint64_t total_messages;
        float system_efficiency;
        std::vector<std::string> bottlenecks;
    };
    
    CoordinatorMetrics metrics;
    std::atomic<bool> running;
    std::thread coordinator_thread;
    
public:
    MultiAgentCoordinator() : running(false) {
        task_planner = std::make_unique<TaskPlanner>();
        resource_manager = std::make_unique<ResourceManager>();
        load_balancer = std::make_unique<LoadBalancer>();
        conflict_resolver = std::make_unique<ConflictResolver>();
    }
    
    // Agent management
    KernelResult RegisterAgent(std::unique_ptr<BaseAgent> agent);
    KernelResult UnregisterAgent(uint32_t agent_id);
    KernelResult StartAgent(uint32_t agent_id);
    KernelResult StopAgent(uint32_t agent_id);
    KernelResult PauseAgent(uint32_t agent_id);
    KernelResult ResumeAgent(uint32_t agent_id);
    
    // Task management
    uint64_t SubmitTask(const std::string& task_description,
                       const std::vector<uint8_t>& task_data,
                       const std::vector<AgentSpecialization>& required_specializations);
    KernelResult CancelTask(uint64_t task_id);
    TaskExecutionState GetTaskStatus(uint64_t task_id);
    std::vector<uint8_t> GetTaskResult(uint64_t task_id);
    
    // Agent discovery and selection
    std::vector<uint32_t> FindAgentsBySpecialization(AgentSpecialization spec);
    std::vector<uint32_t> FindAgentsByCapability(const std::string& capability);
    std::vector<uint32_t> FindAvailableAgents();
    uint32_t SelectBestAgent(const std::vector<uint32_t>& candidates, const std::vector<uint8_t>& task_data);
    
    // Communication routing
    KernelResult RouteMessage(const AgentMessage& message);
    std::vector<AgentMessage> GetMessagesForAgent(uint32_t agent_id);
    void BroadcastToAllAgents(const std::string& message_type, const std::vector<uint8_t>& payload);
    void BroadcastToSpecialization(AgentSpecialization spec, const std::string& message_type, const std::vector<uint8_t>& payload);
    
    // System management
    KernelResult Start();
    void Stop();
    void Pause();
    void Resume();
    
    // Monitoring and statistics
    CoordinatorMetrics GetMetrics() const;
    std::vector<AgentMetrics> GetAllAgentMetrics() const;
    void GenerateSystemReport();
    void OptimizeSystemPerformance();
    
    // Advanced features
    void EnableAutoScaling(bool enable);
    void SetLoadBalancingStrategy(const std::string& strategy);
    void EnableConflictResolution(bool enable);
    void SetTaskPrioritization(const std::string& strategy);
    
private:
    // Internal coordination functions
    void MainCoordinationLoop();
    void ProcessTaskQueue();
    void DistributeTasks();
    void MonitorAgentHealth();
    void ResolveConflicts();
    void OptimizeResourceUsage();
    void HandleAgentFailures();
    
    // Helper functions
    std::vector<uint32_t> SelectAgentsForTask(const std::vector<AgentSpecialization>& specs);
    void UpdateTaskProgress(uint64_t task_id, float progress);
    void HandleTaskCompletion(uint64_t task_id, const std::vector<uint8_t>& result);
    void HandleTaskFailure(uint64_t task_id, const std::string& error);
    
    // Performance optimization
    void RebalanceLoad();
    void OptimizeAgentPlacement();
    void UpdateSpecializationMap();
    void CleanupCompletedTasks();
};

// Task Planner - determines how to break down complex tasks
class TaskPlanner {
private:
    struct TaskBreakdown {
        uint64_t task_id;
        std::vector<uint64_t> subtasks;
        std::map<uint64_t, std::vector<uint32_t>> agent_assignments;
        std::map<uint64_t, uint64_t> dependencies;
        std::map<uint64_t, float> estimated_duration;
        std::map<uint64_t, AgentPriority> priorities;
    };
    
    std::map<uint64_t, TaskBreakdown> task_breakdowns;
    std::mutex planner_mutex;
    
public:
    TaskBreakdown PlanTask(const std::string& task_description,
                          const std::vector<uint8_t>& task_data,
                          const std::vector<AgentSpecialization>& available_specializations);
    
    void OptimizePlan(TaskBreakdown& breakdown);
    float EstimateTaskDuration(const TaskBreakdown& breakdown);
    std::vector<uint64_t> GetCriticalPath(const TaskBreakdown& breakdown);
    void ValidatePlan(const TaskBreakdown& breakdown);
};

// Resource Manager - manages system resources for agents
class ResourceManager {
private:
    struct ResourceAllocation {
        uint32_t agent_id;
        uint64_t memory_limit;
        uint64_t cpu_limit;
        uint64_t network_limit;
        uint64_t storage_limit;
        std::vector<std::string> special_resources;
    };
    
    std::map<uint32_t, ResourceAllocation> allocations;
    std::mutex resource_mutex;
    
public:
    KernelResult AllocateResources(uint32_t agent_id, const ResourceAllocation& allocation);
    KernelResult DeallocateResources(uint32_t agent_id);
    ResourceAllocation GetAgentResources(uint32_t agent_id);
    bool CheckResourceAvailability(const ResourceAllocation& required);
    void OptimizeResourceUsage();
};

// Load Balancer - distributes work across agents
class LoadBalancer {
private:
    enum class BalancingStrategy {
        ROUND_ROBIN,
        LEAST_LOADED,
        CAPABILITY_BASED,
        PERFORMANCE_BASED,
        ADAPTIVE
    };
    
    BalancingStrategy current_strategy;
    std::map<uint32_t, float> agent_loads;
    std::mutex load_mutex;
    
public:
    uint32_t SelectAgent(const std::vector<uint32_t>& candidates, const std::vector<uint8_t>& task_data);
    void UpdateAgentLoad(uint32_t agent_id, float load);
    void SetBalancingStrategy(BalancingStrategy strategy);
    void OptimizeDistribution();
};

// Conflict Resolver - handles conflicts between agents
class ConflictResolver {
private:
    struct Conflict {
        uint64_t conflict_id;
        std::vector<uint32_t> involved_agents;
        std::string conflict_type;
        std::string description;
        uint64_t timestamp;
        ConflictResolutionState state;
    };
    
    std::vector<Conflict> active_conflicts;
    std::mutex conflict_mutex;
    
public:
    uint64_t RegisterConflict(const std::vector<uint32_t>& agents, const std::string& type, const std::string& description);
    KernelResult ResolveConflict(uint64_t conflict_id, const std::string& resolution);
    std::vector<Conflict> GetActiveConflicts();
    void AutoResolveConflicts();
};

// Global multi-agent coordinator instance
extern MultiAgentCoordinator* g_multi_agent_coordinator;

} // namespace AI
} // namespace AgenticOS