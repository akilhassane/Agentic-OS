#pragma once

#include <cstdint>
#include <vector>
#include <string>
#include <map>
#include <memory>
#include <functional>
#include "../common/kernel_types.h"

namespace AgenticOS {
namespace AI {

// Wire Protocol Version
constexpr uint32_t WIRE_PROTOCOL_VERSION = 0x0100;

// Message Types for Agent Communication
enum class WireMessageType : uint16_t {
    // System Messages
    HEARTBEAT = 0x0001,
    REGISTER = 0x0002,
    UNREGISTER = 0x0003,
    STATUS_UPDATE = 0x0004,
    ERROR_REPORT = 0x0005,
    SHUTDOWN = 0x0006,
    
    // Task Management
    TASK_REQUEST = 0x0100,
    TASK_ASSIGNMENT = 0x0101,
    TASK_PROGRESS = 0x0102,
    TASK_COMPLETE = 0x0103,
    TASK_FAILED = 0x0104,
    TASK_CANCEL = 0x0105,
    
    // Data Exchange
    DATA_REQUEST = 0x0200,
    DATA_RESPONSE = 0x0201,
    DATA_STREAM = 0x0202,
    DATA_COMPLETE = 0x0203,
    
    // Capability Management
    CAPABILITY_QUERY = 0x0300,
    CAPABILITY_RESPONSE = 0x0301,
    CAPABILITY_UPDATE = 0x0302,
    CAPABILITY_REQUEST = 0x0303,
    
    // Learning and Adaptation
    LEARNING_REQUEST = 0x0400,
    LEARNING_DATA = 0x0401,
    LEARNING_COMPLETE = 0x0402,
    ADAPTATION_REQUEST = 0x0403,
    ADAPTATION_RESPONSE = 0x0404,
    
    // Resource Management
    RESOURCE_REQUEST = 0x0500,
    RESOURCE_ALLOCATION = 0x0501,
    RESOURCE_RELEASE = 0x0502,
    RESOURCE_STATUS = 0x0503,
    
    // Coordination
    COORDINATION_REQUEST = 0x0600,
    COORDINATION_RESPONSE = 0x0601,
    SYNCHRONIZATION = 0x0602,
    CONFLICT_RESOLUTION = 0x0603,
    
    // Security and Validation
    AUTHENTICATION = 0x0700,
    AUTHORIZATION = 0x0701,
    VALIDATION_REQUEST = 0x0702,
    VALIDATION_RESPONSE = 0x0703,
    SECURITY_ALERT = 0x0704,
    
    // Monitoring and Debugging
    METRICS_REQUEST = 0x0800,
    METRICS_RESPONSE = 0x0801,
    DEBUG_REQUEST = 0x0802,
    DEBUG_RESPONSE = 0x0803,
    LOG_REQUEST = 0x0804,
    LOG_RESPONSE = 0x0805,
    
    // Custom/Application Specific
    CUSTOM_MESSAGE = 0xFFFF
};

// Wire Protocol Header Structure
struct WireHeader {
    uint32_t magic_number;        // 0x41474E54 (AGNT)
    uint32_t protocol_version;    // WIRE_PROTOCOL_VERSION
    uint16_t message_type;        // WireMessageType
    uint16_t flags;               // Message flags
    uint32_t sender_id;           // Sender agent ID
    uint32_t receiver_id;         // Receiver agent ID (0 for broadcast)
    uint64_t message_id;          // Unique message identifier
    uint64_t timestamp;           // Message timestamp
    uint32_t payload_size;        // Size of payload in bytes
    uint32_t checksum;            // CRC32 checksum of payload
    uint32_t sequence_number;     // For ordered message delivery
    uint32_t priority;            // Message priority
    uint32_t timeout_ms;          // Response timeout in milliseconds
    uint32_t reserved[4];         // Reserved for future use
} __attribute__((packed));

// Wire Protocol Flags
enum class WireFlags : uint16_t {
    NONE = 0x0000,
    ENCRYPTED = 0x0001,
    COMPRESSED = 0x0002,
    FRAGMENTED = 0x0004,
    URGENT = 0x0008,
    RELIABLE = 0x0010,
    ORDERED = 0x0020,
    BROADCAST = 0x0040,
    MULTICAST = 0x0080,
    RESPONSE_REQUIRED = 0x0100,
    ACK_REQUIRED = 0x0200,
    RETRY_ON_FAILURE = 0x0400,
    HIGH_PRIORITY = 0x0800,
    LOW_PRIORITY = 0x1000,
    DEBUG_MODE = 0x2000,
    TRACE_ENABLED = 0x4000,
    RESERVED = 0x8000
};

// Wire Protocol Message Structure
struct WireMessage {
    WireHeader header;
    std::vector<uint8_t> payload;
    
    // Constructor
    WireMessage() {
        header.magic_number = 0x41474E54; // AGNT
        header.protocol_version = WIRE_PROTOCOL_VERSION;
        header.timestamp = GetCurrentTimeUS();
        header.message_id = GenerateMessageID();
        header.sequence_number = 0;
        header.priority = 0;
        header.timeout_ms = 5000; // 5 second default
        memset(header.reserved, 0, sizeof(header.reserved));
    }
    
    // Utility functions
    void SetMessageType(WireMessageType type) { header.message_type = static_cast<uint16_t>(type); }
    void SetSender(uint32_t sender_id) { header.sender_id = sender_id; }
    void SetReceiver(uint32_t receiver_id) { header.receiver_id = receiver_id; }
    void SetPriority(uint32_t priority) { header.priority = priority; }
    void SetTimeout(uint32_t timeout_ms) { header.timeout_ms = timeout_ms; }
    void SetFlag(WireFlags flag) { header.flags |= static_cast<uint16_t>(flag); }
    void ClearFlag(WireFlags flag) { header.flags &= ~static_cast<uint16_t>(flag); }
    bool HasFlag(WireFlags flag) const { return (header.flags & static_cast<uint16_t>(flag)) != 0; }
    
    // Payload management
    void SetPayload(const std::vector<uint8_t>& data);
    std::vector<uint8_t> GetPayload() const;
    void UpdateChecksum();
    bool ValidateChecksum() const;
    
    // Serialization
    std::vector<uint8_t> Serialize() const;
    KernelResult Deserialize(const std::vector<uint8_t>& data);
    
private:
    uint64_t GetCurrentTimeUS();
    uint64_t GenerateMessageID();
    uint32_t CalculateCRC32(const std::vector<uint8_t>& data) const;
};

// Wire Protocol Payload Structures

// Task Management Payloads
struct TaskRequestPayload {
    uint64_t task_id;
    std::string task_description;
    std::vector<uint8_t> task_data;
    std::vector<uint32_t> required_capabilities;
    uint64_t deadline;
    uint32_t priority;
    std::map<std::string, std::string> parameters;
    
    std::vector<uint8_t> Serialize() const;
    KernelResult Deserialize(const std::vector<uint8_t>& data);
};

struct TaskAssignmentPayload {
    uint64_t task_id;
    uint32_t assigned_agent_id;
    std::vector<uint8_t> task_data;
    uint64_t deadline;
    std::map<std::string, std::string> instructions;
    
    std::vector<uint8_t> Serialize() const;
    KernelResult Deserialize(const std::vector<uint8_t>& data);
};

struct TaskProgressPayload {
    uint64_t task_id;
    float progress_percentage;
    std::string status_message;
    std::vector<uint8_t> intermediate_data;
    uint64_t estimated_completion;
    
    std::vector<uint8_t> Serialize() const;
    KernelResult Deserialize(const std::vector<uint8_t>& data);
};

struct TaskCompletePayload {
    uint64_t task_id;
    bool success;
    std::vector<uint8_t> result_data;
    std::string result_message;
    uint64_t execution_time;
    std::map<std::string, std::string> metadata;
    
    std::vector<uint8_t> Serialize() const;
    KernelResult Deserialize(const std::vector<uint8_t>& data);
};

// Capability Management Payloads
struct CapabilityQueryPayload {
    uint32_t query_id;
    std::vector<std::string> requested_capabilities;
    std::vector<AgentSpecialization> required_specializations;
    bool include_metrics;
    bool include_availability;
    
    std::vector<uint8_t> Serialize() const;
    KernelResult Deserialize(const std::vector<uint8_t>& data);
};

struct CapabilityResponsePayload {
    uint32_t query_id;
    std::vector<AgentCapability> capabilities;
    std::vector<AgentMetrics> metrics;
    bool available;
    uint64_t response_time;
    
    std::vector<uint8_t> Serialize() const;
    KernelResult Deserialize(const std::vector<uint8_t>& data);
};

// Learning and Adaptation Payloads
struct LearningRequestPayload {
    uint64_t learning_id;
    std::string learning_type;
    std::vector<uint8_t> training_data;
    std::map<std::string, std::string> parameters;
    uint64_t timeout;
    
    std::vector<uint8_t> Serialize() const;
    KernelResult Deserialize(const std::vector<uint8_t>& data);
};

struct LearningDataPayload {
    uint64_t learning_id;
    std::vector<uint8_t> data_chunk;
    uint32_t chunk_index;
    uint32_t total_chunks;
    bool is_final_chunk;
    
    std::vector<uint8_t> Serialize() const;
    KernelResult Deserialize(const std::vector<uint8_t>& data);
};

// Resource Management Payloads
struct ResourceRequestPayload {
    uint64_t request_id;
    uint64_t memory_requested;
    uint32_t cpu_cores_requested;
    uint64_t storage_requested;
    std::vector<std::string> special_resources;
    uint64_t duration;
    
    std::vector<uint8_t> Serialize() const;
    KernelResult Deserialize(const std::vector<uint8_t>& data);
};

struct ResourceAllocationPayload {
    uint64_t request_id;
    bool allocated;
    uint64_t memory_allocated;
    uint32_t cpu_cores_allocated;
    uint64_t storage_allocated;
    std::vector<std::string> special_resources_allocated;
    std::string allocation_reason;
    
    std::vector<uint8_t> Serialize() const;
    KernelResult Deserialize(const std::vector<uint8_t>& data);
};

// Metrics and Monitoring Payloads
struct MetricsRequestPayload {
    uint64_t request_id;
    std::vector<std::string> requested_metrics;
    bool include_history;
    uint32_t history_length;
    
    std::vector<uint8_t> Serialize() const;
    KernelResult Deserialize(const std::vector<uint8_t>& data);
};

struct MetricsResponsePayload {
    uint64_t request_id;
    AgentMetrics metrics;
    std::vector<std::string> available_metrics;
    uint64_t collection_time;
    
    std::vector<uint8_t> Serialize() const;
    KernelResult Deserialize(const std::vector<uint8_t>& data);
};

// Wire Protocol Handler Interface
class WireProtocolHandler {
protected:
    uint32_t agent_id;
    std::map<WireMessageType, std::function<KernelResult(const WireMessage&)>> message_handlers;
    
public:
    WireProtocolHandler(uint32_t id) : agent_id(id) {}
    virtual ~WireProtocolHandler() = default;
    
    // Core protocol functions
    virtual KernelResult Initialize() = 0;
    virtual KernelResult SendMessage(const WireMessage& message) = 0;
    virtual KernelResult ReceiveMessage(WireMessage& message) = 0;
    virtual KernelResult ProcessMessage(const WireMessage& message) = 0;
    
    // Message creation helpers
    WireMessage CreateMessage(WireMessageType type, uint32_t receiver_id = 0);
    WireMessage CreateTaskRequest(uint64_t task_id, const std::string& description, const std::vector<uint8_t>& data);
    WireMessage CreateCapabilityQuery(const std::vector<std::string>& capabilities);
    WireMessage CreateResourceRequest(uint64_t memory, uint32_t cpu_cores);
    WireMessage CreateMetricsRequest(const std::vector<std::string>& metrics);
    
    // Message processing
    void RegisterMessageHandler(WireMessageType type, std::function<KernelResult(const WireMessage&)> handler);
    KernelResult HandleTaskRequest(const WireMessage& message);
    KernelResult HandleCapabilityQuery(const WireMessage& message);
    KernelResult HandleResourceRequest(const WireMessage& message);
    KernelResult HandleMetricsRequest(const WireMessage& message);
    
    // Utility functions
    bool ValidateMessage(const WireMessage& message) const;
    void LogMessage(const WireMessage& message, const std::string& direction);
    uint64_t GetCurrentTimeUS();
    uint64_t GenerateMessageID();
};

// Wire Protocol Serializer/Deserializer
class WireSerializer {
public:
    // Generic serialization
    template<typename T>
    static std::vector<uint8_t> Serialize(const T& obj) {
        return obj.Serialize();
    }
    
    template<typename T>
    static KernelResult Deserialize(const std::vector<uint8_t>& data, T& obj) {
        return obj.Deserialize(data);
    }
    
    // Primitive type serialization
    static std::vector<uint8_t> SerializeString(const std::string& str);
    static std::vector<uint8_t> SerializeVector(const std::vector<uint8_t>& vec);
    static std::vector<uint8_t> SerializeMap(const std::map<std::string, std::string>& map);
    
    // Primitive type deserialization
    static KernelResult DeserializeString(const std::vector<uint8_t>& data, std::string& str);
    static KernelResult DeserializeVector(const std::vector<uint8_t>& data, std::vector<uint8_t>& vec);
    static KernelResult DeserializeMap(const std::vector<uint8_t>& data, std::map<std::string, std::string>& map);
    
    // Wire message specific
    static std::vector<uint8_t> SerializeWireMessage(const WireMessage& message);
    static KernelResult DeserializeWireMessage(const std::vector<uint8_t>& data, WireMessage& message);
};

// Wire Protocol Network Interface
class WireNetworkInterface {
private:
    int socket_fd;
    std::string bind_address;
    uint16_t bind_port;
    std::atomic<bool> running;
    std::thread receive_thread;
    
public:
    WireNetworkInterface() : socket_fd(-1), bind_port(0), running(false) {}
    ~WireNetworkInterface() { Stop(); }
    
    // Network management
    KernelResult Initialize(const std::string& address, uint16_t port);
    KernelResult Start();
    void Stop();
    
    // Message transmission
    KernelResult SendMessage(const WireMessage& message, const std::string& target_address, uint16_t target_port);
    KernelResult BroadcastMessage(const WireMessage& message);
    
    // Message reception
    void SetMessageHandler(std::function<void(const WireMessage&)> handler);
    
private:
    void ReceiveLoop();
    KernelResult CreateSocket();
    KernelResult BindSocket();
    KernelResult SetSocketOptions();
};

// Wire Protocol Security
class WireSecurity {
private:
    std::vector<uint8_t> encryption_key;
    std::vector<uint8_t> authentication_key;
    bool encryption_enabled;
    bool authentication_enabled;
    
public:
    WireSecurity() : encryption_enabled(false), authentication_enabled(false) {}
    
    // Security configuration
    void EnableEncryption(const std::vector<uint8_t>& key);
    void EnableAuthentication(const std::vector<uint8_t>& key);
    void DisableEncryption();
    void DisableAuthentication();
    
    // Security operations
    std::vector<uint8_t> EncryptPayload(const std::vector<uint8_t>& payload);
    std::vector<uint8_t> DecryptPayload(const std::vector<uint8_t>& encrypted_payload);
    std::vector<uint8_t> SignMessage(const WireMessage& message);
    bool VerifyMessage(const WireMessage& message, const std::vector<uint8_t>& signature);
    
    // Utility functions
    bool IsEncryptionEnabled() const { return encryption_enabled; }
    bool IsAuthenticationEnabled() const { return authentication_enabled; }
};

// Wire Protocol Statistics
struct WireProtocolStats {
    uint64_t messages_sent;
    uint64_t messages_received;
    uint64_t messages_processed;
    uint64_t messages_failed;
    uint64_t bytes_sent;
    uint64_t bytes_received;
    uint64_t average_latency_ms;
    uint64_t max_latency_ms;
    uint64_t min_latency_ms;
    std::map<WireMessageType, uint64_t> message_type_counts;
    std::map<uint32_t, uint64_t> agent_message_counts;
    
    void Reset();
    void UpdateLatency(uint64_t latency_ms);
    void IncrementMessageType(WireMessageType type);
    void IncrementAgentMessages(uint32_t agent_id);
};

// Global wire protocol instances
extern WireProtocolHandler* g_wire_protocol_handler;
extern WireNetworkInterface* g_wire_network_interface;
extern WireSecurity* g_wire_security;
extern WireProtocolStats g_wire_stats;

} // namespace AI
} // namespace AgenticOS