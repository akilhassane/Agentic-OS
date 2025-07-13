cmake_minimum_required(VERSION 3.16)
project(AgenticOS VERSION 1.0.0 LANGUAGES C CXX ASM)

# Set C++ standard
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Build configuration
set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type")
set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")

# Options
option(ENABLE_AI_OPTIMIZATIONS "Enable AI-specific optimizations" ON)
option(ENABLE_GPU_ACCELERATION "Enable GPU acceleration for AI" ON)
option(ENABLE_NEURAL_NETWORKS "Enable neural network support" ON)
option(ENABLE_VOICE_INTERFACE "Enable voice interface support" ON)
option(ENABLE_GESTURE_INTERFACE "Enable gesture interface support" ON)
option(ENABLE_MULTIMODAL_INPUT "Enable multimodal input support" ON)
option(ENABLE_CONTINUOUS_LEARNING "Enable continuous learning capabilities" ON)
option(ENABLE_SYSTEM_EVOLUTION "Enable system self-evolution" ON)
option(ENABLE_UNIVERSAL_INTERFACES "Enable universal interface engine" ON)
option(BUILD_TESTS "Build tests" OFF)
option(BUILD_EXAMPLES "Build examples" OFF)
option(BUILD_DOCUMENTATION "Build documentation" OFF)

# Compiler flags
if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU" OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    set(CMAKE_CXX_FLAGS_DEBUG "-g -O0 -Wall -Wextra -Wpedantic")
    set(CMAKE_CXX_FLAGS_RELEASE "-O3 -DNDEBUG -march=native")
    
    if(ENABLE_AI_OPTIMIZATIONS)
        set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -ffast-math -funroll-loops")
    endif()
endif()

# Include directories
include_directories(
    ${CMAKE_SOURCE_DIR}
    ${CMAKE_SOURCE_DIR}/kernel
    ${CMAKE_SOURCE_DIR}/system
    ${CMAKE_SOURCE_DIR}/userspace
    ${CMAKE_SOURCE_DIR}/external/include
)

# Find required packages
find_package(Threads REQUIRED)
find_package(PkgConfig REQUIRED)

# GPU/AI acceleration libraries
if(ENABLE_GPU_ACCELERATION)
    find_package(CUDA QUIET)
    if(CUDA_FOUND)
        enable_language(CUDA)
        add_definitions(-DWITH_CUDA)
        message(STATUS "CUDA support enabled")
    endif()
    
    # Try to find ROCm for AMD GPUs
    find_path(ROCM_INCLUDE_DIR hip/hip_runtime.h PATHS /opt/rocm/include)
    if(ROCM_INCLUDE_DIR)
        add_definitions(-DWITH_ROCM)
        message(STATUS "ROCm support enabled")
    endif()
endif()

# Neural network libraries
if(ENABLE_NEURAL_NETWORKS)
    # Try to find common ML libraries
    find_path(TORCH_INCLUDE_DIR torch/torch.h PATHS /usr/local/include /usr/include)
    if(TORCH_INCLUDE_DIR)
        add_definitions(-DWITH_TORCH)
        message(STATUS "PyTorch C++ support enabled")
    endif()
    
    find_path(TENSORFLOW_INCLUDE_DIR tensorflow/c/c_api.h PATHS /usr/local/include /usr/include)
    if(TENSORFLOW_INCLUDE_DIR)
        add_definitions(-DWITH_TENSORFLOW)
        message(STATUS "TensorFlow C++ support enabled")
    endif()
endif()

# Voice interface libraries
if(ENABLE_VOICE_INTERFACE)
    pkg_check_modules(SPEECH_LIBS QUIET libspeechd)
    if(SPEECH_LIBS_FOUND)
        add_definitions(-DWITH_SPEECH)
        message(STATUS "Speech support enabled")
    endif()
endif()

# Gesture interface libraries
if(ENABLE_GESTURE_INTERFACE)
    find_path(OPENCV_INCLUDE_DIR opencv2/opencv.hpp PATHS /usr/local/include /usr/include)
    if(OPENCV_INCLUDE_DIR)
        add_definitions(-DWITH_OPENCV)
        message(STATUS "OpenCV support enabled for gesture recognition")
    endif()
endif()

# Add compile definitions based on options
if(ENABLE_AI_OPTIMIZATIONS)
    add_definitions(-DENABLE_AI_OPTIMIZATIONS)
endif()

if(ENABLE_CONTINUOUS_LEARNING)
    add_definitions(-DENABLE_CONTINUOUS_LEARNING)
endif()

if(ENABLE_SYSTEM_EVOLUTION)
    add_definitions(-DENABLE_SYSTEM_EVOLUTION)
endif()

if(ENABLE_UNIVERSAL_INTERFACES)
    add_definitions(-DENABLE_UNIVERSAL_INTERFACES)
endif()

# Bootloader
add_subdirectory(bootloader)

# Kernel
add_subdirectory(kernel)

# System services and components
add_subdirectory(system)

# Userspace applications
add_subdirectory(userspace)

# External libraries
if(EXISTS ${CMAKE_SOURCE_DIR}/external)
    add_subdirectory(external)
endif()

# Tests
if(BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif()

# Examples
if(BUILD_EXAMPLES)
    add_subdirectory(examples)
endif()

# Documentation
if(BUILD_DOCUMENTATION)
    find_package(Doxygen)
    if(DOXYGEN_FOUND)
        set(DOXYGEN_IN ${CMAKE_CURRENT_SOURCE_DIR}/docs/Doxyfile.in)
        set(DOXYGEN_OUT ${CMAKE_CURRENT_BINARY_DIR}/Doxyfile)
        
        configure_file(${DOXYGEN_IN} ${DOXYGEN_OUT} @ONLY)
        
        add_custom_target(doc_doxygen ALL
            COMMAND ${DOXYGEN_EXECUTABLE} ${DOXYGEN_OUT}
            WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
            COMMENT "Generating API documentation with Doxygen"
            VERBATIM)
    endif()
endif()

# Create installation package
include(InstallRequiredSystemLibraries)
set(CPACK_RESOURCE_FILE_LICENSE "${CMAKE_CURRENT_SOURCE_DIR}/LICENSE")
set(CPACK_PACKAGE_VERSION_MAJOR "${PROJECT_VERSION_MAJOR}")
set(CPACK_PACKAGE_VERSION_MINOR "${PROJECT_VERSION_MINOR}")
set(CPACK_PACKAGE_VERSION_PATCH "${PROJECT_VERSION_PATCH}")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "AgenticOS - Self-Evolving AI Operating System")
set(CPACK_PACKAGE_VENDOR "AgenticOS Team")
set(CPACK_PACKAGE_CONTACT "support@agentic-os.org")
set(CPACK_GENERATOR "TGZ;DEB;RPM")
set(CPACK_DEBIAN_PACKAGE_DEPENDS "libc6 (>= 2.17), libgcc1 (>= 1:4.1.1), libstdc++6 (>= 4.9)")
set(CPACK_RPM_PACKAGE_REQUIRES "glibc >= 2.17, libgcc >= 4.1.1, libstdc++ >= 4.9")
include(CPack)

# Status summary
message(STATUS "")
message(STATUS "╔═══════════════════════════════════════════════════════════╗")
message(STATUS "║                 AgenticOS Build Configuration             ║")
message(STATUS "╠═══════════════════════════════════════════════════════════╣")
message(STATUS "║ Version: ${PROJECT_VERSION}")
message(STATUS "║ Build type: ${CMAKE_BUILD_TYPE}")
message(STATUS "║ C++ standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "║ Compiler: ${CMAKE_CXX_COMPILER_ID}")
message(STATUS "╠═══════════════════════════════════════════════════════════╣")
message(STATUS "║ AI Optimizations: ${ENABLE_AI_OPTIMIZATIONS}")
message(STATUS "║ GPU Acceleration: ${ENABLE_GPU_ACCELERATION}")
message(STATUS "║ Neural Networks: ${ENABLE_NEURAL_NETWORKS}")
message(STATUS "║ Voice Interface: ${ENABLE_VOICE_INTERFACE}")
message(STATUS "║ Gesture Interface: ${ENABLE_GESTURE_INTERFACE}")
message(STATUS "║ Multimodal Input: ${ENABLE_MULTIMODAL_INPUT}")
message(STATUS "║ Continuous Learning: ${ENABLE_CONTINUOUS_LEARNING}")
message(STATUS "║ System Evolution: ${ENABLE_SYSTEM_EVOLUTION}")
message(STATUS "║ Universal Interfaces: ${ENABLE_UNIVERSAL_INTERFACES}")
message(STATUS "╠═══════════════════════════════════════════════════════════╣")
message(STATUS "║ CUDA Support: ${CUDA_FOUND}")
if(ROCM_INCLUDE_DIR)
    message(STATUS "║ ROCm Support: YES")
else()
    message(STATUS "║ ROCm Support: NO")
endif()
if(TORCH_INCLUDE_DIR)
    message(STATUS "║ PyTorch Support: YES")
else()
    message(STATUS "║ PyTorch Support: NO")
endif()
if(TENSORFLOW_INCLUDE_DIR)
    message(STATUS "║ TensorFlow Support: YES")
else()
    message(STATUS "║ TensorFlow Support: NO")
endif()
message(STATUS "╚═══════════════════════════════════════════════════════════╝")
message(STATUS "")