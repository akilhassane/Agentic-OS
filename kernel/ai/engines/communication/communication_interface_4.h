#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct communication_interface_4 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class communication_interface_manager_4 {
public:
    void RegisterInterface(const communication_interface_4& interface);
    void UnregisterInterface(const std::string& id);
    communication_interface_4 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
