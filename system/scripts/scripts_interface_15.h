#pragma once
#include <string>
#include <vector>

namespace AgenticOS {

struct scripts_interface_15 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class scripts_interface_manager_15 {
public:
    void RegisterInterface(const scripts_interface_15& interface);
    void UnregisterInterface(const std::string& id);
    scripts_interface_15 GetInterface(const std::string& id);
};

} // namespace AgenticOS
