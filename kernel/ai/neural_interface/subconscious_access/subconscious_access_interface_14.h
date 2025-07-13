#pragma once
#include <string>
#include <vector>

namespace AgenticOS {
namespace AI {

struct subconscious_access_interface_14 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class subconscious_access_interface_manager_14 {
public:
    void RegisterInterface(const subconscious_access_interface_14& interface);
    void UnregisterInterface(const std::string& id);
    subconscious_access_interface_14 GetInterface(const std::string& id);
};

} // namespace AI
} // namespace AgenticOS
