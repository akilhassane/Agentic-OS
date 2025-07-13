#pragma once
#include <string>
#include <vector>

namespace AgenticOS {

struct drivers_interface_7 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class drivers_interface_manager_7 {
public:
    void RegisterInterface(const drivers_interface_7& interface);
    void UnregisterInterface(const std::string& id);
    drivers_interface_7 GetInterface(const std::string& id);
};

} // namespace AgenticOS
