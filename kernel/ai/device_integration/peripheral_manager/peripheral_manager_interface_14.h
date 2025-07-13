#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct peripheral_manager_interface_14 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class peripheral_manager_interface_manager_14 {
public:
    void RegisterInterface(const peripheral_manager_interface_14& interface);
    void UnregisterInterface(const std::string& id);
    peripheral_manager_interface_14 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
