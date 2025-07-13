#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct device_monitor_interface_13 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class device_monitor_interface_manager_13 {
public:
    void RegisterInterface(const device_monitor_interface_13& interface);
    void UnregisterInterface(const std::string& id);
    device_monitor_interface_13 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
