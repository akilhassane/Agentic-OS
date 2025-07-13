#pragma once
#include <string>
#include <vector>

namespace AgenticOS {

struct tools_interface_8 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class tools_interface_manager_8 {
public:
    void RegisterInterface(const tools_interface_8& interface);
    void UnregisterInterface(const std::string& id);
    tools_interface_8 GetInterface(const std::string& id);
};

} // namespace AgenticOS
