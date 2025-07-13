#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct integration_interface_7 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class integration_interface_manager_7 {
public:
    void RegisterInterface(const integration_interface_7& interface);
    void UnregisterInterface(const std::string& id);
    integration_interface_7 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
