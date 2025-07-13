#pragma once

#include "../multi_agent_system.h"
#include "../agent_wire_protocol.h"
#include <memory>
#include <vector>
#include <map>

namespace AgenticOS {
namespace AI {

// Knowledge Engine - Handles knowledge representation, reasoning, and inference
class KnowledgeEngine {
private:
    // Knowledge components
    struct KnowledgeEngineCore {
        std::unique_ptr<KnowledgeBase> knowledge_base;
        std::unique_ptr<ReasoningEngine> reasoning_engine;
        std::unique_ptr<InferenceEngine> inference_engine;
        std::unique_ptr<OntologyManager> ontology_manager;
        std::unique_ptr<SemanticAnalyzer> semantic_analyzer;
        std::unique_ptr<KnowledgeIntegrator> knowledge_integrator;
    };
    
    // Knowledge capabilities
    enum class KnowledgeCapability {
        KNOWLEDGE_REPRESENTATION,
        REASONING,
        INFERENCE,
        ONTOLOGY_MANAGEMENT,
        SEMANTIC_ANALYSIS,
        KNOWLEDGE_INTEGRATION,
        KNOWLEDGE_DISCOVERY,
        KNOWLEDGE_EXTRACTION,
        KNOWLEDGE_VALIDATION,
        KNOWLEDGE_LEARNING,
        KNOWLEDGE_REASONING,
        KNOWLEDGE_QUERYING,
        KNOWLEDGE_UPDATING,
        KNOWLEDGE_VERSIONING,
        KNOWLEDGE_SHARING,
        KNOWLEDGE_SECURITY
    };
    
    // Knowledge context
    struct KnowledgeContext {
        std::string knowledge_domain;
        std::string representation_format;
        std::vector<std::string> knowledge_sources;
        std::vector<KnowledgeCapability> required_capabilities;
        float confidence_threshold;
        uint64_t reasoning_timeout;
        bool enable_learning;
        bool enable_validation;
    };
    
    // Core components
    std::unique_ptr<KnowledgeEngineCore> knowledge_core;
    std::map<KnowledgeCapability, bool> capability_status;
    std::map<std::string, KnowledgeContext> context_cache;
    
    // Performance tracking
    struct KnowledgeMetrics {
        uint64_t knowledge_entries;
        uint64_t reasoning_operations;
        uint64_t inference_operations;
        uint64_t ontology_operations;
        float average_reasoning_time;
        float knowledge_accuracy;
        std::map<KnowledgeCapability, uint64_t> capability_usage;
        std::vector<std::string> recent_knowledge_events;
    };
    
    KnowledgeMetrics metrics;
    
public:
    KnowledgeEngine() {
        knowledge_core = std::make_unique<KnowledgeEngineCore>();
    }
    
    // Core knowledge functions
    KernelResult Initialize();
    KernelResult StoreKnowledge(const KnowledgeEntry& entry, const KnowledgeContext& context);
    KernelResult QueryKnowledge(const KnowledgeQuery& query, KnowledgeResult& result);
    KernelResult Reason(const ReasoningRequest& request, ReasoningResult& result);
    KernelResult Infer(const InferenceRequest& request, InferenceResult& result);
    KernelResult UpdateOntology(const OntologyUpdate& update, const KnowledgeContext& context);
    
    // Knowledge management
    KernelResult EnableCapability(KnowledgeCapability capability);
    KernelResult DisableCapability(KnowledgeCapability capability);
    bool IsCapabilityEnabled(KnowledgeCapability capability);
    std::vector<KnowledgeCapability> GetEnabledCapabilities();
    
    // Context management
    KernelResult SetKnowledgeContext(const std::string& context_id, const KnowledgeContext& context);
    KernelResult GetKnowledgeContext(const std::string& context_id, KnowledgeContext& context);
    KernelResult UpdateKnowledgeContext(const std::string& context_id, const std::map<std::string, std::string>& updates);
    
    // Performance monitoring
    KnowledgeMetrics GetMetrics() const;
    void ResetMetrics();
    void GenerateKnowledgeReport();
    
private:
    // Knowledge implementations
    KernelResult ExecuteKnowledgeStorage(const std::vector<uint8_t>& knowledge_data);
    KernelResult ExecuteKnowledgeQuery(const std::vector<uint8_t>& query_data);
    KernelResult ExecuteReasoning(const std::vector<uint8_t>& reasoning_data);
    KernelResult ExecuteInference(const std::vector<uint8_t>& inference_data);
    KernelResult ExecuteOntologyUpdate(const std::vector<uint8_t>& ontology_data);
    
    // Knowledge utility functions
    float CalculateKnowledgeConfidence(const std::vector<uint8_t>& knowledge_data);
    void AnalyzeKnowledgePatterns(const std::vector<uint8_t>& pattern_data);
    void UpdateKnowledgeModel(const std::string& knowledge_id, const std::vector<uint8_t>& knowledge_data);
    void OptimizeKnowledgeStrategy(const std::vector<uint8_t>& strategy_data);
    
    // Utility functions
    KnowledgeContext SelectBestContext(const std::string& task_description);
    void LogKnowledgeOperation(const std::string& operation, const std::string& details);
};

// Forward declarations for knowledge engine components
class KnowledgeBase;
class ReasoningEngine;
class InferenceEngine;
class OntologyManager;
class SemanticAnalyzer;
class KnowledgeIntegrator;

// Knowledge data structures
struct KnowledgeEntry {
    std::string entry_id;
    std::string entry_type;
    std::string entry_content;
    std::map<std::string, float> entry_metadata;
    float confidence_score;
    uint64_t timestamp;
    std::string source;
    std::vector<std::string> tags;
};

struct KnowledgeQuery {
    std::string query_id;
    std::string query_type;
    std::string query_content;
    std::map<std::string, float> query_parameters;
    std::vector<std::string> query_constraints;
    uint64_t timeout;
    float confidence_threshold;
};

struct KnowledgeResult {
    std::string result_id;
    std::string query_id;
    std::vector<KnowledgeEntry> entries;
    std::map<std::string, float> result_metrics;
    float confidence_score;
    uint64_t query_time;
    std::string result_type;
};

struct ReasoningRequest {
    std::string request_id;
    std::string reasoning_type;
    std::vector<std::string> premises;
    std::string conclusion;
    std::map<std::string, float> reasoning_parameters;
    uint64_t timeout;
    float confidence_threshold;
};

struct ReasoningResult {
    std::string result_id;
    std::string request_id;
    bool valid_conclusion;
    std::vector<std::string> reasoning_steps;
    std::map<std::string, float> reasoning_metrics;
    float confidence_score;
    std::string reasoning_method;
};

struct InferenceRequest {
    std::string request_id;
    std::string inference_type;
    std::vector<std::string> evidence;
    std::map<std::string, float> inference_parameters;
    uint64_t timeout;
    float confidence_threshold;
};

struct InferenceResult {
    std::string result_id;
    std::string request_id;
    std::vector<std::string> conclusions;
    std::map<std::string, float> inference_metrics;
    float confidence_score;
    std::string inference_method;
};

struct OntologyUpdate {
    std::string update_id;
    std::string ontology_id;
    std::string update_type;
    std::vector<std::string> concepts;
    std::map<std::string, std::string> relationships;
    std::map<std::string, float> update_parameters;
    uint64_t timestamp;
};

struct KnowledgeOntology {
    std::string ontology_id;
    std::string ontology_name;
    std::vector<std::string> concepts;
    std::map<std::string, std::string> relationships;
    std::map<std::string, float> concept_properties;
    uint64_t last_updated;
};

struct KnowledgeRule {
    std::string rule_id;
    std::string rule_type;
    std::vector<std::string> conditions;
    std::vector<std::string> conclusions;
    std::map<std::string, float> rule_parameters;
    float confidence_score;
    uint64_t last_used;
};

} // namespace AI
} // namespace AgenticOS