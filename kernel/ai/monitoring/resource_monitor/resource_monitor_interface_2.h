#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct resource_monitor_interface_2 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class resource_monitor_interface_manager_2 {
public:
    void RegisterInterface(const resource_monitor_interface_2& interface);
    void UnregisterInterface(const std::string& id);
    resource_monitor_interface_2 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
