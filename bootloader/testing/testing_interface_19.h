#pragma once
#include <string>
#include <vector>

namespace AgenticOS {

struct testing_interface_19 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class testing_interface_manager_19 {
public:
    void RegisterInterface(const testing_interface_19& interface);
    void UnregisterInterface(const std::string& id);
    testing_interface_19 GetInterface(const std::string& id);
};

} // namespace AgenticOS
