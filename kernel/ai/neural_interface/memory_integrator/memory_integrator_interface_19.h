#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct memory_integrator_interface_19 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class memory_integrator_interface_manager_19 {
public:
    void RegisterInterface(const memory_integrator_interface_19& interface);
    void UnregisterInterface(const std::string& id);
    memory_integrator_interface_19 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
