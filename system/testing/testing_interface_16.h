#pragma once
#include <string>
#include <vector>

namespace AgenticOS {

struct testing_interface_16 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class testing_interface_manager_16 {
public:
    void RegisterInterface(const testing_interface_16& interface);
    void UnregisterInterface(const std::string& id);
    testing_interface_16 GetInterface(const std::string& id);
};

} // namespace AgenticOS
