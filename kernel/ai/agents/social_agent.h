#pragma once

#include "../multi_agent_system.h"
#include "../agent_wire_protocol.h"
#include <memory>
#include <vector>
#include <map>

namespace AgenticOS {
namespace AI {

// Social Agent - Handles social interaction, empathy, and relationship management
class SocialAgent : public BaseAgent {
private:
    // Social interaction components
    struct SocialEngine {
        std::unique_ptr<EmpathyEngine> empathy_engine;
        std::unique_ptr<ConversationManager> conversation_manager;
        std::unique_ptr<RelationshipTracker> relationship_tracker;
        std::unique_ptr<EmotionAnalyzer> emotion_analyzer;
        std::unique_ptr<SocialLearning> social_learning;
        std::unique_ptr<CulturalAdapter> cultural_adapter;
    };
    
    // Social capabilities
    enum class SocialCapability {
        EMPATHY,
        CONVERSATION,
        EMOTION_RECOGNITION,
        RELATIONSHIP_BUILDING,
        CONFLICT_RESOLUTION,
        COLLABORATION,
        LEADERSHIP,
        FOLLOWERSHIP,
        CULTURAL_ADAPTATION,
        SOCIAL_LEARNING,
        PERSUASION,
        NEGOTIATION,
        MEDIATION,
        MENTORING,
        COACHING,
        SUPPORT_PROVIDING
    };
    
    // Social interaction context
    struct SocialContext {
        std::string interaction_type;
        std::string relationship_level;
        std::string cultural_context;
        std::vector<std::string> participants;
        std::map<std::string, float> emotional_states;
        std::vector<SocialCapability> required_capabilities;
        float empathy_level;
        bool enable_adaptive_behavior;
        bool preserve_privacy;
    };
    
    // Core components
    std::unique_ptr<SocialEngine> social_engine;
    std::map<SocialCapability, bool> capability_status;
    std::map<std::string, SocialContext> context_cache;
    
    // Performance tracking
    struct SocialMetrics {
        uint64_t interactions_handled;
        uint64_t conversations_managed;
        uint64_t relationships_built;
        uint64_t conflicts_resolved;
        float average_empathy_score;
        float average_satisfaction_score;
        std::map<SocialCapability, uint64_t> capability_usage;
        std::vector<std::string> recent_interactions;
    };
    
    SocialMetrics metrics;
    
public:
    SocialAgent(uint32_t id) : BaseAgent(id, "SocialAgent", AgentSpecialization::SOCIAL_INTERACTION_AGENT) {
        social_engine = std::make_unique<SocialEngine>();
    }
    
    // Core agent functions
    KernelResult Initialize() override;
    KernelResult ExecuteTask(const std::vector<uint8_t>& task_data) override;
    void ProcessMessage(const AgentMessage& message) override;
    void LearnFromExperience(const std::vector<uint8_t>& experience_data) override;
    void AdaptToEnvironment(const std::vector<uint8_t>& environment_data) override;
    
    // Social interaction capabilities
    KernelResult ProcessInteraction(const SocialInteraction& interaction, const SocialContext& context);
    KernelResult ManageConversation(const Conversation& conversation, const SocialContext& context);
    KernelResult BuildRelationship(const RelationshipTarget& target, const SocialContext& context);
    KernelResult ResolveConflict(const Conflict& conflict, const SocialContext& context);
    KernelResult ProvideSupport(const SupportRequest& request, const SocialContext& context);
    KernelResult AdaptToCulture(const CulturalContext& culture, const SocialContext& context);
    
    // Social management
    KernelResult EnableCapability(SocialCapability capability);
    KernelResult DisableCapability(SocialCapability capability);
    bool IsCapabilityEnabled(SocialCapability capability);
    std::vector<SocialCapability> GetEnabledCapabilities();
    
    // Context management
    KernelResult SetSocialContext(const std::string& context_id, const SocialContext& context);
    KernelResult GetSocialContext(const std::string& context_id, SocialContext& context);
    KernelResult UpdateSocialContext(const std::string& context_id, const std::map<std::string, std::string>& updates);
    
    // Performance monitoring
    SocialMetrics GetMetrics() const;
    void ResetMetrics();
    void GenerateSocialReport();
    
protected:
    // Internal social functions
    virtual void MainLoop() override;
    virtual void ProcessTask(const std::vector<uint8_t>& task_data) override;
    virtual void HandleMessage(const AgentMessage& message) override;
    virtual void PerformLearning() override;
    virtual void UpdateState() override;
    
private:
    // Social interaction implementations
    KernelResult ExecuteEmpathyResponse(const std::vector<uint8_t>& empathy_data);
    KernelResult ExecuteConversationManagement(const std::vector<uint8_t>& conversation_data);
    KernelResult ExecuteRelationshipBuilding(const std::vector<uint8_t>& relationship_data);
    KernelResult ExecuteConflictResolution(const std::vector<uint8_t>& conflict_data);
    KernelResult ExecuteSupportProvision(const std::vector<uint8_t>& support_data);
    
    // Social utility functions
    float CalculateEmpathyScore(const std::vector<uint8_t>& interaction_data);
    void AnalyzeEmotionalState(const std::vector<uint8_t>& emotional_data);
    void UpdateRelationshipModel(const std::string& person_id, const std::vector<uint8_t>& interaction_data);
    void AdaptSocialBehavior(const std::vector<uint8_t>& cultural_data);
    
    // Utility functions
    SocialContext SelectBestContext(const std::string& task_description);
    void LogSocialOperation(const std::string& operation, const std::string& details);
};

// Forward declarations for social engine components
class EmpathyEngine;
class ConversationManager;
class RelationshipTracker;
class EmotionAnalyzer;
class SocialLearning;
class CulturalAdapter;

// Social data structures
struct SocialInteraction {
    std::string interaction_id;
    std::string interaction_type;
    std::vector<std::string> participants;
    std::vector<uint8_t> interaction_data;
    std::map<std::string, float> emotional_states;
    uint64_t timestamp;
    float intensity;
};

struct Conversation {
    std::string conversation_id;
    std::vector<std::string> participants;
    std::vector<ConversationTurn> turns;
    std::string topic;
    std::map<std::string, float> emotional_trajectory;
    uint64_t start_time;
    uint64_t end_time;
};

struct ConversationTurn {
    std::string speaker_id;
    std::string message;
    std::map<std::string, float> emotions;
    uint64_t timestamp;
    float confidence;
};

struct RelationshipTarget {
    std::string person_id;
    std::string relationship_type;
    std::map<std::string, float> relationship_parameters;
    std::vector<std::string> shared_interests;
    float trust_level;
    float familiarity_level;
};

struct Conflict {
    std::string conflict_id;
    std::vector<std::string> parties_involved;
    std::string conflict_type;
    std::string root_cause;
    std::map<std::string, float> emotional_intensities;
    float urgency_level;
    std::vector<std::string> resolution_strategies;
};

struct SupportRequest {
    std::string request_id;
    std::string requester_id;
    std::string support_type;
    std::string description;
    float urgency_level;
    std::map<std::string, float> emotional_state;
    std::vector<std::string> preferred_support_methods;
};

struct CulturalContext {
    std::string culture_id;
    std::string culture_name;
    std::map<std::string, std::string> cultural_norms;
    std::vector<std::string> communication_styles;
    std::map<std::string, float> cultural_values;
    std::vector<std::string> taboos;
};

struct RelationshipModel {
    std::string person_id;
    std::map<std::string, float> relationship_dimensions;
    std::vector<std::string> interaction_history;
    float trust_score;
    float familiarity_score;
    std::map<std::string, float> emotional_bonds;
    uint64_t last_interaction;
};

} // namespace AI
} // namespace AgenticOS