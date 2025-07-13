#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct neural_safety_interface_15 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class neural_safety_interface_manager_15 {
public:
    void RegisterInterface(const neural_safety_interface_15& interface);
    void UnregisterInterface(const std::string& id);
    neural_safety_interface_15 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
