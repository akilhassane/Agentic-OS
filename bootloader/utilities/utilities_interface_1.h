#pragma once
#include <string>
#include <vector>

namespace AgenticOS {

struct utilities_interface_1 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class utilities_interface_manager_1 {
public:
    void RegisterInterface(const utilities_interface_1& interface);
    void UnregisterInterface(const std::string& id);
    utilities_interface_1 GetInterface(const std::string& id);
};

} // namespace AgenticOS
