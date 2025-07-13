#pragma once
#include <string>
#include <vector>

namespace AgenticOS {

struct documentation_interface_7 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class documentation_interface_manager_7 {
public:
    void RegisterInterface(const documentation_interface_7& interface);
    void UnregisterInterface(const std::string& id);
    documentation_interface_7 GetInterface(const std::string& id);
};

} // namespace AgenticOS
