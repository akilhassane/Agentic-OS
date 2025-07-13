#pragma once
#include <string>
#include <vector>

namespace AgenticOS {

struct drivers_interface_11 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class drivers_interface_manager_11 {
public:
    void RegisterInterface(const drivers_interface_11& interface);
    void UnregisterInterface(const std::string& id);
    drivers_interface_11 GetInterface(const std::string& id);
};

} // namespace AgenticOS
