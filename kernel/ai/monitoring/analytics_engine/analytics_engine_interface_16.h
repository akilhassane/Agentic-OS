#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct analytics_engine_interface_16 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class analytics_engine_interface_manager_16 {
public:
    void RegisterInterface(const analytics_engine_interface_16& interface);
    void UnregisterInterface(const std::string& id);
    analytics_engine_interface_16 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
