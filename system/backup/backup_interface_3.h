#pragma once
#include <string>
#include <vector>

namespace AgenticOS {

struct backup_interface_3 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class backup_interface_manager_3 {
public:
    void RegisterInterface(const backup_interface_3& interface);
    void UnregisterInterface(const std::string& id);
    backup_interface_3 GetInterface(const std::string& id);
};

} // namespace AgenticOS
