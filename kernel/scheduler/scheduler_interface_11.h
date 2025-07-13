#pragma once
#include <string>
#include <vector>

namespace AgenticOS {

struct scheduler_interface_11 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class scheduler_interface_manager_11 {
public:
    void RegisterInterface(const scheduler_interface_11& interface);
    void UnregisterInterface(const std::string& id);
    scheduler_interface_11 GetInterface(const std::string& id);
};

} // namespace AgenticOS
