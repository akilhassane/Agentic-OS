#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct inference_interface_7 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class inference_interface_manager_7 {
public:
    void RegisterInterface(const inference_interface_7& interface);
    void UnregisterInterface(const std::string& id);
    inference_interface_7 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
