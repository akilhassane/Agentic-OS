#include "kernel.h"
#include "memory/ai_memory_manager.h"
#include "scheduler/ai_scheduler.h"
#include "drivers/driver_manager.h"
#include "ai/ai_kernel_interface.h"
#include "ai/model_runtime.h"
#include "ai/agent_manager.h"
#include "filesystem/agenticfs.h"
#include "network/ai_network_stack.h"
#include "security/ai_security.h"

// AgenticOS Kernel - AI-First Operating System Kernel
// Copyright (c) 2024 AgenticOS Project

namespace AgenticOS {
namespace Kernel {

struct KernelBootInfo {
    struct AIHardwareInfo {
        bool gpu_detected;
        bool npu_detected; 
        bool tpu_detected;
        uint32_t gpu_memory_mb;
        uint32_t compute_units;
        char gpu_name[64];
        char ai_chip_name[64];
    } ai_hardware;
    
    struct BootConfig {
        uint64_t memory_for_ai_mb;
        bool enable_ai_acceleration;
        bool secure_boot_ai_models;
        char default_ai_runtime[32];
    } boot_config;
    
    void* graphics_protocol;
    void* runtime_services;
    uint64_t ai_memory_base;
    uint64_t ai_memory_size;
};

class AgenticKernel {
private:
    KernelBootInfo* boot_info;
    Memory::AIMemoryManager* memory_manager;
    Scheduler::AIScheduler* scheduler;
    Drivers::DriverManager* driver_manager;
    AI::AIKernelInterface* ai_interface;
    AI::ModelRuntime* model_runtime;
    AI::AgentManager* agent_manager;
    FileSystem::AgenticFS* filesystem;
    Network::AINetworkStack* network_stack;
    Security::AISecurity* security_manager;
    
    bool initialized;
    uint64_t boot_time;
    
public:
    AgenticKernel() : initialized(false), boot_time(0) {
        boot_info = nullptr;
        memory_manager = nullptr;
        scheduler = nullptr;
        driver_manager = nullptr;
        ai_interface = nullptr;
        model_runtime = nullptr;
        agent_manager = nullptr;
        filesystem = nullptr;
        network_stack = nullptr;
        security_manager = nullptr;
    }
    
    KernelResult Initialize(KernelBootInfo* info);
    KernelResult StartAIServices();
    KernelResult InitializeUserspace();
    void MainLoop();
    void Shutdown();
};

// Global kernel instance
AgenticKernel* g_kernel = nullptr;

KernelResult AgenticKernel::Initialize(KernelBootInfo* info) {
    boot_info = info;
    boot_time = GetSystemTime();
    
    PrintKernel("[AgenticOS] Kernel initialization starting...\n");
    PrintKernel("[INFO] AI Memory: %lu MB at 0x%lx\n", 
                info->ai_memory_base, info->ai_memory_size);
    
    // 1. Initialize AI-aware memory management
    PrintKernel("[KERNEL] Initializing AI Memory Manager...\n");
    memory_manager = new Memory::AIMemoryManager();
    KernelResult result = memory_manager->Initialize(
        info->ai_memory_base, 
        info->ai_memory_size,
        info->boot_config.enable_ai_acceleration
    );
    if (result != KERNEL_SUCCESS) {
        PrintKernel("[ERROR] Failed to initialize AI memory manager\n");
        return result;
    }
    
    // 2. Initialize AI-optimized scheduler
    PrintKernel("[KERNEL] Initializing AI Scheduler...\n");
    scheduler = new Scheduler::AIScheduler();
    result = scheduler->Initialize(
        info->ai_hardware.compute_units,
        info->ai_hardware.gpu_detected
    );
    if (result != KERNEL_SUCCESS) {
        PrintKernel("[ERROR] Failed to initialize AI scheduler\n");
        return result;
    }
    
    // 3. Initialize driver manager with AI drivers
    PrintKernel("[KERNEL] Initializing Driver Manager...\n");
    driver_manager = new Drivers::DriverManager();
    result = driver_manager->Initialize(&info->ai_hardware);
    if (result != KERNEL_SUCCESS) {
        PrintKernel("[ERROR] Failed to initialize driver manager\n");
        return result;
    }
    
    // 4. Initialize AI kernel interface
    PrintKernel("[KERNEL] Initializing AI Kernel Interface...\n");
    ai_interface = new AI::AIKernelInterface();
    result = ai_interface->Initialize(memory_manager, scheduler);
    if (result != KERNEL_SUCCESS) {
        PrintKernel("[ERROR] Failed to initialize AI kernel interface\n");
        return result;
    }
    
    // 5. Initialize model runtime
    PrintKernel("[KERNEL] Initializing Model Runtime...\n");
    model_runtime = new AI::ModelRuntime();
    result = model_runtime->Initialize(
        ai_interface,
        info->boot_config.default_ai_runtime
    );
    if (result != KERNEL_SUCCESS) {
        PrintKernel("[ERROR] Failed to initialize model runtime\n");
        return result;
    }
    
    // 6. Initialize agent manager
    PrintKernel("[KERNEL] Initializing Agent Manager...\n");
    agent_manager = new AI::AgentManager();
    result = agent_manager->Initialize(model_runtime, scheduler);
    if (result != KERNEL_SUCCESS) {
        PrintKernel("[ERROR] Failed to initialize agent manager\n");
        return result;
    }
    
    // 7. Initialize AgenticFS
    PrintKernel("[KERNEL] Initializing AgenticFS...\n");
    filesystem = new FileSystem::AgenticFS();
    result = filesystem->Initialize(memory_manager);
    if (result != KERNEL_SUCCESS) {
        PrintKernel("[ERROR] Failed to initialize AgenticFS\n");
        return result;
    }
    
    // 8. Initialize AI network stack
    PrintKernel("[KERNEL] Initializing AI Network Stack...\n");
    network_stack = new Network::AINetworkStack();
    result = network_stack->Initialize(driver_manager);
    if (result != KERNEL_SUCCESS) {
        PrintKernel("[ERROR] Failed to initialize AI network stack\n");
        return result;
    }
    
    // 9. Initialize AI security manager
    PrintKernel("[KERNEL] Initializing AI Security Manager...\n");
    security_manager = new Security::AISecurity();
    result = security_manager->Initialize(
        info->boot_config.secure_boot_ai_models,
        filesystem
    );
    if (result != KERNEL_SUCCESS) {
        PrintKernel("[ERROR] Failed to initialize AI security manager\n");
        return result;
    }
    
    initialized = true;
    PrintKernel("[AgenticOS] Kernel initialization completed successfully\n");
    return KERNEL_SUCCESS;
}

KernelResult AgenticKernel::StartAIServices() {
    if (!initialized) {
        return KERNEL_ERROR_NOT_INITIALIZED;
    }
    
    PrintKernel("[AgenticOS] Starting AI system services...\n");
    
    // Start core AI services
    struct AIService {
        const char* name;
        const char* binary_path;
        uint32_t priority;
        bool critical;
    };
    
    AIService services[] = {
        {"ModelD", "/system/services/modeld", 100, true},
        {"AgentD", "/system/services/agentd", 95, true},
        {"ToolD", "/system/services/toold", 90, false},
        {"KnowledgeD", "/system/services/knowledged", 85, false},
        {"ContextD", "/system/services/contextd", 80, false},
        {"SecurityD", "/system/services/securityd", 99, true}
    };
    
    for (const auto& service : services) {
        PrintKernel("[SERVICE] Starting %s...\n", service.name);
        
        KernelResult result = scheduler->CreateSystemProcess(
            service.binary_path,
            service.priority,
            service.critical
        );
        
        if (result != KERNEL_SUCCESS) {
            if (service.critical) {
                PrintKernel("[ERROR] Critical service %s failed to start\n", service.name);
                return result;
            } else {
                PrintKernel("[WARNING] Non-critical service %s failed to start\n", service.name);
            }
        } else {
            PrintKernel("[INFO] Service %s started successfully\n", service.name);
        }
    }
    
    PrintKernel("[AgenticOS] AI services started\n");
    return KERNEL_SUCCESS;
}

KernelResult AgenticKernel::InitializeUserspace() {
    PrintKernel("[AgenticOS] Initializing userspace...\n");
    
    // Mount root filesystem
    KernelResult result = filesystem->MountRoot("/");
    if (result != KERNEL_SUCCESS) {
        PrintKernel("[ERROR] Failed to mount root filesystem\n");
        return result;
    }
    
    // Create standard directories
    const char* standard_dirs[] = {
        "/bin", "/sbin", "/usr", "/var", "/tmp", "/home",
        "/system", "/system/services", "/system/drivers",
        "/ai", "/ai/models", "/ai/agents", "/ai/tools",
        "/ai/datasets", "/ai/cache", "/ai/logs"
    };
    
    for (const auto& dir : standard_dirs) {
        filesystem->CreateDirectory(dir);
    }
    
    // Start init process
    PrintKernel("[KERNEL] Starting init process...\n");
    result = scheduler->CreateUserProcess(
        "/sbin/init",
        0,  // root user
        true // system process
    );
    
    if (result != KERNEL_SUCCESS) {
        PrintKernel("[ERROR] Failed to start init process\n");
        return result;
    }
    
    PrintKernel("[AgenticOS] Userspace initialized\n");
    return KERNEL_SUCCESS;
}

void AgenticKernel::MainLoop() {
    PrintKernel("[AgenticOS] Entering kernel main loop\n");
    
    uint64_t last_stats_time = GetSystemTime();
    
    while (true) {
        // Process scheduler
        scheduler->Schedule();
        
        // Handle AI workload balancing
        ai_interface->BalanceWorkloads();
        
        // Process agent tasks
        agent_manager->ProcessAgentTasks();
        
        // Handle model inference requests
        model_runtime->ProcessInferenceQueue();
        
        // Network processing
        network_stack->ProcessPackets();
        
        // Security monitoring
        security_manager->MonitorThreats();
        
        // Periodic statistics (every 30 seconds)
        uint64_t current_time = GetSystemTime();
        if (current_time - last_stats_time > 30000) {
            PrintSystemStats();
            last_stats_time = current_time;
        }
        
        // Small sleep to prevent 100% CPU usage
        scheduler->Sleep(1); // 1ms
    }
}

void AgenticKernel::Shutdown() {
    PrintKernel("[AgenticOS] Kernel shutdown initiated\n");
    
    // Stop AI services gracefully
    if (agent_manager) {
        agent_manager->StopAllAgents();
    }
    
    if (model_runtime) {
        model_runtime->UnloadAllModels();
    }
    
    // Shutdown components in reverse order
    delete security_manager;
    delete network_stack;
    delete filesystem;
    delete agent_manager;
    delete model_runtime;
    delete ai_interface;
    delete driver_manager;
    delete scheduler;
    delete memory_manager;
    
    PrintKernel("[AgenticOS] Kernel shutdown completed\n");
}

void PrintSystemStats() {
    auto memory_stats = g_kernel->memory_manager->GetStats();
    auto scheduler_stats = g_kernel->scheduler->GetStats();
    auto ai_stats = g_kernel->ai_interface->GetStats();
    
    PrintKernel("\n=== AgenticOS System Statistics ===\n");
    PrintKernel("Uptime: %lu seconds\n", (GetSystemTime() - g_kernel->boot_time) / 1000);
    PrintKernel("Memory: %lu MB used, %lu MB AI reserved\n", 
                memory_stats.total_used_mb, memory_stats.ai_reserved_mb);
    PrintKernel("Processes: %u total, %u AI agents\n", 
                scheduler_stats.total_processes, scheduler_stats.ai_agents);
    PrintKernel("AI Models: %u loaded, %lu inferences/sec\n", 
                ai_stats.loaded_models, ai_stats.inferences_per_second);
    PrintKernel("=====================================\n\n");
}

} // namespace Kernel
} // namespace AgenticOS

// Kernel entry point called by bootloader
extern "C" void kernel_main(AgenticOS::Kernel::KernelBootInfo* boot_info) {
    using namespace AgenticOS::Kernel;
    
    // Create global kernel instance
    g_kernel = new AgenticKernel();
    
    // Initialize kernel
    KernelResult result = g_kernel->Initialize(boot_info);
    if (result != KERNEL_SUCCESS) {
        PrintKernel("[FATAL] Kernel initialization failed: %d\n", result);
        return;
    }
    
    // Start AI services
    result = g_kernel->StartAIServices();
    if (result != KERNEL_SUCCESS) {
        PrintKernel("[FATAL] Failed to start AI services: %d\n", result);
        return;
    }
    
    // Initialize userspace
    result = g_kernel->InitializeUserspace();
    if (result != KERNEL_SUCCESS) {
        PrintKernel("[FATAL] Failed to initialize userspace: %d\n", result);
        return;
    }
    
    PrintKernel("[AgenticOS] System ready - AI agents and models active\n");
    
    // Enter main kernel loop
    g_kernel->MainLoop();
    
    // Should never reach here unless shutdown
    g_kernel->Shutdown();
}