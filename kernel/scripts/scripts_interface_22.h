#pragma once
#include <string>
#include <vector>

namespace AgenticOS {

struct scripts_interface_22 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class scripts_interface_manager_22 {
public:
    void RegisterInterface(const scripts_interface_22& interface);
    void UnregisterInterface(const std::string& id);
    scripts_interface_22 GetInterface(const std::string& id);
};

} // namespace AgenticOS
