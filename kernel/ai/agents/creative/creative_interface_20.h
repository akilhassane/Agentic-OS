#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct creative_interface_20 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class creative_interface_manager_20 {
public:
    void RegisterInterface(const creative_interface_20& interface);
    void UnregisterInterface(const std::string& id);
    creative_interface_20 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
