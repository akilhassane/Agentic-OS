#pragma once

#include "../multi_agent_system.h"
#include "../agent_wire_protocol.h"
#include <memory>
#include <vector>
#include <map>

namespace AgenticOS {
namespace AI {

// Vision Agent - Handles computer vision, image processing, and visual recognition
class VisionAgent : public BaseAgent {
private:
    // Vision processing components
    struct VisionEngine {
        std::unique_ptr<ImageProcessor> image_processor;
        std::unique_ptr<ObjectDetector> object_detector;
        std::unique_ptr<FaceRecognizer> face_recognizer;
        std::unique_ptr<SceneAnalyzer> scene_analyzer;
        std::unique_ptr<OpticalFlowTracker> optical_flow_tracker;
        std::unique_ptr<DepthEstimator> depth_estimator;
    };
    
    // Vision capabilities
    enum class VisionCapability {
        OBJECT_DETECTION,
        FACE_RECOGNITION,
        SCENE_UNDERSTANDING,
        OPTICAL_CHARACTER_RECOGNITION,
        MOTION_TRACKING,
        DEPTH_ESTIMATION,
        STEREO_VISION,
        PANORAMIC_STITCHING,
        IMAGE_SEGMENTATION,
        FEATURE_EXTRACTION,
        PATTERN_RECOGNITION,
        COLOR_ANALYSIS,
        TEXTURE_ANALYSIS,
        EDGE_DETECTION,
        CORNER_DETECTION,
        BLOB_DETECTION
    };
    
    // Image processing context
    struct VisionContext {
        std::string image_format;
        uint32_t image_width;
        uint32_t image_height;
        uint32_t channels;
        std::vector<VisionCapability> required_capabilities;
        float confidence_threshold;
        uint64_t processing_timeout;
        bool enable_real_time;
        bool preserve_quality;
    };
    
    // Core components
    std::unique_ptr<VisionEngine> vision_engine;
    std::map<VisionCapability, bool> capability_status;
    std::map<std::string, VisionContext> context_cache;
    
    // Performance tracking
    struct VisionMetrics {
        uint64_t images_processed;
        uint64_t objects_detected;
        uint64_t faces_recognized;
        uint64_t scenes_analyzed;
        float average_accuracy;
        uint64_t average_processing_time;
        std::map<VisionCapability, uint64_t> capability_usage;
        std::vector<std::string> recent_operations;
    };
    
    VisionMetrics metrics;
    
public:
    VisionAgent(uint32_t id) : BaseAgent(id, "VisionAgent", AgentSpecialization::VISION_AGENT) {
        vision_engine = std::make_unique<VisionEngine>();
    }
    
    // Core agent functions
    KernelResult Initialize() override;
    KernelResult ExecuteTask(const std::vector<uint8_t>& task_data) override;
    void ProcessMessage(const AgentMessage& message) override;
    void LearnFromExperience(const std::vector<uint8_t>& experience_data) override;
    void AdaptToEnvironment(const std::vector<uint8_t>& environment_data) override;
    
    // Vision processing capabilities
    KernelResult ProcessImage(const std::vector<uint8_t>& image_data, const VisionContext& context, std::vector<uint8_t>& result);
    KernelResult DetectObjects(const std::vector<uint8_t>& image_data, std::vector<ObjectDetection>& detections);
    KernelResult RecognizeFaces(const std::vector<uint8_t>& image_data, std::vector<FaceRecognition>& recognitions);
    KernelResult AnalyzeScene(const std::vector<uint8_t>& image_data, SceneAnalysis& analysis);
    KernelResult ExtractText(const std::vector<uint8_t>& image_data, std::string& extracted_text);
    KernelResult TrackMotion(const std::vector<uint8_t>& video_data, std::vector<MotionTrack>& tracks);
    
    // Vision management
    KernelResult EnableCapability(VisionCapability capability);
    KernelResult DisableCapability(VisionCapability capability);
    bool IsCapabilityEnabled(VisionCapability capability);
    std::vector<VisionCapability> GetEnabledCapabilities();
    
    // Context management
    KernelResult SetVisionContext(const std::string& context_id, const VisionContext& context);
    KernelResult GetVisionContext(const std::string& context_id, VisionContext& context);
    KernelResult UpdateVisionContext(const std::string& context_id, const std::map<std::string, std::string>& updates);
    
    // Performance monitoring
    VisionMetrics GetMetrics() const;
    void ResetMetrics();
    void GenerateVisionReport();
    
protected:
    // Internal vision functions
    virtual void MainLoop() override;
    virtual void ProcessTask(const std::vector<uint8_t>& task_data) override;
    virtual void HandleMessage(const AgentMessage& message) override;
    virtual void PerformLearning() override;
    virtual void UpdateState() override;
    
private:
    // Vision processing implementations
    KernelResult ExecuteObjectDetection(const std::vector<uint8_t>& image_data);
    KernelResult ExecuteFaceRecognition(const std::vector<uint8_t>& image_data);
    KernelResult ExecuteSceneAnalysis(const std::vector<uint8_t>& image_data);
    KernelResult ExecuteTextExtraction(const std::vector<uint8_t>& image_data);
    KernelResult ExecuteMotionTracking(const std::vector<uint8_t>& video_data);
    
    // Vision utility functions
    void PreprocessImage(const std::vector<uint8_t>& input, std::vector<uint8_t>& output);
    void PostprocessResults(const std::vector<uint8_t>& input, std::vector<uint8_t>& output);
    float CalculateConfidence(const std::vector<uint8_t>& detection_data);
    void OptimizeImageQuality(const std::vector<uint8_t>& input, std::vector<uint8_t>& output);
    
    // Utility functions
    VisionContext SelectBestContext(const std::string& task_description);
    void LogVisionOperation(const std::string& operation, const std::string& details);
};

// Forward declarations for vision engine components
class ImageProcessor;
class ObjectDetector;
class FaceRecognizer;
class SceneAnalyzer;
class OpticalFlowTracker;
class DepthEstimator;

// Vision data structures
struct ObjectDetection {
    std::string object_class;
    float confidence;
    uint32_t x, y, width, height;
    std::vector<float> bounding_box;
    std::map<std::string, float> attributes;
};

struct FaceRecognition {
    std::string person_id;
    float confidence;
    uint32_t x, y, width, height;
    std::vector<float> facial_features;
    std::map<std::string, float> emotions;
};

struct SceneAnalysis {
    std::string scene_type;
    float confidence;
    std::vector<std::string> objects_present;
    std::map<std::string, float> scene_attributes;
    std::vector<float> depth_map;
};

struct MotionTrack {
    uint32_t track_id;
    std::vector<uint32_t> positions;
    std::vector<uint64_t> timestamps;
    std::string object_class;
    float confidence;
};

} // namespace AI
} // namespace AgenticOS