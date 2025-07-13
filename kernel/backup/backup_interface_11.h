#pragma once
#include <string>
#include <vector>

namespace AgenticOS {

struct backup_interface_11 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class backup_interface_manager_11 {
public:
    void RegisterInterface(const backup_interface_11& interface);
    void UnregisterInterface(const std::string& id);
    backup_interface_11 GetInterface(const std::string& id);
};

} // namespace AgenticOS
