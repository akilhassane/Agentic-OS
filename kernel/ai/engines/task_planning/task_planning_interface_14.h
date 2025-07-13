#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct task_planning_interface_14 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class task_planning_interface_manager_14 {
public:
    void RegisterInterface(const task_planning_interface_14& interface);
    void UnregisterInterface(const std::string& id);
    task_planning_interface_14 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
