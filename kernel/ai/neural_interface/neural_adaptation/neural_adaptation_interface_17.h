#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct neural_adaptation_interface_17 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class neural_adaptation_interface_manager_17 {
public:
    void RegisterInterface(const neural_adaptation_interface_17& interface);
    void UnregisterInterface(const std::string& id);
    neural_adaptation_interface_17 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
