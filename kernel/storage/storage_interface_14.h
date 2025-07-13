#pragma once
#include <string>
#include <vector>

namespace AgenticOS {

struct storage_interface_14 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class storage_interface_manager_14 {
public:
    void RegisterInterface(const storage_interface_14& interface);
    void UnregisterInterface(const std::string& id);
    storage_interface_14 GetInterface(const std::string& id);
};

} // namespace AgenticOS
