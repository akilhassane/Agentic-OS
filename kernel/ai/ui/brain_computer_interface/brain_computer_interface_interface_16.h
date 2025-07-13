#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct brain_computer_interface_interface_16 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class brain_computer_interface_interface_manager_16 {
public:
    void RegisterInterface(const brain_computer_interface_interface_16& interface);
    void UnregisterInterface(const std::string& id);
    brain_computer_interface_interface_16 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
