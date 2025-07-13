#pragma once
#include <string>
#include <vector>

namespace AgenticOS {

struct storage_interface_18 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class storage_interface_manager_18 {
public:
    void RegisterInterface(const storage_interface_18& interface);
    void UnregisterInterface(const std::string& id);
    storage_interface_18 GetInterface(const std::string& id);
};

} // namespace AgenticOS
