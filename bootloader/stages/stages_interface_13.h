#pragma once
#include <string>
#include <vector>

namespace AgenticOS {

struct stages_interface_13 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class stages_interface_manager_13 {
public:
    void RegisterInterface(const stages_interface_13& interface);
    void UnregisterInterface(const std::string& id);
    stages_interface_13 GetInterface(const std::string& id);
};

} // namespace AgenticOS
