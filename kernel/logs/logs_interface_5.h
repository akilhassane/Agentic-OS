#pragma once
#include <string>
#include <vector>

namespace AgenticOS {

struct logs_interface_5 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class logs_interface_manager_5 {
public:
    void RegisterInterface(const logs_interface_5& interface);
    void UnregisterInterface(const std::string& id);
    logs_interface_5 GetInterface(const std::string& id);
};

} // namespace AgenticOS
