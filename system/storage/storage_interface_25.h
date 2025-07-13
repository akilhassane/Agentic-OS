#pragma once
#include <string>
#include <vector>

namespace AgenticOS {

struct storage_interface_25 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class storage_interface_manager_25 {
public:
    void RegisterInterface(const storage_interface_25& interface);
    void UnregisterInterface(const std::string& id);
    storage_interface_25 GetInterface(const std::string& id);
};

} // namespace AgenticOS
