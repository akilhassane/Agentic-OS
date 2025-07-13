#pragma once

#include "../multi_agent_system.h"
#include "../agent_wire_protocol.h"
#include <memory>
#include <vector>
#include <map>

namespace AgenticOS {
namespace AI {

// Neural Interface UI - Handles advanced user interface capabilities
class NeuralInterfaceUI {
private:
    // UI components
    struct UIEngine {
        std::unique_ptr<HolographicDisplay> holographic_display;
        std::unique_ptr<GestureRecognizer> gesture_recognizer;
        std::unique_ptr<VoiceInterface> voice_interface;
        std::unique_ptr<ImmersiveRenderer> immersive_renderer;
        std::unique_ptr<UIOptimizer> ui_optimizer;
        std::unique_ptr<AccessibilityManager> accessibility_manager;
    };
    
    // UI capabilities
    enum class UICapability {
        HOLOGRAPHIC_DISPLAY,
        GESTURE_RECOGNITION,
        VOICE_INTERFACE,
        IMMERSIVE_RENDERING,
        UI_OPTIMIZATION,
        ACCESSIBILITY_MANAGEMENT,
        BRAIN_COMPUTER_INTERFACE,
        EYE_TRACKING,
        EMOTION_DISPLAY,
        HAPTIC_FEEDBACK,
        AUGMENTED_REALITY,
        VIRTUAL_REALITY,
        MIXED_REALITY,
        NEURAL_VISUALIZATION,
        THOUGHT_DISPLAY,
        CONSCIOUSNESS_INTERFACE
    };
    
    // UI context
    struct UIContext {
        std::string interface_type;
        std::string display_mode;
        std::vector<std::string> available_modalities;
        std::vector<UICapability> required_capabilities;
        float responsiveness_threshold;
        uint64_t update_frequency;
        bool enable_adaptive_interface;
        bool enable_accessibility;
    };
    
    // Core components
    std::unique_ptr<UIEngine> ui_engine;
    std::map<UICapability, bool> capability_status;
    std::map<std::string, UIContext> context_cache;
    
    // Performance tracking
    struct UIMetrics {
        uint64_t interactions_handled;
        uint64_t gestures_recognized;
        uint64_t voice_commands;
        uint64_t holographic_displays;
        float average_response_time;
        float user_satisfaction_score;
        std::map<UICapability, uint64_t> capability_usage;
        std::vector<std::string> recent_ui_events;
    };
    
    UIMetrics metrics;
    
public:
    NeuralInterfaceUI() {
        ui_engine = std::make_unique<UIEngine>();
    }
    
    // Core UI functions
    KernelResult Initialize();
    KernelResult DisplayHologram(const HologramRequest& request, const UIContext& context);
    KernelResult RecognizeGesture(const GestureRequest& request, GestureData& gesture);
    KernelResult ProcessVoiceCommand(const VoiceRequest& request, VoiceResponse& response);
    KernelResult RenderImmersive(const ImmersiveRequest& request, const UIContext& context);
    KernelResult OptimizeInterface(const OptimizationRequest& request, OptimizationResult& result);
    KernelResult ManageAccessibility(const AccessibilityRequest& request, AccessibilityResult& result);
    
    // UI management
    KernelResult EnableCapability(UICapability capability);
    KernelResult DisableCapability(UICapability capability);
    bool IsCapabilityEnabled(UICapability capability);
    std::vector<UICapability> GetEnabledCapabilities();
    
    // Context management
    KernelResult SetUIContext(const std::string& context_id, const UIContext& context);
    KernelResult GetUIContext(const std::string& context_id, UIContext& context);
    KernelResult UpdateUIContext(const std::string& context_id, const std::map<std::string, std::string>& updates);
    
    // Performance monitoring
    UIMetrics GetMetrics() const;
    void ResetMetrics();
    void GenerateUIReport();
    
private:
    // UI implementations
    KernelResult ExecuteHolographicDisplay(const std::vector<uint8_t>& hologram_data);
    KernelResult ExecuteGestureRecognition(const std::vector<uint8_t>& gesture_data);
    KernelResult ExecuteVoiceProcessing(const std::vector<uint8_t>& voice_data);
    KernelResult ExecuteImmersiveRendering(const std::vector<uint8_t>& immersive_data);
    KernelResult ExecuteUIOptimization(const std::vector<uint8_t>& optimization_data);
    
    // UI utility functions
    float CalculateUIResponsiveness(const std::vector<uint8_t>& ui_data);
    void AnalyzeUserInteraction(const std::vector<uint8_t>& interaction_data);
    void UpdateUIModel(const std::string& ui_id, const std::vector<uint8_t>& ui_data);
    void OptimizeUIStrategy(const std::vector<uint8_t>& strategy_data);
    
    // Utility functions
    UIContext SelectBestContext(const std::string& task_description);
    void LogUIOperation(const std::string& operation, const std::string& details);
};

// Forward declarations for UI engine components
class HolographicDisplay;
class GestureRecognizer;
class VoiceInterface;
class ImmersiveRenderer;
class UIOptimizer;
class AccessibilityManager;

// UI data structures
struct HologramRequest {
    std::string request_id;
    std::string hologram_type;
    std::vector<uint8_t> hologram_data;
    std::map<std::string, float> display_parameters;
    uint64_t duration;
    float priority;
};

struct GestureRequest {
    std::string request_id;
    std::string gesture_type;
    std::vector<uint8_t> gesture_data;
    std::map<std::string, float> recognition_parameters;
    uint64_t timeout;
    float confidence_threshold;
};

struct GestureData {
    std::string gesture_id;
    std::string gesture_type;
    std::map<std::string, float> gesture_parameters;
    float confidence_score;
    uint64_t timestamp;
    std::string gesture_location;
    std::vector<std::string> associated_actions;
};

struct VoiceRequest {
    std::string request_id;
    std::string command_type;
    std::vector<uint8_t> voice_data;
    std::map<std::string, float> processing_parameters;
    uint64_t timeout;
    float accuracy_threshold;
};

struct VoiceResponse {
    std::string response_id;
    std::string request_id;
    std::string recognized_command;
    std::map<std::string, float> response_metrics;
    float confidence_score;
    uint64_t processing_time;
    std::string response_action;
};

struct ImmersiveRequest {
    std::string request_id;
    std::string immersive_type;
    std::vector<uint8_t> immersive_data;
    std::map<std::string, float> rendering_parameters;
    uint64_t duration;
    float immersion_level;
};

struct OptimizationRequest {
    std::string request_id;
    std::string optimization_type;
    std::vector<std::string> target_components;
    std::map<std::string, float> optimization_parameters;
    float target_performance;
    uint64_t timeout;
};

struct OptimizationResult {
    std::string result_id;
    std::string request_id;
    std::map<std::string, float> optimization_metrics;
    float performance_improvement;
    uint64_t optimization_time;
    std::vector<std::string> applied_optimizations;
};

struct AccessibilityRequest {
    std::string request_id;
    std::string accessibility_type;
    std::vector<std::string> accessibility_features;
    std::map<std::string, float> accessibility_parameters;
    uint64_t timeout;
    bool enable_adaptive_features;
};

struct AccessibilityResult {
    std::string result_id;
    std::string request_id;
    std::map<std::string, float> accessibility_metrics;
    float accessibility_score;
    uint64_t implementation_time;
    std::vector<std::string> enabled_features;
};

struct HolographicDisplay {
    std::string display_id;
    std::string display_type;
    std::vector<std::string> supported_formats;
    std::map<std::string, float> display_parameters;
    float resolution;
    uint64_t refresh_rate;
};

struct UserInteraction {
    std::string interaction_id;
    std::string interaction_type;
    std::map<std::string, float> interaction_parameters;
    uint64_t timestamp;
    std::string user_id;
    float interaction_duration;
};

struct InterfaceElement {
    std::string element_id;
    std::string element_type;
    std::map<std::string, float> element_properties;
    std::vector<std::string> element_actions;
    float visibility_score;
    uint64_t last_accessed;
};

} // namespace AI
} // namespace AgenticOS