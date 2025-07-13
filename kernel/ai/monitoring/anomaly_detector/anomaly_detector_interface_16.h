#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct anomaly_detector_interface_16 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class anomaly_detector_interface_manager_16 {
public:
    void RegisterInterface(const anomaly_detector_interface_16& interface);
    void UnregisterInterface(const std::string& id);
    anomaly_detector_interface_16 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
