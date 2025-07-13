#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct dream_interface_interface_1 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class dream_interface_interface_manager_1 {
public:
    void RegisterInterface(const dream_interface_interface_1& interface);
    void UnregisterInterface(const std::string& id);
    dream_interface_interface_1 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
