#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct network_interface_6 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class network_interface_manager_6 {
public:
    void RegisterInterface(const network_interface_6& interface);
    void UnregisterInterface(const std::string& id);
    network_interface_6 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
