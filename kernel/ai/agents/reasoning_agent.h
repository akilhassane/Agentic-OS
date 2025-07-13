#pragma once

#include "../multi_agent_system.h"
#include "../agent_wire_protocol.h"
#include <memory>
#include <vector>
#include <map>

namespace AgenticOS {
namespace AI {

// Reasoning Agent - Handles logical reasoning, problem solving, and decision making
class ReasoningAgent : public BaseAgent {
private:
    // Reasoning engine components
    struct ReasoningEngine {
        std::unique_ptr<LogicEngine> logic_engine;
        std::unique_ptr<InferenceEngine> inference_engine;
        std::unique_ptr<DecisionEngine> decision_engine;
        std::unique_ptr<ProblemSolver> problem_solver;
        std::unique_ptr<ConstraintSolver> constraint_solver;
        std::unique_ptr<OptimizationEngine> optimization_engine;
    };
    
    // Knowledge representation
    struct KnowledgeBase {
        std::vector<LogicalRule> rules;
        std::vector<Fact> facts;
        std::vector<Concept> concepts;
        std::vector<Relationship> relationships;
        std::map<std::string, std::vector<uint8_t>> domain_knowledge;
    };
    
    // Reasoning strategies
    enum class ReasoningStrategy {
        DEDUCTIVE,
        INDUCTIVE,
        ABDUCTIVE,
        ANALOGICAL,
        CASE_BASED,
        RULE_BASED,
        MODEL_BASED,
        CONSTRAINT_BASED,
        OPTIMIZATION_BASED,
        HYBRID
    };
    
    // Reasoning context
    struct ReasoningContext {
        std::string problem_domain;
        std::vector<std::string> assumptions;
        std::vector<std::string> constraints;
        std::map<std::string, float> confidence_levels;
        uint64_t reasoning_timeout;
        ReasoningStrategy preferred_strategy;
        bool allow_uncertainty;
        bool require_explanation;
    };
    
    // Core components
    std::unique_ptr<ReasoningEngine> reasoning_engine;
    std::unique_ptr<KnowledgeBase> knowledge_base;
    std::map<std::string, ReasoningContext> context_cache;
    
    // Performance tracking
    struct ReasoningMetrics {
        uint64_t problems_solved;
        uint64_t reasoning_time_total;
        uint64_t average_reasoning_time;
        float success_rate;
        std::map<ReasoningStrategy, uint64_t> strategy_usage;
        std::vector<std::string> recent_problems;
    };
    
    ReasoningMetrics metrics;
    
public:
    ReasoningAgent(uint32_t id) : BaseAgent(id, "ReasoningAgent", AgentSpecialization::REASONING_AGENT) {
        reasoning_engine = std::make_unique<ReasoningEngine>();
        knowledge_base = std::make_unique<KnowledgeBase>();
    }
    
    // Core agent functions
    KernelResult Initialize() override;
    KernelResult ExecuteTask(const std::vector<uint8_t>& task_data) override;
    void ProcessMessage(const AgentMessage& message) override;
    void LearnFromExperience(const std::vector<uint8_t>& experience_data) override;
    void AdaptToEnvironment(const std::vector<uint8_t>& environment_data) override;
    
    // Reasoning capabilities
    KernelResult SolveProblem(const std::string& problem_description, const std::vector<uint8_t>& problem_data);
    KernelResult MakeDecision(const std::vector<std::string>& options, const std::vector<uint8_t>& context);
    KernelResult InferConclusion(const std::vector<std::string>& premises, const std::vector<uint8_t>& evidence);
    KernelResult OptimizeSolution(const std::vector<uint8_t>& current_solution, const std::vector<std::string>& objectives);
    KernelResult ValidateArgument(const std::vector<std::string>& premises, const std::string& conclusion);
    
    // Knowledge management
    KernelResult AddKnowledge(const std::vector<uint8_t>& knowledge_data);
    KernelResult QueryKnowledge(const std::string& query, std::vector<uint8_t>& result);
    KernelResult UpdateKnowledge(const std::string& concept, const std::vector<uint8_t>& new_data);
    KernelResult RemoveKnowledge(const std::string& concept);
    
    // Reasoning strategies
    void SetReasoningStrategy(ReasoningStrategy strategy);
    void EnableUncertaintyHandling(bool enable);
    void SetConfidenceThreshold(float threshold);
    void EnableExplanationGeneration(bool enable);
    
    // Performance monitoring
    ReasoningMetrics GetMetrics() const;
    void ResetMetrics();
    void GenerateReasoningReport();
    
protected:
    // Internal reasoning functions
    virtual void MainLoop() override;
    virtual void ProcessTask(const std::vector<uint8_t>& task_data) override;
    virtual void HandleMessage(const AgentMessage& message) override;
    virtual void PerformLearning() override;
    virtual void UpdateState() override;
    
private:
    // Reasoning engine implementations
    KernelResult ExecuteDeductiveReasoning(const std::vector<uint8_t>& problem_data);
    KernelResult ExecuteInductiveReasoning(const std::vector<uint8_t>& problem_data);
    KernelResult ExecuteAbductiveReasoning(const std::vector<uint8_t>& problem_data);
    KernelResult ExecuteAnalogicalReasoning(const std::vector<uint8_t>& problem_data);
    KernelResult ExecuteCaseBasedReasoning(const std::vector<uint8_t>& problem_data);
    
    // Knowledge processing
    void ProcessNewKnowledge(const std::vector<uint8_t>& knowledge_data);
    void UpdateKnowledgeGraph();
    void ValidateKnowledgeConsistency();
    void OptimizeKnowledgeStructure();
    
    // Utility functions
    ReasoningStrategy SelectBestStrategy(const std::vector<uint8_t>& problem_data);
    float CalculateConfidence(const std::vector<uint8_t>& reasoning_result);
    std::string GenerateExplanation(const std::vector<uint8_t>& reasoning_process);
    void LogReasoningStep(const std::string& step_description);
};

// Forward declarations for reasoning engine components
class LogicEngine;
class InferenceEngine;
class DecisionEngine;
class ProblemSolver;
class ConstraintSolver;
class OptimizationEngine;

// Knowledge representation structures
struct LogicalRule {
    std::string rule_id;
    std::string antecedent;
    std::string consequent;
    float confidence;
    std::vector<std::string> exceptions;
    uint64_t usage_count;
    uint64_t last_used;
};

struct Fact {
    std::string fact_id;
    std::string predicate;
    std::vector<std::string> arguments;
    float confidence;
    uint64_t timestamp;
    std::string source;
};

struct Concept {
    std::string concept_id;
    std::string name;
    std::string definition;
    std::vector<std::string> properties;
    std::vector<std::string> examples;
    std::vector<std::string> related_concepts;
};

struct Relationship {
    std::string relationship_id;
    std::string source_concept;
    std::string target_concept;
    std::string relationship_type;
    float strength;
    std::vector<std::string> conditions;
};

} // namespace AI
} // namespace AgenticOS