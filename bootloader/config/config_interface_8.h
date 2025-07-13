#pragma once
#include <string>
#include <vector>

namespace AgenticOS {

struct config_interface_8 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class config_interface_manager_8 {
public:
    void RegisterInterface(const config_interface_8& interface);
    void UnregisterInterface(const std::string& id);
    config_interface_8 GetInterface(const std::string& id);
};

} // namespace AgenticOS
