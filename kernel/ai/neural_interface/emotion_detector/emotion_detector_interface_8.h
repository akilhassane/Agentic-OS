#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct emotion_detector_interface_8 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class emotion_detector_interface_manager_8 {
public:
    void RegisterInterface(const emotion_detector_interface_8& interface);
    void UnregisterInterface(const std::string& id);
    emotion_detector_interface_8 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
