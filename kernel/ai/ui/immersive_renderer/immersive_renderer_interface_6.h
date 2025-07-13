#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct immersive_renderer_interface_6 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class immersive_renderer_interface_manager_6 {
public:
    void RegisterInterface(const immersive_renderer_interface_6& interface);
    void UnregisterInterface(const std::string& id);
    immersive_renderer_interface_6 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
