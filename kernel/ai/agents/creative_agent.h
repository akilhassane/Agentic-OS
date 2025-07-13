#pragma once

#include "../multi_agent_system.h"
#include "../agent_wire_protocol.h"
#include <memory>
#include <vector>
#include <map>

namespace AgenticOS {
namespace AI {

// Creative Agent - Handles artistic creation, innovation, and creative problem solving
class CreativeAgent : public BaseAgent {
private:
    // Creative domains
    enum class CreativeDomain {
        VISUAL_ART,
        MUSIC,
        LITERATURE,
        DESIGN,
        INNOVATION,
        STORYTELLING,
        POETRY,
        ARCHITECTURE,
        FASHION,
        CULINARY,
        GAME_DESIGN,
        FILM,
        PHOTOGRAPHY,
        SCULPTURE,
        DANCE,
        THEATER
    };
    
    // Creative styles
    struct CreativeStyle {
        std::string style_id;
        std::string style_name;
        std::vector<std::string> characteristics;
        std::map<std::string, float> style_parameters;
        std::vector<std::string> influences;
        float uniqueness_score;
        uint64_t usage_count;
    };
    
    // Creative process
    struct CreativeProcess {
        std::string process_id;
        CreativeDomain domain;
        std::vector<CreativeStyle> applied_styles;
        std::vector<std::string> inspiration_sources;
        std::vector<std::string> constraints;
        std::vector<std::string> objectives;
        float creativity_score;
        uint64_t iteration_count;
    };
    
    // Creative tools
    struct CreativeTools {
        std::unique_ptr<ArtGenerator> art_generator;
        std::unique_ptr<MusicComposer> music_composer;
        std::unique_ptr<StoryGenerator> story_generator;
        std::unique_ptr<DesignEngine> design_engine;
        std::unique_ptr<InnovationEngine> innovation_engine;
        std::unique_ptr<StyleAnalyzer> style_analyzer;
    };
    
    // Core components
    std::unique_ptr<CreativeTools> creative_tools;
    std::map<CreativeDomain, std::vector<CreativeStyle>> domain_styles;
    std::vector<CreativeProcess> active_processes;
    
    // Performance tracking
    struct CreativeMetrics {
        uint64_t artworks_created;
        uint64_t music_pieces_composed;
        uint64_t stories_written;
        uint64_t designs_generated;
        uint64_t innovations_conceived;
        float average_creativity_score;
        std::map<CreativeDomain, uint64_t> domain_usage;
        std::vector<std::string> recent_creations;
    };
    
    CreativeMetrics metrics;
    
public:
    CreativeAgent(uint32_t id) : BaseAgent(id, "CreativeAgent", AgentSpecialization::CREATIVE_AGENT) {
        creative_tools = std::make_unique<CreativeTools>();
    }
    
    // Core agent functions
    KernelResult Initialize() override;
    KernelResult ExecuteTask(const std::vector<uint8_t>& task_data) override;
    void ProcessMessage(const AgentMessage& message) override;
    void LearnFromExperience(const std::vector<uint8_t>& experience_data) override;
    void AdaptToEnvironment(const std::vector<uint8_t>& environment_data) override;
    
    // Creative capabilities
    KernelResult CreateArtwork(const std::string& description, const std::vector<uint8_t>& style_data);
    KernelResult ComposeMusic(const std::string& genre, const std::vector<uint8_t>& mood_data);
    KernelResult WriteStory(const std::string& genre, const std::vector<uint8_t>& plot_data);
    KernelResult GenerateDesign(const std::string& design_type, const std::vector<uint8_t>& requirements);
    KernelResult InnovateSolution(const std::string& problem, const std::vector<uint8_t>& constraints);
    KernelResult CreatePoetry(const std::string& style, const std::vector<uint8_t>& theme_data);
    
    // Style management
    KernelResult AddCreativeStyle(const CreativeStyle& style, CreativeDomain domain);
    KernelResult RemoveCreativeStyle(const std::string& style_id);
    std::vector<CreativeStyle> GetStylesForDomain(CreativeDomain domain);
    KernelResult AnalyzeStyle(const std::vector<uint8_t>& artwork_data, CreativeStyle& detected_style);
    
    // Creative process management
    KernelResult StartCreativeProcess(const CreativeProcess& process);
    KernelResult IterateCreativeProcess(const std::string& process_id, const std::vector<uint8_t>& feedback);
    KernelResult CompleteCreativeProcess(const std::string& process_id, std::vector<uint8_t>& result);
    
    // Performance monitoring
    CreativeMetrics GetMetrics() const;
    void ResetMetrics();
    void GenerateCreativeReport();
    
protected:
    // Internal creative functions
    virtual void MainLoop() override;
    virtual void ProcessTask(const std::vector<uint8_t>& task_data) override;
    virtual void HandleMessage(const AgentMessage& message) override;
    virtual void PerformLearning() override;
    virtual void UpdateState() override;
    
private:
    // Creative tool implementations
    KernelResult ExecuteArtCreation(const std::vector<uint8_t>& art_data);
    KernelResult ExecuteMusicComposition(const std::vector<uint8_t>& music_data);
    KernelResult ExecuteStoryWriting(const std::vector<uint8_t>& story_data);
    KernelResult ExecuteDesignGeneration(const std::vector<uint8_t>& design_data);
    KernelResult ExecuteInnovationProcess(const std::vector<uint8_t>& innovation_data);
    
    // Creative process functions
    void GenerateInspiration(const CreativeDomain domain, std::vector<std::string>& inspiration);
    void ApplyCreativeConstraints(const std::vector<std::string>& constraints, std::vector<uint8_t>& result);
    float EvaluateCreativity(const std::vector<uint8_t>& creation_data);
    void OptimizeCreativeOutput(const std::vector<uint8_t>& initial_creation, std::vector<uint8_t>& optimized);
    
    // Utility functions
    CreativeDomain DetermineDomain(const std::string& task_description);
    CreativeStyle SelectBestStyle(const CreativeDomain domain, const std::vector<uint8_t>& requirements);
    void LogCreativeStep(const std::string& step_description);
};

// Forward declarations for creative tool components
class ArtGenerator;
class MusicComposer;
class StoryGenerator;
class DesignEngine;
class InnovationEngine;
class StyleAnalyzer;

} // namespace AI
} // namespace AgenticOS