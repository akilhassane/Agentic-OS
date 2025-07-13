#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct optimization_interface_8 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class optimization_interface_manager_8 {
public:
    void RegisterInterface(const optimization_interface_8& interface);
    void UnregisterInterface(const std::string& id);
    optimization_interface_8 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
