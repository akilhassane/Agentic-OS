#pragma once

#include "../multi_agent_system.h"
#include "../agent_wire_protocol.h"
#include <memory>
#include <vector>
#include <map>

namespace AgenticOS {
namespace AI {

// Security Agent - Handles threat detection, security monitoring, and incident response
class SecurityAgent : public BaseAgent {
private:
    // Security components
    struct SecurityEngine {
        std::unique_ptr<ThreatDetector> threat_detector;
        std::unique_ptr<IntrusionDetector> intrusion_detector;
        std::unique_ptr<MalwareAnalyzer> malware_analyzer;
        std::unique_ptr<VulnerabilityScanner> vulnerability_scanner;
        std::unique_ptr<IncidentResponder> incident_responder;
        std::unique_ptr<ForensicAnalyzer> forensic_analyzer;
    };
    
    // Security capabilities
    enum class SecurityCapability {
        THREAT_DETECTION,
        INTRUSION_DETECTION,
        MALWARE_ANALYSIS,
        VULNERABILITY_SCANNING,
        INCIDENT_RESPONSE,
        FORENSIC_ANALYSIS,
        BEHAVIORAL_ANALYSIS,
        ANOMALY_DETECTION,
        SIGNATURE_MATCHING,
        HEURISTIC_ANALYSIS,
        SANDBOX_ANALYSIS,
        NETWORK_MONITORING,
        ENDPOINT_PROTECTION,
        DATA_LOSS_PREVENTION,
        ACCESS_CONTROL,
        CRYPTOGRAPHIC_PROTECTION
    };
    
    // Security context
    struct SecurityContext {
        std::string security_domain;
        std::string threat_level;
        std::vector<std::string> protected_assets;
        std::vector<SecurityCapability> required_capabilities;
        float sensitivity_level;
        uint64_t response_timeout;
        bool enable_real_time_monitoring;
        bool enable_automated_response;
    };
    
    // Core components
    std::unique_ptr<SecurityEngine> security_engine;
    std::map<SecurityCapability, bool> capability_status;
    std::map<std::string, SecurityContext> context_cache;
    
    // Performance tracking
    struct SecurityMetrics {
        uint64_t threats_detected;
        uint64_t incidents_responded;
        uint64_t vulnerabilities_found;
        uint64_t malware_analyzed;
        float average_response_time;
        float threat_detection_rate;
        std::map<SecurityCapability, uint64_t> capability_usage;
        std::vector<std::string> recent_security_events;
    };
    
    SecurityMetrics metrics;
    
public:
    SecurityAgent(uint32_t id) : BaseAgent(id, "SecurityAgent", AgentSpecialization::SECURITY_AGENT) {
        security_engine = std::make_unique<SecurityEngine>();
    }
    
    // Core agent functions
    KernelResult Initialize() override;
    KernelResult ExecuteTask(const std::vector<uint8_t>& task_data) override;
    void ProcessMessage(const AgentMessage& message) override;
    void LearnFromExperience(const std::vector<uint8_t>& experience_data) override;
    void AdaptToEnvironment(const std::vector<uint8_t>& environment_data) override;
    
    // Security capabilities
    KernelResult DetectThreats(const SecurityData& data, const SecurityContext& context);
    KernelResult RespondToIncident(const SecurityIncident& incident, const SecurityContext& context);
    KernelResult AnalyzeMalware(const MalwareSample& sample, const SecurityContext& context);
    KernelResult ScanVulnerabilities(const VulnerabilityTarget& target, const SecurityContext& context);
    KernelResult MonitorBehavior(const BehaviorData& data, const SecurityContext& context);
    KernelResult PerformForensics(const ForensicTarget& target, const SecurityContext& context);
    
    // Security management
    KernelResult EnableCapability(SecurityCapability capability);
    KernelResult DisableCapability(SecurityCapability capability);
    bool IsCapabilityEnabled(SecurityCapability capability);
    std::vector<SecurityCapability> GetEnabledCapabilities();
    
    // Context management
    KernelResult SetSecurityContext(const std::string& context_id, const SecurityContext& context);
    KernelResult GetSecurityContext(const std::string& context_id, SecurityContext& context);
    KernelResult UpdateSecurityContext(const std::string& context_id, const std::map<std::string, std::string>& updates);
    
    // Performance monitoring
    SecurityMetrics GetMetrics() const;
    void ResetMetrics();
    void GenerateSecurityReport();
    
protected:
    // Internal security functions
    virtual void MainLoop() override;
    virtual void ProcessTask(const std::vector<uint8_t>& task_data) override;
    virtual void HandleMessage(const AgentMessage& message) override;
    virtual void PerformLearning() override;
    virtual void UpdateState() override;
    
private:
    // Security implementations
    KernelResult ExecuteThreatDetection(const std::vector<uint8_t>& threat_data);
    KernelResult ExecuteIncidentResponse(const std::vector<uint8_t>& incident_data);
    KernelResult ExecuteMalwareAnalysis(const std::vector<uint8_t>& malware_data);
    KernelResult ExecuteVulnerabilityScanning(const std::vector<uint8_t>& scan_data);
    KernelResult ExecuteBehavioralAnalysis(const std::vector<uint8_t>& behavior_data);
    
    // Security utility functions
    float CalculateThreatScore(const std::vector<uint8_t>& threat_data);
    void AnalyzeAttackPattern(const std::vector<uint8_t>& pattern_data);
    void UpdateThreatModel(const std::string& threat_id, const std::vector<uint8_t>& threat_data);
    void OptimizeSecurityStrategy(const std::vector<uint8_t>& strategy_data);
    
    // Utility functions
    SecurityContext SelectBestContext(const std::string& task_description);
    void LogSecurityOperation(const std::string& operation, const std::string& details);
};

// Forward declarations for security engine components
class ThreatDetector;
class IntrusionDetector;
class MalwareAnalyzer;
class VulnerabilityScanner;
class IncidentResponder;
class ForensicAnalyzer;

// Security data structures
struct SecurityData {
    std::string data_id;
    std::string data_type;
    std::vector<uint8_t> raw_data;
    std::map<std::string, float> metadata;
    uint64_t timestamp;
    std::string source;
};

struct SecurityIncident {
    std::string incident_id;
    std::string incident_type;
    std::string severity_level;
    std::vector<std::string> affected_assets;
    std::map<std::string, float> incident_metrics;
    uint64_t detection_time;
    uint64_t response_time;
    std::vector<std::string> response_actions;
};

struct MalwareSample {
    std::string sample_id;
    std::string malware_type;
    std::vector<uint8_t> sample_data;
    std::map<std::string, float> behavioral_indicators;
    std::vector<std::string> signatures;
    float confidence_score;
    uint64_t analysis_time;
};

struct VulnerabilityTarget {
    std::string target_id;
    std::string target_type;
    std::vector<std::string> scan_parameters;
    std::map<std::string, float> vulnerability_metrics;
    std::vector<std::string> known_vulnerabilities;
    float risk_score;
};

struct BehaviorData {
    std::string behavior_id;
    std::string entity_id;
    std::vector<uint8_t> behavior_data;
    std::map<std::string, float> behavioral_indicators;
    std::vector<std::string> anomalies;
    uint64_t observation_time;
};

struct ForensicTarget {
    std::string target_id;
    std::string target_type;
    std::vector<uint8_t> forensic_data;
    std::map<std::string, float> forensic_metrics;
    std::vector<std::string> evidence_types;
    uint64_t collection_time;
};

struct ThreatModel {
    std::string threat_id;
    std::string threat_type;
    std::map<std::string, float> threat_indicators;
    std::vector<std::string> attack_vectors;
    float risk_score;
    std::vector<std::string> mitigation_strategies;
    uint64_t last_updated;
};

struct SecurityPolicy {
    std::string policy_id;
    std::string policy_type;
    std::map<std::string, std::string> policy_rules;
    std::vector<std::string> enforcement_actions;
    float compliance_level;
    uint64_t last_reviewed;
};

} // namespace AI
} // namespace AgenticOS