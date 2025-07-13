#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct eye_tracking_interface_16 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class eye_tracking_interface_manager_16 {
public:
    void RegisterInterface(const eye_tracking_interface_16& interface);
    void UnregisterInterface(const std::string& id);
    eye_tracking_interface_16 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
