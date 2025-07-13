#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct device_optimizer_interface_10 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class device_optimizer_interface_manager_10 {
public:
    void RegisterInterface(const device_optimizer_interface_10& interface);
    void UnregisterInterface(const std::string& id);
    device_optimizer_interface_10 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
