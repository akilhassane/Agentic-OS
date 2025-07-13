#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct intelligent_alerter_interface_13 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class intelligent_alerter_interface_manager_13 {
public:
    void RegisterInterface(const intelligent_alerter_interface_13& interface);
    void UnregisterInterface(const std::string& id);
    intelligent_alerter_interface_13 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
