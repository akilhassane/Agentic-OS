#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct dream_interface_interface_15 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class dream_interface_interface_manager_15 {
public:
    void RegisterInterface(const dream_interface_interface_15& interface);
    void UnregisterInterface(const std::string& id);
    dream_interface_interface_15 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
