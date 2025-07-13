#pragma once

#include <cstdint>
#include <atomic>
#include "../common/kernel_types.h"

namespace AgenticOS {
namespace Memory {

// Lightweight, lock-free memory pool for AI workloads
class AIMemoryPool {
private:
    struct Block {
        std::atomic<Block*> next;
        uint32_t size;
        bool in_use;
        uint8_t alignment_padding[3];
    } __attribute__((packed));

    std::atomic<Block*> free_head;
    uint8_t* pool_start;
    uint8_t* pool_end;
    uint32_t total_size;
    std::atomic<uint32_t> allocated_bytes;

public:
    KernelResult Initialize(void* base, uint32_t size);
    void* Allocate(uint32_t size, uint32_t alignment = 64);
    void Deallocate(void* ptr);
    uint32_t GetAllocatedBytes() const { return allocated_bytes.load(); }
    uint32_t GetTotalSize() const { return total_size; }
};

// High-performance tensor memory allocator
class TensorAllocator {
private:
    static constexpr uint32_t MAX_TENSOR_POOLS = 8;
    static constexpr uint32_t TENSOR_ALIGNMENT = 256; // For SIMD/GPU alignment
    
    struct TensorPool {
        AIMemoryPool pool;
        uint32_t tensor_size;
        std::atomic<uint32_t> active_tensors;
    };
    
    TensorPool pools[MAX_TENSOR_POOLS];
    uint8_t pool_count;
    std::atomic<uint32_t> total_tensor_memory;

public:
    KernelResult Initialize(void* base, uint32_t size);
    void* AllocateTensor(uint32_t elements, uint32_t element_size);
    void DeallocateTensor(void* tensor_ptr);
    uint32_t GetTensorMemoryUsage() const { return total_tensor_memory.load(); }
};

// Main AI memory manager - lightweight and robust
class AIMemoryManager {
private:
    // Memory regions
    void* ai_memory_base;
    uint64_t ai_memory_size;
    
    // Allocators (minimal overhead)
    TensorAllocator tensor_allocator;
    AIMemoryPool model_pool;
    AIMemoryPool agent_pool;
    AIMemoryPool general_pool;
    
    // Statistics (atomic for thread safety)
    std::atomic<uint64_t> total_allocated;
    std::atomic<uint32_t> allocation_count;
    std::atomic<uint32_t> deallocation_count;
    
    // Configuration
    bool gpu_memory_enabled;
    void* gpu_memory_base;
    uint32_t gpu_memory_size;
    
    // Error recovery
    uint32_t corruption_count;
    bool recovery_mode;

public:
    struct MemoryStats {
        uint64_t total_used_mb;
        uint64_t ai_reserved_mb;
        uint32_t tensor_allocations;
        uint32_t model_allocations;
        uint32_t agent_allocations;
        uint32_t fragmentation_percent;
    };

    AIMemoryManager() : 
        ai_memory_base(nullptr),
        ai_memory_size(0),
        total_allocated(0),
        allocation_count(0),
        deallocation_count(0),
        gpu_memory_enabled(false),
        gpu_memory_base(nullptr),
        gpu_memory_size(0),
        corruption_count(0),
        recovery_mode(false) {}

    // Core functions - optimized for speed
    KernelResult Initialize(uint64_t base, uint64_t size, bool enable_gpu);
    
    // Fast allocation functions (lock-free when possible)
    void* AllocateModel(uint32_t size);
    void* AllocateTensor(uint32_t elements, uint32_t element_size);
    void* AllocateAgent(uint32_t size);
    void* AllocateGeneral(uint32_t size);
    
    void DeallocateModel(void* ptr);
    void DeallocateTensor(void* ptr);
    void DeallocateAgent(void* ptr);
    void DeallocateGeneral(void* ptr);
    
    // GPU memory management
    void* AllocateGPU(uint32_t size);
    void DeallocateGPU(void* ptr);
    KernelResult CopyToGPU(void* gpu_ptr, const void* cpu_ptr, uint32_t size);
    KernelResult CopyFromGPU(void* cpu_ptr, const void* gpu_ptr, uint32_t size);
    
    // Statistics and monitoring
    MemoryStats GetStats() const;
    bool CheckIntegrity();
    KernelResult DefragmentPools();
    
    // Error handling and recovery
    bool DetectCorruption();
    KernelResult RecoverFromCorruption();
    void EnableRecoveryMode() { recovery_mode = true; }
    void DisableRecoveryMode() { recovery_mode = false; }
};

// Inline fast path functions for performance
inline void* AIMemoryManager::AllocateGeneral(uint32_t size) {
    if (__builtin_expect(recovery_mode, 0)) {
        return nullptr; // Fail fast in recovery mode
    }
    
    void* ptr = general_pool.Allocate(size);
    if (__builtin_expect(ptr != nullptr, 1)) {
        total_allocated.fetch_add(size, std::memory_order_relaxed);
        allocation_count.fetch_add(1, std::memory_order_relaxed);
    }
    return ptr;
}

inline void AIMemoryManager::DeallocateGeneral(void* ptr) {
    if (__builtin_expect(ptr == nullptr || recovery_mode, 0)) {
        return;
    }
    
    general_pool.Deallocate(ptr);
    deallocation_count.fetch_add(1, std::memory_order_relaxed);
}

} // namespace Memory
} // namespace AgenticOS