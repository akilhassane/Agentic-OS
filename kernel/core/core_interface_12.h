#pragma once
#include <string>
#include <vector>

namespace AgenticOS {

struct core_interface_12 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class core_interface_manager_12 {
public:
    void RegisterInterface(const core_interface_12& interface);
    void UnregisterInterface(const std::string& id);
    core_interface_12 GetInterface(const std::string& id);
};

} // namespace AgenticOS
