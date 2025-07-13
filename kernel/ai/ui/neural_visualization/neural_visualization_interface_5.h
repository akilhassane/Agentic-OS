#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct neural_visualization_interface_5 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class neural_visualization_interface_manager_5 {
public:
    void RegisterInterface(const neural_visualization_interface_5& interface);
    void UnregisterInterface(const std::string& id);
    neural_visualization_interface_5 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
