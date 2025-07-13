#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct dream_interface_interface_19 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class dream_interface_interface_manager_19 {
public:
    void RegisterInterface(const dream_interface_interface_19& interface);
    void UnregisterInterface(const std::string& id);
    dream_interface_interface_19 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
