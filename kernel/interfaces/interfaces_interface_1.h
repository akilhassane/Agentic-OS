#pragma once
#include <string>
#include <vector>

namespace AgenticOS {

struct interfaces_interface_1 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class interfaces_interface_manager_1 {
public:
    void RegisterInterface(const interfaces_interface_1& interface);
    void UnregisterInterface(const std::string& id);
    interfaces_interface_1 GetInterface(const std::string& id);
};

} // namespace AgenticOS
