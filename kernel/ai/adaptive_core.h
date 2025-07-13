#pragma once

#include <cstdint>
#include <atomic>
#include <vector>
#include <memory>
#include "../common/kernel_types.h"

namespace AgenticOS {
namespace AI {

// Universal Task Abstraction - can represent any human task
struct UniversalTask {
    uint64_t task_id;
    TaskType type;
    std::string description;
    std::vector<uint8_t> input_data;
    std::vector<uint8_t> context_data;
    uint32_t complexity_score;
    uint32_t required_capabilities;
    uint64_t deadline_us;
    
    // Learning metadata
    uint32_t execution_count;
    uint32_t success_rate;
    uint64_t average_execution_time;
    std::vector<uint8_t> learned_patterns;
};

// Human Behavior Model - learns and adapts to user patterns
class HumanBehaviorModel {
private:
    struct BehaviorPattern {
        std::string pattern_name;
        std::vector<float> features;
        float confidence;
        uint64_t last_updated;
        uint32_t occurrence_count;
    };
    
    std::vector<BehaviorPattern> patterns;
    std::atomic<uint64_t> interactions_processed;
    std::atomic<float> adaptation_rate;
    
public:
    void ObserveInteraction(const std::vector<uint8_t>& interaction_data);
    std::vector<float> PredictNextAction(const std::vector<uint8_t>& current_context);
    void UpdatePreferences(const std::vector<uint8_t>& feedback);
    float GetAdaptationConfidence() const;
    void EvolveBehaviorModel();
};

// Capability Learning Engine - learns new capabilities dynamically
class CapabilityLearningEngine {
private:
    struct Capability {
        uint32_t capability_id;
        std::string name;
        std::string description;
        std::vector<uint8_t> implementation_code;
        std::vector<uint32_t> required_tools;
        float success_rate;
        uint64_t learning_iterations;
        bool is_evolving;
    };
    
    std::vector<Capability> capabilities;
    std::atomic<uint32_t> next_capability_id;
    
public:
    uint32_t LearnNewCapability(const std::string& task_description, 
                               const std::vector<uint8_t>& example_data);
    void ImproveCapability(uint32_t capability_id, 
                          const std::vector<uint8_t>& feedback);
    std::vector<uint32_t> FindCapabilitiesForTask(const UniversalTask& task);
    void EvolveCapabilities();
};

// Self-Evolution Engine - continuously improves the OS
class SelfEvolutionEngine {
private:
    struct EvolutionCandidate {
        std::string component_name;
        std::vector<uint8_t> new_code;
        float performance_gain;
        float risk_score;
        uint64_t test_iterations;
    };
    
    std::vector<EvolutionCandidate> candidates;
    std::atomic<uint64_t> evolution_cycles;
    std::atomic<float> system_performance_baseline;
    
public:
    void AnalyzeSystemPerformance();
    void GenerateEvolutionCandidates();
    void TestEvolutionCandidate(const EvolutionCandidate& candidate);
    void ApplySuccessfulEvolutions();
    void RollbackFailedEvolution(const std::string& component_name);
};

// Universal Interface Engine - can interface with any tool/system
class UniversalInterfaceEngine {
private:
    struct InterfaceAdapter {
        uint32_t adapter_id;
        std::string interface_type;
        std::vector<uint8_t> protocol_handler;
        std::vector<std::string> supported_operations;
        bool auto_discovered;
        float reliability_score;
    };
    
    std::vector<InterfaceAdapter> adapters;
    std::atomic<uint32_t> active_connections;
    
public:
    uint32_t DiscoverInterface(const std::string& target_system);
    KernelResult ConnectToSystem(uint32_t adapter_id, const std::string& connection_params);
    KernelResult ExecuteOperation(uint32_t adapter_id, const std::string& operation, 
                                 const std::vector<uint8_t>& parameters);
    void LearnNewProtocol(const std::vector<uint8_t>& protocol_data);
    std::vector<std::string> GetAvailableOperations(uint32_t adapter_id);
};

// Main Adaptive AI Core - the brain of the OS
class AdaptiveAICore {
private:
    // Core AI components
    std::unique_ptr<HumanBehaviorModel> behavior_model;
    std::unique_ptr<CapabilityLearningEngine> capability_engine;
    std::unique_ptr<SelfEvolutionEngine> evolution_engine;
    std::unique_ptr<UniversalInterfaceEngine> interface_engine;
    
    // Knowledge and memory
    std::vector<UniversalTask> task_history;
    std::vector<uint8_t> global_knowledge_base;
    std::vector<uint8_t> episodic_memory;
    std::vector<uint8_t> procedural_memory;
    
    // Learning state
    std::atomic<uint64_t> total_tasks_executed;
    std::atomic<float> overall_success_rate;
    std::atomic<uint64_t> learning_iterations;
    std::atomic<bool> is_learning;
    std::atomic<bool> is_evolving;
    
    // Adaptation parameters
    float adaptation_aggressiveness;
    float exploration_rate;
    float exploitation_rate;
    uint64_t personality_seed;
    
    // Safety and constraints
    std::vector<std::string> safety_constraints;
    std::vector<std::string> ethical_guidelines;
    float max_risk_tolerance;
    
public:
    AdaptiveAICore() : 
        total_tasks_executed(0),
        overall_success_rate(0.0f),
        learning_iterations(0),
        is_learning(false),
        is_evolving(false),
        adaptation_aggressiveness(0.5f),
        exploration_rate(0.3f),
        exploitation_rate(0.7f),
        personality_seed(0),
        max_risk_tolerance(0.1f) {}
    
    // Core functions
    KernelResult Initialize(const std::vector<uint8_t>& initial_knowledge);
    KernelResult ExecuteTask(const UniversalTask& task);
    void AdaptToHuman(const std::vector<uint8_t>& interaction_data);
    void LearnFromExperience(const UniversalTask& task, const std::vector<uint8_t>& outcome);
    
    // Capability expansion
    KernelResult LearnNewSkill(const std::string& skill_description, 
                              const std::vector<uint8_t>& training_data);
    KernelResult IntegrateNewTool(const std::string& tool_interface,
                                 const std::vector<uint8_t>& tool_specs);
    KernelResult ConnectToExternalSystem(const std::string& system_type,
                                        const std::string& connection_info);
    
    // Evolution and adaptation
    void EvolveCapabilities();
    void AdaptPersonality(const std::vector<uint8_t>& user_feedback);
    void OptimizePerformance();
    void UpdateEthicalGuidelines(const std::vector<std::string>& new_guidelines);
    
    // Reasoning and planning
    std::vector<UniversalTask> PlanTaskSequence(const std::string& goal_description);
    std::vector<uint8_t> GenerateCreativeSolution(const std::string& problem_description);
    float EvaluateTaskFeasibility(const UniversalTask& task);
    std::vector<std::string> ExplainReasoning(const UniversalTask& task);
    
    // Human interaction
    std::string CommunicateWithHuman(const std::string& input_message);
    void UnderstandHumanIntent(const std::vector<uint8_t>& multimodal_input);
    std::vector<uint8_t> PredictHumanNeeds(const std::vector<uint8_t>& context);
    void AdjustToHumanPreferences(const std::vector<uint8_t>& preference_data);
    
    // Monitoring and statistics
    struct AdaptiveStats {
        uint64_t tasks_executed;
        float success_rate;
        uint64_t capabilities_learned;
        uint64_t evolution_cycles;
        float adaptation_confidence;
        uint32_t active_interfaces;
        uint64_t knowledge_base_size;
        float human_satisfaction_score;
    };
    
    AdaptiveStats GetStats() const;
    bool IsHealthy() const;
    void PerformSelfDiagnostics();
    
    // Meta-learning and self-reflection
    void ReflectOnPerformance();
    void AnalyzeLearningPatterns();
    void OptimizeLearningStrategy();
    void PredictFutureCapabilities();
    
private:
    // Internal learning mechanisms
    void UpdateKnowledgeBase(const std::vector<uint8_t>& new_knowledge);
    void ConsolidateMemories();
    void PruneIrrelevantInformation();
    void CrossReferenceKnowledge();
    
    // Internal adaptation mechanisms
    void AnalyzeUserPatterns();
    void AdjustBehaviorParameters();
    void PersonalizeInteractions();
    void OptimizeUserExperience();
    
    // Safety and validation
    bool ValidateEvolution(const std::vector<uint8_t>& evolution_candidate);
    bool CheckEthicalCompliance(const UniversalTask& task);
    void EnforceSafetyConstraints();
    void MonitorSystemIntegrity();
};

// Task Categories - comprehensive classification
enum class TaskType : uint32_t {
    // Cognitive tasks
    REASONING = 0x0001,
    PROBLEM_SOLVING = 0x0002,
    CREATIVE_THINKING = 0x0003,
    LEARNING = 0x0004,
    MEMORY_RETRIEVAL = 0x0005,
    PATTERN_RECOGNITION = 0x0006,
    DECISION_MAKING = 0x0007,
    PLANNING = 0x0008,
    
    // Communication tasks
    NATURAL_LANGUAGE = 0x0100,
    TRANSLATION = 0x0101,
    SPEECH_RECOGNITION = 0x0102,
    SPEECH_SYNTHESIS = 0x0103,
    WRITING = 0x0104,
    READING_COMPREHENSION = 0x0105,
    CONVERSATION = 0x0106,
    
    // Physical tasks (through interfaces)
    MOTOR_CONTROL = 0x0200,
    MANIPULATION = 0x0201,
    NAVIGATION = 0x0202,
    COORDINATION = 0x0203,
    FINE_MOTOR = 0x0204,
    
    // Sensory tasks
    VISUAL_PROCESSING = 0x0300,
    AUDIO_PROCESSING = 0x0301,
    MULTIMODAL_PERCEPTION = 0x0302,
    SENSOR_FUSION = 0x0303,
    
    // Social tasks
    EMOTION_RECOGNITION = 0x0400,
    SOCIAL_INTERACTION = 0x0401,
    EMPATHY = 0x0402,
    CULTURAL_ADAPTATION = 0x0403,
    
    // Creative tasks
    ART_CREATION = 0x0500,
    MUSIC_COMPOSITION = 0x0501,
    STORYTELLING = 0x0502,
    DESIGN = 0x0503,
    INNOVATION = 0x0504,
    
    // Technical tasks
    PROGRAMMING = 0x0600,
    SYSTEM_ADMINISTRATION = 0x0601,
    DATA_ANALYSIS = 0x0602,
    SCIENTIFIC_RESEARCH = 0x0603,
    ENGINEERING = 0x0604,
    
    // Business tasks
    PROJECT_MANAGEMENT = 0x0700,
    FINANCIAL_ANALYSIS = 0x0701,
    MARKETING = 0x0702,
    SALES = 0x0703,
    CUSTOMER_SERVICE = 0x0704,
    
    // Personal tasks
    PERSONAL_ASSISTANT = 0x0800,
    EDUCATION = 0x0801,
    ENTERTAINMENT = 0x0802,
    HEALTH_MONITORING = 0x0803,
    LIFESTYLE_OPTIMIZATION = 0x0804,
    
    // Meta tasks
    SELF_IMPROVEMENT = 0x0900,
    CAPABILITY_LEARNING = 0x0901,
    ADAPTATION = 0x0902,
    EVOLUTION = 0x0903,
    
    // Unknown/Custom
    UNKNOWN = 0xFFFF,
    CUSTOM = 0xFFFE
};

// Global adaptive AI core instance
extern AdaptiveAICore* g_adaptive_core;

} // namespace AI
} // namespace AgenticOS