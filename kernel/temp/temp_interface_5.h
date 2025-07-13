#pragma once
#include <string>
#include <vector>

namespace AgenticOS {

struct temp_interface_5 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class temp_interface_manager_5 {
public:
    void RegisterInterface(const temp_interface_5& interface);
    void UnregisterInterface(const std::string& id);
    temp_interface_5 GetInterface(const std::string& id);
};

} // namespace AgenticOS
