#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct alert_manager_interface_6 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class alert_manager_interface_manager_6 {
public:
    void RegisterInterface(const alert_manager_interface_6& interface);
    void UnregisterInterface(const std::string& id);
    alert_manager_interface_6 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
