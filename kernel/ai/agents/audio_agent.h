#pragma once

#include "../multi_agent_system.h"
#include "../agent_wire_protocol.h"
#include <memory>
#include <vector>
#include <map>

namespace AgenticOS {
namespace AI {

// Audio Agent - Handles audio processing, speech recognition, and sound analysis
class AudioAgent : public BaseAgent {
private:
    // Audio processing components
    struct AudioEngine {
        std::unique_ptr<SpeechRecognizer> speech_recognizer;
        std::unique_ptr<TextToSpeech> text_to_speech;
        std::unique_ptr<AudioAnalyzer> audio_analyzer;
        std::unique_ptr<NoiseReducer> noise_reducer;
        std::unique_ptr<AudioEnhancer> audio_enhancer;
        std::unique_ptr<MusicAnalyzer> music_analyzer;
    };
    
    // Audio capabilities
    enum class AudioCapability {
        SPEECH_RECOGNITION,
        TEXT_TO_SPEECH,
        NOISE_REDUCTION,
        AUDIO_ENHANCEMENT,
        MUSIC_ANALYSIS,
        EMOTION_DETECTION,
        SPEAKER_IDENTIFICATION,
        LANGUAGE_DETECTION,
        ACCENT_RECOGNITION,
        SOUND_CLASSIFICATION,
        AUDIO_SEGMENTATION,
        FEATURE_EXTRACTION,
        PATTERN_RECOGNITION,
        FREQUENCY_ANALYSIS,
        AMPLITUDE_ANALYSIS,
        PHASE_ANALYSIS
    };
    
    // Audio processing context
    struct AudioContext {
        std::string audio_format;
        uint32_t sample_rate;
        uint32_t channels;
        uint32_t bit_depth;
        std::vector<AudioCapability> required_capabilities;
        float confidence_threshold;
        uint64_t processing_timeout;
        bool enable_real_time;
        bool preserve_quality;
    };
    
    // Core components
    std::unique_ptr<AudioEngine> audio_engine;
    std::map<AudioCapability, bool> capability_status;
    std::map<std::string, AudioContext> context_cache;
    
    // Performance tracking
    struct AudioMetrics {
        uint64_t audio_segments_processed;
        uint64_t speech_recognitions;
        uint64_t text_to_speech_conversions;
        uint64_t noise_reductions;
        float average_accuracy;
        uint64_t average_processing_time;
        std::map<AudioCapability, uint64_t> capability_usage;
        std::vector<std::string> recent_operations;
    };
    
    AudioMetrics metrics;
    
public:
    AudioAgent(uint32_t id) : BaseAgent(id, "AudioAgent", AgentSpecialization::AUDIO_AGENT) {
        audio_engine = std::make_unique<AudioEngine>();
    }
    
    // Core agent functions
    KernelResult Initialize() override;
    KernelResult ExecuteTask(const std::vector<uint8_t>& task_data) override;
    void ProcessMessage(const AgentMessage& message) override;
    void LearnFromExperience(const std::vector<uint8_t>& experience_data) override;
    void AdaptToEnvironment(const std::vector<uint8_t>& environment_data) override;
    
    // Audio processing capabilities
    KernelResult ProcessAudio(const std::vector<uint8_t>& audio_data, const AudioContext& context, std::vector<uint8_t>& result);
    KernelResult RecognizeSpeech(const std::vector<uint8_t>& audio_data, std::string& recognized_text);
    KernelResult SynthesizeSpeech(const std::string& text, const std::string& voice, std::vector<uint8_t>& audio_output);
    KernelResult AnalyzeAudio(const std::vector<uint8_t>& audio_data, AudioAnalysis& analysis);
    KernelResult ReduceNoise(const std::vector<uint8_t>& audio_data, std::vector<uint8_t>& cleaned_audio);
    KernelResult EnhanceAudio(const std::vector<uint8_t>& audio_data, std::vector<uint8_t>& enhanced_audio);
    
    // Audio management
    KernelResult EnableCapability(AudioCapability capability);
    KernelResult DisableCapability(AudioCapability capability);
    bool IsCapabilityEnabled(AudioCapability capability);
    std::vector<AudioCapability> GetEnabledCapabilities();
    
    // Context management
    KernelResult SetAudioContext(const std::string& context_id, const AudioContext& context);
    KernelResult GetAudioContext(const std::string& context_id, AudioContext& context);
    KernelResult UpdateAudioContext(const std::string& context_id, const std::map<std::string, std::string>& updates);
    
    // Performance monitoring
    AudioMetrics GetMetrics() const;
    void ResetMetrics();
    void GenerateAudioReport();
    
protected:
    // Internal audio functions
    virtual void MainLoop() override;
    virtual void ProcessTask(const std::vector<uint8_t>& task_data) override;
    virtual void HandleMessage(const AgentMessage& message) override;
    virtual void PerformLearning() override;
    virtual void UpdateState() override;
    
private:
    // Audio processing implementations
    KernelResult ExecuteSpeechRecognition(const std::vector<uint8_t>& audio_data);
    KernelResult ExecuteTextToSpeech(const std::vector<uint8_t>& text_data);
    KernelResult ExecuteAudioAnalysis(const std::vector<uint8_t>& audio_data);
    KernelResult ExecuteNoiseReduction(const std::vector<uint8_t>& audio_data);
    KernelResult ExecuteAudioEnhancement(const std::vector<uint8_t>& audio_data);
    
    // Audio utility functions
    void PreprocessAudio(const std::vector<uint8_t>& input, std::vector<uint8_t>& output);
    void PostprocessAudio(const std::vector<uint8_t>& input, std::vector<uint8_t>& output);
    float CalculateAudioQuality(const std::vector<uint8_t>& audio_data);
    void OptimizeAudioParameters(const std::vector<uint8_t>& input, std::vector<uint8_t>& output);
    
    // Utility functions
    AudioContext SelectBestContext(const std::string& task_description);
    void LogAudioOperation(const std::string& operation, const std::string& details);
};

// Forward declarations for audio engine components
class SpeechRecognizer;
class TextToSpeech;
class AudioAnalyzer;
class NoiseReducer;
class AudioEnhancer;
class MusicAnalyzer;

// Audio data structures
struct AudioAnalysis {
    std::string audio_type;
    float confidence;
    std::vector<float> frequency_spectrum;
    std::map<std::string, float> audio_features;
    std::vector<std::string> detected_sounds;
    float overall_quality;
};

struct SpeechRecognition {
    std::string recognized_text;
    float confidence;
    std::string language;
    std::string speaker_id;
    std::map<std::string, float> emotions;
    uint64_t timestamp;
};

struct AudioEnhancement {
    std::vector<uint8_t> enhanced_audio;
    float improvement_score;
    std::map<std::string, float> enhancement_metrics;
    std::vector<std::string> applied_filters;
};

struct MusicAnalysis {
    std::string genre;
    float tempo;
    std::string key;
    std::vector<std::string> instruments;
    std::map<std::string, float> musical_features;
    float complexity_score;
};

} // namespace AI
} // namespace AgenticOS