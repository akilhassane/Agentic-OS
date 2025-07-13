#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct neural_learning_interface_11 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class neural_learning_interface_manager_11 {
public:
    void RegisterInterface(const neural_learning_interface_11& interface);
    void UnregisterInterface(const std::string& id);
    neural_learning_interface_11 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
