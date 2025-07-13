#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct real_time_monitor_interface_6 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class real_time_monitor_interface_manager_6 {
public:
    void RegisterInterface(const real_time_monitor_interface_6& interface);
    void UnregisterInterface(const std::string& id);
    real_time_monitor_interface_6 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
