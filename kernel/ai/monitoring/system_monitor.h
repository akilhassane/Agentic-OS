#pragma once

#include "../multi_agent_system.h"
#include "../agent_wire_protocol.h"
#include <memory>
#include <vector>
#include <map>

namespace AgenticOS {
namespace AI {

// System Monitor - Handles comprehensive system monitoring, analytics, and performance tracking
class SystemMonitor {
private:
    // Monitoring components
    struct MonitoringEngine {
        std::unique_ptr<PerformanceMonitor> performance_monitor;
        std::unique_ptr<ResourceMonitor> resource_monitor;
        std::unique_ptr<HealthMonitor> health_monitor;
        std::unique_ptr<AnalyticsEngine> analytics_engine;
        std::unique_ptr<AlertManager> alert_manager;
        std::unique_ptr<PredictiveAnalyzer> predictive_analyzer;
    };
    
    // Monitoring capabilities
    enum class MonitoringCapability {
        PERFORMANCE_MONITORING,
        RESOURCE_MONITORING,
        HEALTH_MONITORING,
        ANALYTICS,
        ALERT_MANAGEMENT,
        PREDICTIVE_ANALYSIS,
        REAL_TIME_MONITORING,
        HISTORICAL_ANALYSIS,
        TREND_ANALYSIS,
        ANOMALY_DETECTION,
        CAPACITY_PLANNING,
        PERFORMANCE_OPTIMIZATION,
        SYSTEM_DIAGNOSTICS,
        ROOT_CAUSE_ANALYSIS,
        PERFORMANCE_FORECASTING,
        INTELLIGENT_ALERTING
    };
    
    // Monitoring context
    struct MonitoringContext {
        std::string monitoring_domain;
        std::string monitoring_strategy;
        std::vector<std::string> monitored_components;
        std::vector<MonitoringCapability> required_capabilities;
        float alert_threshold;
        uint64_t monitoring_interval;
        bool enable_real_time;
        bool enable_predictive_analysis;
    };
    
    // Core components
    std::unique_ptr<MonitoringEngine> monitoring_engine;
    std::map<MonitoringCapability, bool> capability_status;
    std::map<std::string, MonitoringContext> context_cache;
    
    // Performance tracking
    struct MonitoringMetrics {
        uint64_t metrics_collected;
        uint64_t alerts_generated;
        uint64_t anomalies_detected;
        uint64_t predictions_made;
        float average_response_time;
        float system_health_score;
        std::map<MonitoringCapability, uint64_t> capability_usage;
        std::vector<std::string> recent_monitoring_events;
    };
    
    MonitoringMetrics metrics;
    
public:
    SystemMonitor() {
        monitoring_engine = std::make_unique<MonitoringEngine>();
    }
    
    // Core monitoring functions
    KernelResult Initialize();
    KernelResult MonitorPerformance(const PerformanceRequest& request, PerformanceData& data);
    KernelResult MonitorResources(const ResourceRequest& request, ResourceData& data);
    KernelResult MonitorHealth(const HealthRequest& request, HealthData& data);
    KernelResult AnalyzeSystem(const AnalyticsRequest& request, AnalyticsResult& result);
    KernelResult GenerateAlert(const AlertRequest& request, AlertData& alert);
    KernelResult PredictSystem(const PredictionRequest& request, PredictionResult& result);
    
    // Monitoring management
    KernelResult EnableCapability(MonitoringCapability capability);
    KernelResult DisableCapability(MonitoringCapability capability);
    bool IsCapabilityEnabled(MonitoringCapability capability);
    std::vector<MonitoringCapability> GetEnabledCapabilities();
    
    // Context management
    KernelResult SetMonitoringContext(const std::string& context_id, const MonitoringContext& context);
    KernelResult GetMonitoringContext(const std::string& context_id, MonitoringContext& context);
    KernelResult UpdateMonitoringContext(const std::string& context_id, const std::map<std::string, std::string>& updates);
    
    // Performance monitoring
    MonitoringMetrics GetMetrics() const;
    void ResetMetrics();
    void GenerateMonitoringReport();
    
private:
    // Monitoring implementations
    KernelResult ExecutePerformanceMonitoring(const std::vector<uint8_t>& performance_data);
    KernelResult ExecuteResourceMonitoring(const std::vector<uint8_t>& resource_data);
    KernelResult ExecuteHealthMonitoring(const std::vector<uint8_t>& health_data);
    KernelResult ExecuteAnalytics(const std::vector<uint8_t>& analytics_data);
    KernelResult ExecuteAlertGeneration(const std::vector<uint8_t>& alert_data);
    
    // Monitoring utility functions
    float CalculateSystemHealth(const std::vector<uint8_t>& health_data);
    void AnalyzeSystemPatterns(const std::vector<uint8_t>& pattern_data);
    void UpdateMonitoringModel(const std::string& model_id, const std::vector<uint8_t>& model_data);
    void OptimizeMonitoringStrategy(const std::vector<uint8_t>& strategy_data);
    
    // Utility functions
    MonitoringContext SelectBestContext(const std::string& task_description);
    void LogMonitoringOperation(const std::string& operation, const std::string& details);
};

// Forward declarations for monitoring engine components
class PerformanceMonitor;
class ResourceMonitor;
class HealthMonitor;
class AnalyticsEngine;
class AlertManager;
class PredictiveAnalyzer;

// Monitoring data structures
struct PerformanceRequest {
    std::string request_id;
    std::string component_id;
    std::vector<std::string> performance_metrics;
    std::map<std::string, float> request_parameters;
    uint64_t monitoring_duration;
    float sampling_rate;
};

struct PerformanceData {
    std::string data_id;
    std::string component_id;
    std::map<std::string, float> performance_metrics;
    std::vector<float> time_series_data;
    uint64_t timestamp;
    float performance_score;
    std::string performance_status;
};

struct ResourceRequest {
    std::string request_id;
    std::string resource_type;
    std::vector<std::string> resource_metrics;
    std::map<std::string, float> request_parameters;
    uint64_t monitoring_duration;
    float utilization_threshold;
};

struct ResourceData {
    std::string data_id;
    std::string resource_type;
    std::map<std::string, float> resource_metrics;
    float utilization_percentage;
    uint64_t timestamp;
    std::string resource_status;
    std::vector<std::string> bottlenecks;
};

struct HealthRequest {
    std::string request_id;
    std::string system_component;
    std::vector<std::string> health_indicators;
    std::map<std::string, float> request_parameters;
    uint64_t monitoring_duration;
    float health_threshold;
};

struct HealthData {
    std::string data_id;
    std::string component_id;
    std::map<std::string, float> health_indicators;
    float overall_health_score;
    uint64_t timestamp;
    std::string health_status;
    std::vector<std::string> health_issues;
};

struct AnalyticsRequest {
    std::string request_id;
    std::string analysis_type;
    std::vector<std::string> data_sources;
    std::map<std::string, float> analysis_parameters;
    uint64_t analysis_timeout;
    float confidence_threshold;
};

struct AnalyticsResult {
    std::string result_id;
    std::string request_id;
    std::map<std::string, float> analysis_metrics;
    std::vector<std::string> insights;
    float confidence_score;
    uint64_t analysis_time;
    std::string analysis_method;
};

struct AlertRequest {
    std::string request_id;
    std::string alert_type;
    std::string alert_message;
    std::map<std::string, float> alert_parameters;
    float severity_level;
    uint64_t timestamp;
};

struct AlertData {
    std::string alert_id;
    std::string request_id;
    std::string alert_type;
    std::string alert_message;
    float severity_level;
    uint64_t timestamp;
    std::vector<std::string> affected_components;
    std::vector<std::string> recommended_actions;
};

struct PredictionRequest {
    std::string request_id;
    std::string prediction_type;
    std::vector<std::string> prediction_targets;
    std::map<std::string, float> prediction_parameters;
    uint64_t prediction_horizon;
    float confidence_threshold;
};

struct PredictionResult {
    std::string result_id;
    std::string request_id;
    std::map<std::string, float> predictions;
    std::vector<float> confidence_intervals;
    float overall_confidence;
    uint64_t prediction_time;
    std::string prediction_method;
};

struct SystemMetric {
    std::string metric_id;
    std::string metric_name;
    std::string metric_type;
    float metric_value;
    std::map<std::string, float> metric_metadata;
    uint64_t timestamp;
    std::string unit;
};

struct SystemTrend {
    std::string trend_id;
    std::string trend_type;
    std::vector<float> trend_data;
    std::map<std::string, float> trend_parameters;
    float trend_direction;
    uint64_t analysis_period;
};

} // namespace AI
} // namespace AgenticOS