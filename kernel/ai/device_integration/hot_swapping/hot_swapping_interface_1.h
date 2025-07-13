#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct hot_swapping_interface_1 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class hot_swapping_interface_manager_1 {
public:
    void RegisterInterface(const hot_swapping_interface_1& interface);
    void UnregisterInterface(const std::string& id);
    hot_swapping_interface_1 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
