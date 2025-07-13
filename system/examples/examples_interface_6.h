#pragma once
#include <string>
#include <vector>

namespace AgenticOS {

struct examples_interface_6 {
    std::string id;
    std::string type;
    std::vector<std::string> capabilities;
    std::map<std::string, float> parameters;
};

class examples_interface_manager_6 {
public:
    void RegisterInterface(const examples_interface_6& interface);
    void UnregisterInterface(const std::string& id);
    examples_interface_6 GetInterface(const std::string& id);
};

} // namespace AgenticOS
