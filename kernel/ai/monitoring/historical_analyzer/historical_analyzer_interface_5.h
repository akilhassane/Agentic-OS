#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct historical_analyzer_interface_5 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class historical_analyzer_interface_manager_5 {
public:
    void RegisterInterface(const historical_analyzer_interface_5& interface);
    void UnregisterInterface(const std::string& id);
    historical_analyzer_interface_5 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
