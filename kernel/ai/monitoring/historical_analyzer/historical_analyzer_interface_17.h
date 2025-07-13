#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct historical_analyzer_interface_17 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class historical_analyzer_interface_manager_17 {
public:
    void RegisterInterface(const historical_analyzer_interface_17& interface);
    void UnregisterInterface(const std::string& id);
    historical_analyzer_interface_17 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
