#pragma once

#include "../multi_agent_system.h"
#include "../agent_wire_protocol.h"
#include <memory>
#include <vector>
#include <map>
#include <queue>

namespace AgenticOS {
namespace AI {

// Task Planning Engine - Handles task decomposition, planning, and execution orchestration
class TaskPlanningEngine {
private:
    // Planning components
    struct PlanningEngine {
        std::unique_ptr<TaskDecomposer> task_decomposer;
        std::unique_ptr<Planner> planner;
        std::unique_ptr<ExecutionOrchestrator> execution_orchestrator;
        std::unique_ptr<ResourceAllocator> resource_allocator;
        std::unique_ptr<ConstraintSolver> constraint_solver;
        std::unique_ptr<Optimizer> optimizer;
    };
    
    // Planning capabilities
    enum class PlanningCapability {
        TASK_DECOMPOSITION,
        PLANNING,
        EXECUTION_ORCHESTRATION,
        RESOURCE_ALLOCATION,
        CONSTRAINT_SOLVING,
        OPTIMIZATION,
        SCHEDULING,
        PRIORITIZATION,
        DEPENDENCY_RESOLUTION,
        PARALLEL_EXECUTION,
        ERROR_RECOVERY,
        ADAPTIVE_PLANNING,
        LEARNING_PLANNING,
        COLLABORATIVE_PLANNING,
        DISTRIBUTED_PLANNING,
        REAL_TIME_PLANNING
    };
    
    // Planning context
    struct PlanningContext {
        std::string planning_domain;
        std::string planning_strategy;
        std::vector<std::string> available_resources;
        std::vector<PlanningCapability> required_capabilities;
        float optimization_level;
        uint64_t planning_timeout;
        bool enable_adaptive_planning;
        bool enable_learning;
    };
    
    // Core components
    std::unique_ptr<PlanningEngine> planning_engine;
    std::map<PlanningCapability, bool> capability_status;
    std::map<std::string, PlanningContext> context_cache;
    
    // Performance tracking
    struct PlanningMetrics {
        uint64_t tasks_planned;
        uint64_t plans_executed;
        uint64_t optimizations_performed;
        uint64_t constraints_resolved;
        float average_planning_time;
        float plan_execution_success_rate;
        std::map<PlanningCapability, uint64_t> capability_usage;
        std::vector<std::string> recent_planning_events;
    };
    
    PlanningMetrics metrics;
    
public:
    TaskPlanningEngine() {
        planning_engine = std::make_unique<PlanningEngine>();
    }
    
    // Core planning functions
    KernelResult Initialize();
    KernelResult DecomposeTask(const Task& task, std::vector<SubTask>& subtasks);
    KernelResult CreatePlan(const std::vector<SubTask>& subtasks, Plan& plan);
    KernelResult ExecutePlan(const Plan& plan, ExecutionResult& result);
    KernelResult OptimizePlan(const Plan& plan, Plan& optimized_plan);
    KernelResult AllocateResources(const ResourceRequest& request, ResourceAllocation& allocation);
    
    // Planning management
    KernelResult EnableCapability(PlanningCapability capability);
    KernelResult DisableCapability(PlanningCapability capability);
    bool IsCapabilityEnabled(PlanningCapability capability);
    std::vector<PlanningCapability> GetEnabledCapabilities();
    
    // Context management
    KernelResult SetPlanningContext(const std::string& context_id, const PlanningContext& context);
    KernelResult GetPlanningContext(const std::string& context_id, PlanningContext& context);
    KernelResult UpdatePlanningContext(const std::string& context_id, const std::map<std::string, std::string>& updates);
    
    // Performance monitoring
    PlanningMetrics GetMetrics() const;
    void ResetMetrics();
    void GeneratePlanningReport();
    
private:
    // Planning implementations
    KernelResult ExecuteTaskDecomposition(const std::vector<uint8_t>& task_data);
    KernelResult ExecutePlanning(const std::vector<uint8_t>& planning_data);
    KernelResult ExecuteOrchestration(const std::vector<uint8_t>& orchestration_data);
    KernelResult ExecuteResourceAllocation(const std::vector<uint8_t>& allocation_data);
    KernelResult ExecuteConstraintSolving(const std::vector<uint8_t>& constraint_data);
    
    // Planning utility functions
    float CalculatePlanQuality(const std::vector<uint8_t>& plan_data);
    void AnalyzePlanningPatterns(const std::vector<uint8_t>& pattern_data);
    void UpdatePlanningModel(const std::string& plan_id, const std::vector<uint8_t>& plan_data);
    void OptimizePlanningStrategy(const std::vector<uint8_t>& strategy_data);
    
    // Utility functions
    PlanningContext SelectBestContext(const std::string& task_description);
    void LogPlanningOperation(const std::string& operation, const std::string& details);
};

// Forward declarations for planning engine components
class TaskDecomposer;
class Planner;
class ExecutionOrchestrator;
class ResourceAllocator;
class ConstraintSolver;
class Optimizer;

// Planning data structures
struct Task {
    std::string task_id;
    std::string task_description;
    std::string task_type;
    std::vector<std::string> task_requirements;
    std::map<std::string, float> task_parameters;
    float priority;
    uint64_t deadline;
    std::vector<std::string> dependencies;
};

struct SubTask {
    std::string subtask_id;
    std::string parent_task_id;
    std::string subtask_description;
    std::string subtask_type;
    std::vector<std::string> subtask_requirements;
    std::map<std::string, float> subtask_parameters;
    float priority;
    uint64_t estimated_duration;
    std::vector<std::string> dependencies;
};

struct Plan {
    std::string plan_id;
    std::vector<PlanStep> steps;
    std::map<std::string, float> plan_metrics;
    float plan_quality;
    uint64_t estimated_execution_time;
    std::vector<std::string> required_resources;
    std::map<std::string, float> resource_requirements;
};

struct PlanStep {
    std::string step_id;
    std::string subtask_id;
    std::string agent_id;
    uint64_t start_time;
    uint64_t duration;
    std::map<std::string, float> step_parameters;
    std::vector<std::string> dependencies;
    float priority;
};

struct ExecutionResult {
    std::string execution_id;
    std::string plan_id;
    std::vector<StepResult> step_results;
    std::map<std::string, float> execution_metrics;
    bool success;
    std::string failure_reason;
    uint64_t actual_execution_time;
};

struct StepResult {
    std::string step_id;
    std::string agent_id;
    bool success;
    std::vector<uint8_t> result_data;
    std::map<std::string, float> step_metrics;
    uint64_t actual_duration;
    std::string error_message;
};

struct ResourceRequest {
    std::string request_id;
    std::string resource_type;
    uint64_t quantity_required;
    std::map<std::string, float> resource_parameters;
    uint64_t duration;
    float priority;
};

struct ResourceAllocation {
    std::string allocation_id;
    std::string resource_id;
    std::string request_id;
    uint64_t allocated_quantity;
    uint64_t start_time;
    uint64_t end_time;
    std::map<std::string, float> allocation_parameters;
};

struct PlanningConstraint {
    std::string constraint_id;
    std::string constraint_type;
    std::vector<std::string> affected_elements;
    std::map<std::string, float> constraint_parameters;
    float constraint_strength;
    std::string constraint_description;
};

struct OptimizationObjective {
    std::string objective_id;
    std::string objective_type;
    std::map<std::string, float> objective_parameters;
    float weight;
    std::string objective_description;
};

} // namespace AI
} // namespace AgenticOS