#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct memory_interface_3 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class memory_interface_manager_3 {
public:
    void RegisterInterface(const memory_interface_3& interface);
    void UnregisterInterface(const std::string& id);
    memory_interface_3 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
