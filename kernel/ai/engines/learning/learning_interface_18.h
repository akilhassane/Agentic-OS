#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct learning_interface_18 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class learning_interface_manager_18 {
public:
    void RegisterInterface(const learning_interface_18& interface);
    void UnregisterInterface(const std::string& id);
    learning_interface_18 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
