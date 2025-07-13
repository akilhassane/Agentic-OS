#pragma once

#include "../multi_agent_system.h"
#include "../agent_wire_protocol.h"
#include <memory>
#include <vector>
#include <map>

namespace AgenticOS {
namespace AI {

// Learning Agent - Handles capability acquisition, skill learning, and knowledge transfer
class LearningAgent : public BaseAgent {
private:
    // Learning components
    struct LearningEngine {
        std::unique_ptr<SkillAcquisition> skill_acquisition;
        std::unique_ptr<KnowledgeTransfer> knowledge_transfer;
        std::unique_ptr<MetaLearning> meta_learning;
        std::unique_ptr<CurriculumDesigner> curriculum_designer;
        std::unique_ptr<LearningOptimizer> learning_optimizer;
        std::unique_ptr<CompetencyAssessor> competency_assessor;
    };
    
    // Learning capabilities
    enum class LearningCapability {
        SKILL_ACQUISITION,
        KNOWLEDGE_TRANSFER,
        META_LEARNING,
        CURRICULUM_DESIGN,
        LEARNING_OPTIMIZATION,
        COMPETENCY_ASSESSMENT,
        ADAPTIVE_LEARNING,
        COLLABORATIVE_LEARNING,
        EXPERIENTIAL_LEARNING,
        TRANSFER_LEARNING,
        ACTIVE_LEARNING,
        REINFORCEMENT_LEARNING,
        SUPERVISED_LEARNING,
        UNSUPERVISED_LEARNING,
        SEMI_SUPERVISED_LEARNING,
        FEDERATED_LEARNING
    };
    
    // Learning context
    struct LearningContext {
        std::string learning_domain;
        std::string learning_objective;
        std::vector<std::string> prerequisites;
        std::vector<LearningCapability> required_capabilities;
        float difficulty_level;
        uint64_t learning_timeout;
        bool enable_adaptive_curriculum;
        bool enable_collaborative_learning;
    };
    
    // Core components
    std::unique_ptr<LearningEngine> learning_engine;
    std::map<LearningCapability, bool> capability_status;
    std::map<std::string, LearningContext> context_cache;
    
    // Performance tracking
    struct LearningMetrics {
        uint64_t skills_acquired;
        uint64_t knowledge_transfers;
        uint64_t learning_sessions;
        uint64_t competencies_assessed;
        float average_learning_rate;
        float average_retention_rate;
        std::map<LearningCapability, uint64_t> capability_usage;
        std::vector<std::string> recent_learning_activities;
    };
    
    LearningMetrics metrics;
    
public:
    LearningAgent(uint32_t id) : BaseAgent(id, "LearningAgent", AgentSpecialization::LEARNING_AGENT) {
        learning_engine = std::make_unique<LearningEngine>();
    }
    
    // Core agent functions
    KernelResult Initialize() override;
    KernelResult ExecuteTask(const std::vector<uint8_t>& task_data) override;
    void ProcessMessage(const AgentMessage& message) override;
    void LearnFromExperience(const std::vector<uint8_t>& experience_data) override;
    void AdaptToEnvironment(const std::vector<uint8_t>& environment_data) override;
    
    // Learning capabilities
    KernelResult AcquireSkill(const SkillTarget& skill, const LearningContext& context);
    KernelResult TransferKnowledge(const KnowledgeSource& source, const KnowledgeTarget& target, const LearningContext& context);
    KernelResult DesignCurriculum(const LearningObjective& objective, const LearningContext& context);
    KernelResult OptimizeLearning(const LearningSession& session, const LearningContext& context);
    KernelResult AssessCompetency(const CompetencyTarget& competency, const LearningContext& context);
    KernelResult AdaptLearningStrategy(const LearningFeedback& feedback, const LearningContext& context);
    
    // Learning management
    KernelResult EnableCapability(LearningCapability capability);
    KernelResult DisableCapability(LearningCapability capability);
    bool IsCapabilityEnabled(LearningCapability capability);
    std::vector<LearningCapability> GetEnabledCapabilities();
    
    // Context management
    KernelResult SetLearningContext(const std::string& context_id, const LearningContext& context);
    KernelResult GetLearningContext(const std::string& context_id, LearningContext& context);
    KernelResult UpdateLearningContext(const std::string& context_id, const std::map<std::string, std::string>& updates);
    
    // Performance monitoring
    LearningMetrics GetMetrics() const;
    void ResetMetrics();
    void GenerateLearningReport();
    
protected:
    // Internal learning functions
    virtual void MainLoop() override;
    virtual void ProcessTask(const std::vector<uint8_t>& task_data) override;
    virtual void HandleMessage(const AgentMessage& message) override;
    virtual void PerformLearning() override;
    virtual void UpdateState() override;
    
private:
    // Learning implementations
    KernelResult ExecuteSkillAcquisition(const std::vector<uint8_t>& skill_data);
    KernelResult ExecuteKnowledgeTransfer(const std::vector<uint8_t>& transfer_data);
    KernelResult ExecuteCurriculumDesign(const std::vector<uint8_t>& curriculum_data);
    KernelResult ExecuteLearningOptimization(const std::vector<uint8_t>& optimization_data);
    KernelResult ExecuteCompetencyAssessment(const std::vector<uint8_t>& assessment_data);
    
    // Learning utility functions
    float CalculateLearningProgress(const std::vector<uint8_t>& learning_data);
    void AnalyzeLearningPatterns(const std::vector<uint8_t>& pattern_data);
    void UpdateLearningModel(const std::string& skill_id, const std::vector<uint8_t>& learning_data);
    void OptimizeLearningStrategy(const std::vector<uint8_t>& strategy_data);
    
    // Utility functions
    LearningContext SelectBestContext(const std::string& task_description);
    void LogLearningOperation(const std::string& operation, const std::string& details);
};

// Forward declarations for learning engine components
class SkillAcquisition;
class KnowledgeTransfer;
class MetaLearning;
class CurriculumDesigner;
class LearningOptimizer;
class CompetencyAssessor;

// Learning data structures
struct SkillTarget {
    std::string skill_id;
    std::string skill_name;
    std::string skill_description;
    std::vector<std::string> prerequisites;
    std::map<std::string, float> skill_parameters;
    float difficulty_level;
    uint64_t estimated_learning_time;
};

struct KnowledgeSource {
    std::string source_id;
    std::string source_type;
    std::vector<uint8_t> knowledge_data;
    std::map<std::string, float> knowledge_metadata;
    float reliability_score;
    uint64_t last_updated;
};

struct KnowledgeTarget {
    std::string target_id;
    std::string target_type;
    std::vector<std::string> target_capabilities;
    std::map<std::string, float> target_parameters;
    float current_knowledge_level;
    float target_knowledge_level;
};

struct LearningObjective {
    std::string objective_id;
    std::string objective_description;
    std::vector<std::string> learning_outcomes;
    std::map<std::string, float> success_criteria;
    float priority_level;
    uint64_t deadline;
};

struct LearningSession {
    std::string session_id;
    std::string session_type;
    std::vector<uint8_t> session_data;
    std::map<std::string, float> session_metrics;
    uint64_t start_time;
    uint64_t end_time;
    float effectiveness_score;
};

struct CompetencyTarget {
    std::string competency_id;
    std::string competency_name;
    std::vector<std::string> competency_dimensions;
    std::map<std::string, float> competency_levels;
    float current_proficiency;
    float target_proficiency;
};

struct LearningFeedback {
    std::string feedback_id;
    std::string learning_session_id;
    std::map<std::string, float> feedback_metrics;
    std::vector<std::string> improvement_suggestions;
    float overall_satisfaction;
    uint64_t timestamp;
};

struct LearningModel {
    std::string model_id;
    std::map<std::string, float> learning_parameters;
    std::vector<std::string> acquired_skills;
    std::map<std::string, float> knowledge_levels;
    float overall_learning_rate;
    uint64_t total_learning_time;
};

} // namespace AI
} // namespace AgenticOS