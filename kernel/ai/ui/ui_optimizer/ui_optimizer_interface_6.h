#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct ui_optimizer_interface_6 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class ui_optimizer_interface_manager_6 {
public:
    void RegisterInterface(const ui_optimizer_interface_6& interface);
    void UnregisterInterface(const std::string& id);
    ui_optimizer_interface_6 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
