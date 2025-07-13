#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct subconscious_access_interface_17 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class subconscious_access_interface_manager_17 {
public:
    void RegisterInterface(const subconscious_access_interface_17& interface);
    void UnregisterInterface(const std::string& id);
    subconscious_access_interface_17 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
