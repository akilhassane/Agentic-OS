#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct device_maintenance_interface_11 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class device_maintenance_interface_manager_11 {
public:
    void RegisterInterface(const device_maintenance_interface_11& interface);
    void UnregisterInterface(const std::string& id);
    device_maintenance_interface_11 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
