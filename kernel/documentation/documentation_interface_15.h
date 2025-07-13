#pragma once
#include <string>
#include <vector>

namespace AgenticOS {

struct documentation_interface_15 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class documentation_interface_manager_15 {
public:
    void RegisterInterface(const documentation_interface_15& interface);
    void UnregisterInterface(const std::string& id);
    documentation_interface_15 GetInterface(const std::string& id);
};

} // namespace AgenticOS
