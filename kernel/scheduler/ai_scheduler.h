#pragma once

#include <cstdint>
#include <atomic>
#include "../common/kernel_types.h"

namespace AgenticOS {
namespace Scheduler {

// Lightweight process control block optimized for AI workloads
struct ProcessControlBlock {
    uint32_t pid;
    uint32_t parent_pid;
    ProcessState state;
    uint8_t priority;
    uint8_t ai_priority; // Special AI workload priority
    uint16_t flags;
    
    // CPU context (minimal for fast switching)
    uint64_t rsp, rbp, rip;
    uint64_t r12, r13, r14, r15;
    uint64_t rflags;
    
    // AI-specific context
    void* ai_context;     // Pointer to AI model/agent context
    uint32_t gpu_context_id; // GPU context identifier
    uint64_t ai_memory_usage;
    
    // Timing and statistics
    uint64_t cpu_time_us;
    uint64_t start_time;
    uint64_t last_scheduled;
    uint32_t schedule_count;
    
    // Fault tolerance
    uint8_t fault_count;
    uint8_t recovery_attempts;
    ProcessState last_good_state;
    
    // Lock-free linked list
    std::atomic<ProcessControlBlock*> next;
} __attribute__((packed));

// Lock-free run queue for high performance
class LockFreeRunQueue {
private:
    std::atomic<ProcessControlBlock*> head;
    std::atomic<ProcessControlBlock*> tail;
    std::atomic<uint32_t> size;

public:
    void Initialize();
    bool Enqueue(ProcessControlBlock* pcb);
    ProcessControlBlock* Dequeue();
    uint32_t GetSize() const { return size.load(std::memory_order_relaxed); }
    bool IsEmpty() const { return size.load(std::memory_order_relaxed) == 0; }
};

// GPU/AI accelerator scheduling context
struct AIAcceleratorContext {
    uint32_t device_id;
    ProcessControlBlock* current_process;
    std::atomic<bool> in_use;
    uint64_t context_switch_time_us;
    uint32_t queue_depth;
    LockFreeRunQueue ai_queue;
};

// Lightweight, robust AI scheduler
class AIScheduler {
private:
    // Process management
    static constexpr uint32_t MAX_PROCESSES = 4096;
    static constexpr uint32_t MAX_AI_ACCELERATORS = 16;
    
    ProcessControlBlock process_table[MAX_PROCESSES];
    std::atomic<uint32_t> next_pid;
    std::atomic<uint32_t> active_processes;
    
    // Scheduling queues (lock-free for performance)
    LockFreeRunQueue ready_queue;
    LockFreeRunQueue ai_high_priority;
    LockFreeRunQueue ai_normal_priority;
    LockFreeRunQueue system_queue;
    
    // AI accelerator management
    AIAcceleratorContext accelerators[MAX_AI_ACCELERATORS];
    uint8_t accelerator_count;
    
    // Current execution context
    ProcessControlBlock* current_process;
    uint64_t time_slice_us;
    std::atomic<uint64_t> total_context_switches;
    
    // Fault tolerance and recovery
    uint32_t scheduler_faults;
    bool degraded_mode;
    uint64_t last_health_check;
    
    // Performance optimization
    uint64_t last_schedule_time;
    uint32_t schedule_overhead_us;
    bool idle_state;

public:
    struct SchedulerStats {
        uint32_t total_processes;
        uint32_t ai_agents;
        uint32_t running_processes;
        uint64_t context_switches_per_sec;
        uint32_t average_latency_us;
        uint8_t cpu_utilization_percent;
        uint8_t ai_utilization_percent;
    };

    AIScheduler() :
        next_pid(1),
        active_processes(0),
        accelerator_count(0),
        current_process(nullptr),
        time_slice_us(10000), // 10ms default
        total_context_switches(0),
        scheduler_faults(0),
        degraded_mode(false),
        last_health_check(0),
        last_schedule_time(0),
        schedule_overhead_us(0),
        idle_state(true) {}

    // Core scheduling functions
    KernelResult Initialize(uint32_t compute_units, bool gpu_detected);
    void Schedule();
    void Yield();
    void Preempt();
    
    // Process management - optimized for speed
    KernelResult CreateSystemProcess(const char* path, uint32_t priority, bool critical);
    KernelResult CreateUserProcess(const char* path, uint32_t uid, bool system);
    KernelResult CreateAIAgent(void* ai_context, uint32_t priority);
    void TerminateProcess(uint32_t pid);
    void SuspendProcess(uint32_t pid);
    void ResumeProcess(uint32_t pid);
    
    // AI-specific scheduling
    KernelResult ScheduleOnGPU(uint32_t pid, uint32_t gpu_id);
    void ReturnFromGPU(uint32_t pid);
    void BalanceAIWorkloads();
    
    // Fast path operations (inline for performance)
    void Sleep(uint64_t microseconds);
    ProcessControlBlock* GetCurrentProcess() { return current_process; }
    uint32_t GetCurrentPID() { return current_process ? current_process->pid : 0; }
    
    // Statistics and monitoring
    SchedulerStats GetStats() const;
    bool HealthCheck();
    void EnterDegradedMode() { degraded_mode = true; }
    void ExitDegradedMode() { degraded_mode = false; }
    
    // Fault tolerance
    KernelResult RecoverProcess(uint32_t pid);
    void HandleSchedulerFault();
    bool ValidateProcessState(ProcessControlBlock* pcb);

private:
    // Internal scheduling functions
    ProcessControlBlock* SelectNextProcess();
    void ContextSwitch(ProcessControlBlock* next);
    void UpdateProcessStats(ProcessControlBlock* pcb);
    void CheckTimeSlice();
    
    // AI scheduling optimization
    void OptimizeAIScheduling();
    bool ShouldPreemptForAI(ProcessControlBlock* current, ProcessControlBlock* ai_process);
    void BalanceGPUQueues();
    
    // Fault handling
    void HandleProcessFault(ProcessControlBlock* pcb);
    bool AttemptProcessRecovery(ProcessControlBlock* pcb);
    void QuarantineProcess(ProcessControlBlock* pcb);
};

// Inline fast path functions for minimal overhead
inline void AIScheduler::Sleep(uint64_t microseconds) {
    if (__builtin_expect(current_process == nullptr, 0)) {
        return;
    }
    
    current_process->state = ProcessState::SLEEPING;
    current_process->last_scheduled = GetSystemTimeUS() + microseconds;
    Yield();
}

inline void AIScheduler::Yield() {
    if (__builtin_expect(degraded_mode, 0)) {
        return; // Skip yielding in degraded mode
    }
    
    if (current_process) {
        current_process->state = ProcessState::READY;
        ready_queue.Enqueue(current_process);
    }
    
    Schedule();
}

// Lock-free context switch for maximum performance
inline void AIScheduler::ContextSwitch(ProcessControlBlock* next) {
    if (__builtin_expect(next == current_process, 0)) {
        return; // No switch needed
    }
    
    uint64_t switch_start = GetSystemTimeUS();
    
    // Save current context (if any)
    if (current_process) {
        // Save minimal context for fast switching
        asm volatile(
            "movq %%rsp, %0\n"
            "movq %%rbp, %1\n"
            "movq %%r12, %2\n"
            "movq %%r13, %3\n"
            "movq %%r14, %4\n"
            "movq %%r15, %5\n"
            "pushfq\n"
            "popq %6\n"
            : "=m" (current_process->rsp),
              "=m" (current_process->rbp),
              "=m" (current_process->r12),
              "=m" (current_process->r13),
              "=m" (current_process->r14),
              "=m" (current_process->r15),
              "=m" (current_process->rflags)
            :
            : "memory"
        );
    }
    
    // Switch to next process
    current_process = next;
    next->state = ProcessState::RUNNING;
    next->last_scheduled = switch_start;
    next->schedule_count++;
    
    // Restore context
    asm volatile(
        "movq %0, %%rsp\n"
        "movq %1, %%rbp\n"
        "movq %2, %%r12\n"
        "movq %3, %%r13\n"
        "movq %4, %%r14\n"
        "movq %5, %%r15\n"
        "pushq %6\n"
        "popfq\n"
        :
        : "m" (next->rsp),
          "m" (next->rbp),
          "m" (next->r12),
          "m" (next->r13),
          "m" (next->r14),
          "m" (next->r15),
          "m" (next->rflags)
        : "memory"
    );
    
    uint64_t switch_end = GetSystemTimeUS();
    schedule_overhead_us = switch_end - switch_start;
    total_context_switches.fetch_add(1, std::memory_order_relaxed);
}

} // namespace Scheduler
} // namespace AgenticOS