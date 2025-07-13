#pragma once
#include <string>
#include <vector>

namespace AgenticOS {

struct interfaces_interface_20 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class interfaces_interface_manager_20 {
public:
    void RegisterInterface(const interfaces_interface_20& interface);
    void UnregisterInterface(const std::string& id);
    interfaces_interface_20 GetInterface(const std::string& id);
};

} // namespace AgenticOS
