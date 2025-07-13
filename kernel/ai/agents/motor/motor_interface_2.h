#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct motor_interface_2 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class motor_interface_manager_2 {
public:
    void RegisterInterface(const motor_interface_2& interface);
    void UnregisterInterface(const std::string& id);
    motor_interface_2 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
