#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct adaptation_interface_11 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class adaptation_interface_manager_11 {
public:
    void RegisterInterface(const adaptation_interface_11& interface);
    void UnregisterInterface(const std::string& id);
    adaptation_interface_11 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
