#pragma once

#include "../multi_agent_system.h"
#include "../agent_wire_protocol.h"
#include <memory>
#include <vector>
#include <map>

namespace AgenticOS {
namespace AI {

// Motor Agent - Handles physical motor control, movement, and manipulation
class MotorAgent : public BaseAgent {
private:
    // Motor control components
    struct MotorEngine {
        std::unique_ptr<MotorController> motor_controller;
        std::unique_ptr<KinematicsSolver> kinematics_solver;
        std::unique_ptr<DynamicsSolver> dynamics_solver;
        std::unique_ptr<TrajectoryPlanner> trajectory_planner;
        std::unique_ptr<ForceController> force_controller;
        std::unique_ptr<ImpedanceController> impedance_controller;
    };
    
    // Motor capabilities
    enum class MotorCapability {
        POSITION_CONTROL,
        VELOCITY_CONTROL,
        FORCE_CONTROL,
        IMPEDANCE_CONTROL,
        TRAJECTORY_TRACKING,
        OBSTACLE_AVOIDANCE,
        GRASP_PLANNING,
        MANIPULATION,
        LOCOMOTION,
        BALANCE_CONTROL,
        COORDINATION,
        FINE_MOTOR,
        GROSS_MOTOR,
        REFLEX_RESPONSE,
        ADAPTIVE_CONTROL,
        LEARNING_CONTROL
    };
    
    // Motor control context
    struct MotorContext {
        std::string control_mode;
        uint32_t degrees_of_freedom;
        std::vector<float> joint_limits;
        std::vector<MotorCapability> required_capabilities;
        float safety_threshold;
        uint64_t control_frequency;
        bool enable_adaptive_control;
        bool enable_learning;
    };
    
    // Core components
    std::unique_ptr<MotorEngine> motor_engine;
    std::map<MotorCapability, bool> capability_status;
    std::map<std::string, MotorContext> context_cache;
    
    // Performance tracking
    struct MotorMetrics {
        uint64_t movements_executed;
        uint64_t trajectories_completed;
        uint64_t grasps_performed;
        uint64_t manipulations_completed;
        float average_accuracy;
        uint64_t average_execution_time;
        std::map<MotorCapability, uint64_t> capability_usage;
        std::vector<std::string> recent_operations;
    };
    
    MotorMetrics metrics;
    
public:
    MotorAgent(uint32_t id) : BaseAgent(id, "MotorAgent", AgentSpecialization::MOTOR_CONTROL_AGENT) {
        motor_engine = std::make_unique<MotorEngine>();
    }
    
    // Core agent functions
    KernelResult Initialize() override;
    KernelResult ExecuteTask(const std::vector<uint8_t>& task_data) override;
    void ProcessMessage(const AgentMessage& message) override;
    void LearnFromExperience(const std::vector<uint8_t>& experience_data) override;
    void AdaptToEnvironment(const std::vector<uint8_t>& environment_data) override;
    
    // Motor control capabilities
    KernelResult ControlPosition(const std::vector<float>& target_position, const MotorContext& context);
    KernelResult ControlVelocity(const std::vector<float>& target_velocity, const MotorContext& context);
    KernelResult ControlForce(const std::vector<float>& target_force, const MotorContext& context);
    KernelResult ExecuteTrajectory(const std::vector<TrajectoryPoint>& trajectory, const MotorContext& context);
    KernelResult PerformGrasp(const GraspTarget& target, const MotorContext& context);
    KernelResult PerformManipulation(const ManipulationTask& task, const MotorContext& context);
    
    // Motor management
    KernelResult EnableCapability(MotorCapability capability);
    KernelResult DisableCapability(MotorCapability capability);
    bool IsCapabilityEnabled(MotorCapability capability);
    std::vector<MotorCapability> GetEnabledCapabilities();
    
    // Context management
    KernelResult SetMotorContext(const std::string& context_id, const MotorContext& context);
    KernelResult GetMotorContext(const std::string& context_id, MotorContext& context);
    KernelResult UpdateMotorContext(const std::string& context_id, const std::map<std::string, std::string>& updates);
    
    // Performance monitoring
    MotorMetrics GetMetrics() const;
    void ResetMetrics();
    void GenerateMotorReport();
    
protected:
    // Internal motor functions
    virtual void MainLoop() override;
    virtual void ProcessTask(const std::vector<uint8_t>& task_data) override;
    virtual void HandleMessage(const AgentMessage& message) override;
    virtual void PerformLearning() override;
    virtual void UpdateState() override;
    
private:
    // Motor control implementations
    KernelResult ExecutePositionControl(const std::vector<uint8_t>& control_data);
    KernelResult ExecuteVelocityControl(const std::vector<uint8_t>& control_data);
    KernelResult ExecuteForceControl(const std::vector<uint8_t>& control_data);
    KernelResult ExecuteTrajectoryControl(const std::vector<uint8_t>& trajectory_data);
    KernelResult ExecuteGraspControl(const std::vector<uint8_t>& grasp_data);
    
    // Motor utility functions
    void CalculateInverseKinematics(const std::vector<float>& target_pose, std::vector<float>& joint_angles);
    void CalculateForwardKinematics(const std::vector<float>& joint_angles, std::vector<float>& end_effector_pose);
    float CalculateTrajectoryError(const std::vector<float>& actual, const std::vector<float>& desired);
    void OptimizeTrajectory(const std::vector<TrajectoryPoint>& input, std::vector<TrajectoryPoint>& optimized);
    
    // Utility functions
    MotorContext SelectBestContext(const std::string& task_description);
    void LogMotorOperation(const std::string& operation, const std::string& details);
};

// Forward declarations for motor engine components
class MotorController;
class KinematicsSolver;
class DynamicsSolver;
class TrajectoryPlanner;
class ForceController;
class ImpedanceController;

// Motor data structures
struct TrajectoryPoint {
    uint64_t timestamp;
    std::vector<float> position;
    std::vector<float> velocity;
    std::vector<float> acceleration;
    std::vector<float> force;
};

struct GraspTarget {
    std::string object_id;
    std::vector<float> object_pose;
    std::vector<float> grasp_pose;
    float grasp_quality;
    std::map<std::string, float> grasp_parameters;
};

struct ManipulationTask {
    std::string task_id;
    std::string task_type;
    std::vector<TrajectoryPoint> trajectory;
    std::map<std::string, float> task_parameters;
    float priority;
    uint64_t deadline;
};

struct MotorState {
    std::vector<float> joint_positions;
    std::vector<float> joint_velocities;
    std::vector<float> joint_forces;
    std::vector<float> end_effector_pose;
    std::map<std::string, float> sensor_readings;
    uint64_t timestamp;
};

struct SafetyConstraints {
    std::vector<float> position_limits;
    std::vector<float> velocity_limits;
    std::vector<float> force_limits;
    std::vector<float> acceleration_limits;
    float collision_threshold;
    float emergency_stop_threshold;
};

} // namespace AI
} // namespace AgenticOS