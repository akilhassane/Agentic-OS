#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct trend_analyzer_interface_8 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class trend_analyzer_interface_manager_8 {
public:
    void RegisterInterface(const trend_analyzer_interface_8& interface);
    void UnregisterInterface(const std::string& id);
    trend_analyzer_interface_8 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
