#pragma once

#include "../multi_agent_system.h"
#include "../agent_wire_protocol.h"
#include <memory>
#include <vector>
#include <map>

namespace AgenticOS {
namespace AI {

// Neural Shell - Handles direct brain-computer interface and neural communication
class NeuralShell {
private:
    // Neural interface components
    struct NeuralInterface {
        std::unique_ptr<BrainInterface> brain_interface;
        std::unique_ptr<NeuralDecoder> neural_decoder;
        std::unique_ptr<NeuralEncoder> neural_encoder;
        std::unique_ptr<NeuralProcessor> neural_processor;
        std::unique_ptr<NeuralMonitor> neural_monitor;
        std::unique_ptr<NeuralSafety> neural_safety;
    };
    
    // Neural capabilities
    enum class NeuralCapability {
        BRAIN_INTERFACE,
        NEURAL_DECODING,
        NEURAL_ENCODING,
        NEURAL_PROCESSING,
        NEURAL_MONITORING,
        NEURAL_SAFETY,
        THOUGHT_READING,
        THOUGHT_WRITING,
        EMOTION_DETECTION,
        EMOTION_SYNTHESIS,
        MEMORY_ACCESS,
        MEMORY_WRITING,
        CONSCIOUSNESS_MONITORING,
        SUBCONSCIOUS_ACCESS,
        DREAM_INTERFACE,
        NEURAL_LEARNING
    };
    
    // Neural context
    struct NeuralContext {
        std::string interface_type;
        std::string brain_region;
        std::vector<std::string> neural_channels;
        std::vector<NeuralCapability> required_capabilities;
        float safety_threshold;
        uint64_t processing_timeout;
        bool enable_real_time;
        bool enable_safety_protocols;
    };
    
    // Core components
    std::unique_ptr<NeuralInterface> neural_interface;
    std::map<NeuralCapability, bool> capability_status;
    std::map<std::string, NeuralContext> context_cache;
    
    // Performance tracking
    struct NeuralMetrics {
        uint64_t neural_signals_processed;
        uint64_t thoughts_decoded;
        uint64_t emotions_detected;
        uint64_t memories_accessed;
        float average_accuracy;
        float safety_compliance;
        std::map<NeuralCapability, uint64_t> capability_usage;
        std::vector<std::string> recent_neural_events;
    };
    
    NeuralMetrics metrics;
    
public:
    NeuralShell() {
        neural_interface = std::make_unique<NeuralInterface>();
    }
    
    // Core neural functions
    KernelResult Initialize();
    KernelResult ReadThoughts(const NeuralRequest& request, ThoughtData& thoughts);
    KernelResult WriteThoughts(const ThoughtData& thoughts, const NeuralContext& context);
    KernelResult DetectEmotions(const EmotionRequest& request, EmotionData& emotions);
    KernelResult SynthesizeEmotions(const EmotionData& emotions, const NeuralContext& context);
    KernelResult AccessMemory(const MemoryRequest& request, MemoryData& memory);
    KernelResult WriteMemory(const MemoryData& memory, const NeuralContext& context);
    
    // Neural management
    KernelResult EnableCapability(NeuralCapability capability);
    KernelResult DisableCapability(NeuralCapability capability);
    bool IsCapabilityEnabled(NeuralCapability capability);
    std::vector<NeuralCapability> GetEnabledCapabilities();
    
    // Context management
    KernelResult SetNeuralContext(const std::string& context_id, const NeuralContext& context);
    KernelResult GetNeuralContext(const std::string& context_id, NeuralContext& context);
    KernelResult UpdateNeuralContext(const std::string& context_id, const std::map<std::string, std::string>& updates);
    
    // Performance monitoring
    NeuralMetrics GetMetrics() const;
    void ResetMetrics();
    void GenerateNeuralReport();
    
private:
    // Neural implementations
    KernelResult ExecuteThoughtReading(const std::vector<uint8_t>& neural_data);
    KernelResult ExecuteThoughtWriting(const std::vector<uint8_t>& thought_data);
    KernelResult ExecuteEmotionDetection(const std::vector<uint8_t>& emotion_data);
    KernelResult ExecuteEmotionSynthesis(const std::vector<uint8_t>& synthesis_data);
    KernelResult ExecuteMemoryAccess(const std::vector<uint8_t>& memory_data);
    
    // Neural utility functions
    float CalculateNeuralAccuracy(const std::vector<uint8_t>& neural_data);
    void AnalyzeNeuralPatterns(const std::vector<uint8_t>& pattern_data);
    void UpdateNeuralModel(const std::string& neural_id, const std::vector<uint8_t>& neural_data);
    void OptimizeNeuralStrategy(const std::vector<uint8_t>& strategy_data);
    
    // Utility functions
    NeuralContext SelectBestContext(const std::string& task_description);
    void LogNeuralOperation(const std::string& operation, const std::string& details);
};

// Forward declarations for neural interface components
class BrainInterface;
class NeuralDecoder;
class NeuralEncoder;
class NeuralProcessor;
class NeuralMonitor;
class NeuralSafety;

// Neural data structures
struct NeuralRequest {
    std::string request_id;
    std::string request_type;
    std::vector<std::string> brain_regions;
    std::map<std::string, float> request_parameters;
    uint64_t timeout;
    float confidence_threshold;
};

struct ThoughtData {
    std::string thought_id;
    std::string thought_content;
    std::string thought_type;
    std::map<std::string, float> thought_metadata;
    float confidence_score;
    uint64_t timestamp;
    std::string brain_region;
    std::vector<std::string> associated_emotions;
};

struct EmotionRequest {
    std::string request_id;
    std::string emotion_type;
    std::vector<std::string> brain_regions;
    std::map<std::string, float> request_parameters;
    uint64_t timeout;
    float sensitivity_threshold;
};

struct EmotionData {
    std::string emotion_id;
    std::string emotion_type;
    float intensity;
    std::map<std::string, float> emotion_components;
    uint64_t timestamp;
    std::string brain_region;
    std::vector<std::string> associated_thoughts;
};

struct MemoryRequest {
    std::string request_id;
    std::string memory_type;
    std::vector<std::string> memory_cues;
    std::map<std::string, float> request_parameters;
    uint64_t timeout;
    float recall_threshold;
};

struct MemoryData {
    std::string memory_id;
    std::string memory_content;
    std::string memory_type;
    std::map<std::string, float> memory_metadata;
    float vividness_score;
    uint64_t timestamp;
    std::string brain_region;
    std::vector<std::string> associated_emotions;
};

struct NeuralSignal {
    std::string signal_id;
    std::string signal_type;
    std::vector<float> signal_data;
    std::map<std::string, float> signal_metadata;
    uint64_t timestamp;
    std::string brain_region;
    float signal_strength;
};

struct BrainRegion {
    std::string region_id;
    std::string region_name;
    std::vector<std::string> functions;
    std::map<std::string, float> activity_levels;
    std::vector<std::string> connections;
    uint64_t last_accessed;
};

struct NeuralSafetyProtocol {
    std::string protocol_id;
    std::string protocol_type;
    std::map<std::string, std::string> safety_rules;
    std::vector<std::string> emergency_actions;
    float safety_threshold;
    uint64_t last_reviewed;
};

} // namespace AI
} // namespace AgenticOS