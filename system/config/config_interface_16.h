#pragma once
#include <string>
#include <vector>

namespace AgenticOS {

struct config_interface_16 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class config_interface_manager_16 {
public:
    void RegisterInterface(const config_interface_16& interface);
    void UnregisterInterface(const std::string& id);
    config_interface_16 GetInterface(const std::string& id);
};

} // namespace AgenticOS
