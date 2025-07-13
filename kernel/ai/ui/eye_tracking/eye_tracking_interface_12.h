#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct eye_tracking_interface_12 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class eye_tracking_interface_manager_12 {
public:
    void RegisterInterface(const eye_tracking_interface_12& interface);
    void UnregisterInterface(const std::string& id);
    eye_tracking_interface_12 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
