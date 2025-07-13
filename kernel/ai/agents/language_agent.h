#pragma once

#include "../multi_agent_system.h"
#include "../agent_wire_protocol.h"
#include <memory>
#include <vector>
#include <map>

namespace AgenticOS {
namespace AI {

// Language Agent - Handles natural language processing, translation, and communication
class LanguageAgent : public BaseAgent {
private:
    // Language processing components
    struct LanguageEngine {
        std::unique_ptr<NLPParser> nlp_parser;
        std::unique_ptr<TranslationEngine> translation_engine;
        std::unique_ptr<SentimentAnalyzer> sentiment_analyzer;
        std::unique_ptr<TextGenerator> text_generator;
        std::unique_ptr<LanguageModel> language_model;
        std::unique_ptr<GrammarChecker> grammar_checker;
    };
    
    // Supported languages
    struct LanguageSupport {
        std::string language_code;
        std::string language_name;
        float proficiency_level;
        std::vector<std::string> dialects;
        std::map<std::string, float> dialect_proficiency;
        bool is_native_speaker;
    };
    
    // Language processing context
    struct LanguageContext {
        std::string source_language;
        std::string target_language;
        std::string domain_context;
        std::string formality_level;
        std::map<std::string, std::string> cultural_context;
        std::vector<std::string> specialized_terminology;
        bool preserve_style;
        bool maintain_tone;
    };
    
    // Core components
    std::unique_ptr<LanguageEngine> language_engine;
    std::map<std::string, LanguageSupport> supported_languages;
    std::map<std::string, LanguageContext> context_cache;
    
    // Performance tracking
    struct LanguageMetrics {
        uint64_t texts_processed;
        uint64_t translations_performed;
        uint64_t conversations_handled;
        uint64_t documents_analyzed;
        float average_accuracy;
        std::map<std::string, uint64_t> language_usage;
        std::vector<std::string> recent_interactions;
    };
    
    LanguageMetrics metrics;
    
public:
    LanguageAgent(uint32_t id) : BaseAgent(id, "LanguageAgent", AgentSpecialization::LANGUAGE_AGENT) {
        language_engine = std::make_unique<LanguageEngine>();
    }
    
    // Core agent functions
    KernelResult Initialize() override;
    KernelResult ExecuteTask(const std::vector<uint8_t>& task_data) override;
    void ProcessMessage(const AgentMessage& message) override;
    void LearnFromExperience(const std::vector<uint8_t>& experience_data) override;
    void AdaptToEnvironment(const std::vector<uint8_t>& environment_data) override;
    
    // Language processing capabilities
    KernelResult ProcessText(const std::string& text, const std::string& language, std::vector<uint8_t>& result);
    KernelResult TranslateText(const std::string& text, const std::string& source_lang, 
                              const std::string& target_lang, std::string& translation);
    KernelResult AnalyzeSentiment(const std::string& text, float& sentiment_score, std::string& sentiment_label);
    KernelResult GenerateText(const std::string& prompt, const std::string& style, std::string& generated_text);
    KernelResult CheckGrammar(const std::string& text, std::vector<std::string>& corrections);
    KernelResult ExtractEntities(const std::string& text, std::vector<std::string>& entities);
    
    // Language management
    KernelResult AddLanguageSupport(const LanguageSupport& language);
    KernelResult RemoveLanguageSupport(const std::string& language_code);
    std::vector<LanguageSupport> GetSupportedLanguages();
    float GetLanguageProficiency(const std::string& language_code);
    
    // Context management
    KernelResult SetLanguageContext(const std::string& context_id, const LanguageContext& context);
    KernelResult GetLanguageContext(const std::string& context_id, LanguageContext& context);
    KernelResult UpdateLanguageContext(const std::string& context_id, const std::map<std::string, std::string>& updates);
    
    // Performance monitoring
    LanguageMetrics GetMetrics() const;
    void ResetMetrics();
    void GenerateLanguageReport();
    
protected:
    // Internal language functions
    virtual void MainLoop() override;
    virtual void ProcessTask(const std::vector<uint8_t>& task_data) override;
    virtual void HandleMessage(const AgentMessage& message) override;
    virtual void PerformLearning() override;
    virtual void UpdateState() override;
    
private:
    // Language processing implementations
    KernelResult ExecuteTextProcessing(const std::vector<uint8_t>& text_data);
    KernelResult ExecuteTranslation(const std::vector<uint8_t>& translation_data);
    KernelResult ExecuteSentimentAnalysis(const std::vector<uint8_t>& sentiment_data);
    KernelResult ExecuteTextGeneration(const std::vector<uint8_t>& generation_data);
    KernelResult ExecuteGrammarChecking(const std::vector<uint8_t>& grammar_data);
    
    // Language utility functions
    std::string DetectLanguage(const std::string& text);
    void NormalizeText(const std::string& input, std::string& normalized);
    void TokenizeText(const std::string& text, std::vector<std::string>& tokens);
    void LemmatizeText(const std::vector<std::string>& tokens, std::vector<std::string>& lemmas);
    void TagPartsOfSpeech(const std::vector<std::string>& tokens, std::vector<std::string>& pos_tags);
    
    // Utility functions
    LanguageContext SelectBestContext(const std::string& task_description);
    void LogLanguageOperation(const std::string& operation, const std::string& details);
};

// Forward declarations for language engine components
class NLPParser;
class TranslationEngine;
class SentimentAnalyzer;
class TextGenerator;
class LanguageModel;
class GrammarChecker;

} // namespace AI
} // namespace AgenticOS