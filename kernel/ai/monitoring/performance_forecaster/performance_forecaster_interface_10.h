#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct performance_forecaster_interface_10 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class performance_forecaster_interface_manager_10 {
public:
    void RegisterInterface(const performance_forecaster_interface_10& interface);
    void UnregisterInterface(const std::string& id);
    performance_forecaster_interface_10 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
