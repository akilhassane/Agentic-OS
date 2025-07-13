#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct brain_interface_interface_10 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class brain_interface_interface_manager_10 {
public:
    void RegisterInterface(const brain_interface_interface_10& interface);
    void UnregisterInterface(const std::string& id);
    brain_interface_interface_10 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
