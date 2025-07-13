#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct device_security_interface_15 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class device_security_interface_manager_15 {
public:
    void RegisterInterface(const device_security_interface_15& interface);
    void UnregisterInterface(const std::string& id);
    device_security_interface_15 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
