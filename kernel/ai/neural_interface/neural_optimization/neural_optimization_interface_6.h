#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct neural_optimization_interface_6 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class neural_optimization_interface_manager_6 {
public:
    void RegisterInterface(const neural_optimization_interface_6& interface);
    void UnregisterInterface(const std::string& id);
    neural_optimization_interface_6 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
