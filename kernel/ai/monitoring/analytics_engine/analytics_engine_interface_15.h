#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct analytics_engine_interface_15 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class analytics_engine_interface_manager_15 {
public:
    void RegisterInterface(const analytics_engine_interface_15& interface);
    void UnregisterInterface(const std::string& id);
    analytics_engine_interface_15 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
