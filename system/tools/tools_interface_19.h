#pragma once
#include <string>
#include <vector>

namespace AgenticOS {

struct tools_interface_19 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class tools_interface_manager_19 {
public:
    void RegisterInterface(const tools_interface_19& interface);
    void UnregisterInterface(const std::string& id);
    tools_interface_19 GetInterface(const std::string& id);
};

} // namespace AgenticOS
