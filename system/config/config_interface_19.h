#pragma once
#include <string>
#include <vector>

namespace AgenticOS {

struct config_interface_19 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class config_interface_manager_19 {
public:
    void RegisterInterface(const config_interface_19& interface);
    void UnregisterInterface(const std::string& id);
    config_interface_19 GetInterface(const std::string& id);
};

} // namespace AgenticOS
