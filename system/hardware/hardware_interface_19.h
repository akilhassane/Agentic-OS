#pragma once
#include <string>
#include <vector>

namespace AgenticOS {

struct hardware_interface_19 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class hardware_interface_manager_19 {
public:
    void RegisterInterface(const hardware_interface_19& interface);
    void UnregisterInterface(const std::string& id);
    hardware_interface_19 GetInterface(const std::string& id);
};

} // namespace AgenticOS
