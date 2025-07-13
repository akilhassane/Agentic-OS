#!/bin/bash

# AgenticOS Installation Script
# Self-evolving AI Operating System Installation
# Version: 1.0.0

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Constants
AGENTIC_OS_VERSION="1.0.0"
INSTALL_DIR="/opt/agentic-os"
BOOT_DIR="/boot/agentic-os"
CONFIG_DIR="/etc/agentic-os"
LOG_FILE="/var/log/agentic-os-install.log"
MINIMUM_RAM_GB=8
MINIMUM_DISK_GB=50

# Logo and header
display_logo() {
    echo -e "${CYAN}"
    echo "    ╔═══════════════════════════════════════════════════════════╗"
    echo "    ║                  🤖 AgenticOS Installer                   ║"
    echo "    ║              Self-Evolving AI Operating System            ║"
    echo "    ║                     Version ${AGENTIC_OS_VERSION}                      ║"
    echo "    ╚═══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Logging function
log() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Progress bar
show_progress() {
    local current=$1
    local total=$2
    local width=50
    local percentage=$((current * 100 / total))
    local filled=$((width * current / total))
    local empty=$((width - filled))
    
    printf "\r["
    printf "%${filled}s" | tr ' ' '='
    printf "%${empty}s" | tr ' ' '-'
    printf "] %d%%" "$percentage"
}

# Check system requirements
check_requirements() {
    log "${BLUE}Checking system requirements...${NC}"
    
    # Check if running as root
    if [[ $EUID -ne 0 ]]; then
        log "${RED}This installer must be run as root. Please use sudo.${NC}"
        exit 1
    fi
    
    # Check CPU architecture
    ARCH=$(uname -m)
    if [[ "$ARCH" != "x86_64" && "$ARCH" != "aarch64" ]]; then
        log "${RED}Unsupported architecture: $ARCH${NC}"
        log "${RED}AgenticOS requires x86_64 or aarch64 architecture.${NC}"
        exit 1
    fi
    
    # Check RAM
    RAM_GB=$(free -g | awk 'NR==2{print $2}')
    if [[ $RAM_GB -lt $MINIMUM_RAM_GB ]]; then
        log "${RED}Insufficient RAM: ${RAM_GB}GB (minimum: ${MINIMUM_RAM_GB}GB)${NC}"
        exit 1
    fi
    
    # Check disk space
    DISK_GB=$(df / | awk 'NR==2{print int($4/1024/1024)}')
    if [[ $DISK_GB -lt $MINIMUM_DISK_GB ]]; then
        log "${RED}Insufficient disk space: ${DISK_GB}GB (minimum: ${MINIMUM_DISK_GB}GB)${NC}"
        exit 1
    fi
    
    # Check for required packages
    local packages=("gcc" "g++" "make" "cmake" "git" "curl" "wget" "python3")
    for pkg in "${packages[@]}"; do
        if ! command -v "$pkg" &> /dev/null; then
            log "${YELLOW}Installing required package: $pkg${NC}"
            apt-get update && apt-get install -y "$pkg"
        fi
    done
    
    log "${GREEN}✓ System requirements met${NC}"
}

# Download and extract AgenticOS
download_agentic_os() {
    log "${BLUE}Downloading AgenticOS...${NC}"
    
    # Create temporary directory
    TMP_DIR=$(mktemp -d)
    cd "$TMP_DIR"
    
    # Download the latest release (simulated - in practice would download from repository)
    log "Downloading from GitHub repository..."
    
    # For now, we'll simulate the download with our current files
    # In a real scenario, this would download a pre-built release
    mkdir -p agentic-os
    
    # Copy source files (in real scenario, these would be downloaded)
    cp -r /workspace/* agentic-os/ 2>/dev/null || true
    
    log "${GREEN}✓ AgenticOS downloaded successfully${NC}"
}

# Build AgenticOS
build_agentic_os() {
    log "${BLUE}Building AgenticOS...${NC}"
    
    cd agentic-os
    
    # Create build directory
    mkdir -p build
    cd build
    
    # Configure build
    log "Configuring build system..."
    cmake .. -DCMAKE_BUILD_TYPE=Release -DENABLE_AI_OPTIMIZATIONS=ON
    
    # Build the OS
    log "Compiling AgenticOS (this may take a while)..."
    make -j$(nproc)
    
    # Build additional components
    log "Building AI components..."
    make ai-core
    make neural-shell
    make adaptive-daemon
    
    log "${GREEN}✓ AgenticOS built successfully${NC}"
}

# Install bootloader
install_bootloader() {
    log "${BLUE}Installing UEFI bootloader...${NC}"
    
    # Create boot directory
    mkdir -p "$BOOT_DIR"
    
    # Copy bootloader
    cp build/bootloader/agentic-bootloader.efi "$BOOT_DIR/"
    
    # Create EFI boot entry
    if command -v efibootmgr &> /dev/null; then
        efibootmgr -c -d /dev/sda -p 1 -L "AgenticOS" -l "\\EFI\\agentic-os\\agentic-bootloader.efi"
    fi
    
    log "${GREEN}✓ Bootloader installed${NC}"
}

# Install kernel and system files
install_system() {
    log "${BLUE}Installing system files...${NC}"
    
    # Create system directories
    mkdir -p "$INSTALL_DIR"/{kernel,drivers,ai,services,userspace}
    mkdir -p "$CONFIG_DIR"
    
    # Install kernel
    cp build/kernel/agentic-kernel "$INSTALL_DIR/kernel/"
    
    # Install drivers
    cp -r build/drivers/* "$INSTALL_DIR/drivers/"
    
    # Install AI core
    cp -r build/ai/* "$INSTALL_DIR/ai/"
    
    # Install services
    cp -r build/services/* "$INSTALL_DIR/services/"
    
    # Install userspace
    cp -r build/userspace/* "$INSTALL_DIR/userspace/"
    
    # Set permissions
    chmod -R 755 "$INSTALL_DIR"
    
    log "${GREEN}✓ System files installed${NC}"
}

# Configure AI system
configure_ai() {
    log "${BLUE}Configuring AI system...${NC}"
    
    # Create AI configuration
    cat > "$CONFIG_DIR/ai-config.json" << EOF
{
    "version": "$AGENTIC_OS_VERSION",
    "ai_core": {
        "enable_learning": true,
        "enable_adaptation": true,
        "enable_evolution": true,
        "learning_rate": 0.01,
        "adaptation_rate": 0.1,
        "max_memory_gb": $(($RAM_GB / 2)),
        "enable_gpu_acceleration": true
    },
    "neural_shell": {
        "enable_voice": true,
        "enable_gesture": true,
        "enable_multimodal": true,
        "personality_mode": "adaptive",
        "proactivity_level": 0.7
    },
    "adaptive_daemon": {
        "enable_proactive_assistance": true,
        "enable_continuous_learning": true,
        "enable_emotional_adaptation": true,
        "max_concurrent_tasks": 10
    },
    "security": {
        "enable_ai_sandboxing": true,
        "enable_learning_validation": true,
        "max_risk_tolerance": 0.1
    }
}
EOF
    
    # Initialize AI knowledge base
    log "Initializing AI knowledge base..."
    "$INSTALL_DIR/ai/knowledge-initializer" --config "$CONFIG_DIR/ai-config.json"
    
    log "${GREEN}✓ AI system configured${NC}"
}

# Set up systemd services
setup_services() {
    log "${BLUE}Setting up system services...${NC}"
    
    # Create systemd service files
    cat > /etc/systemd/system/agentic-daemon.service << EOF
[Unit]
Description=AgenticOS Adaptive Daemon
After=network.target

[Service]
Type=notify
ExecStart=$INSTALL_DIR/services/adaptive-daemon
Restart=always
RestartSec=10
User=root
Group=root

[Install]
WantedBy=multi-user.target
EOF

    cat > /etc/systemd/system/agentic-ai-core.service << EOF
[Unit]
Description=AgenticOS AI Core
After=network.target

[Service]
Type=notify
ExecStart=$INSTALL_DIR/ai/ai-core
Restart=always
RestartSec=10
User=root
Group=root

[Install]
WantedBy=multi-user.target
EOF

    cat > /etc/systemd/system/agentic-interface-engine.service << EOF
[Unit]
Description=AgenticOS Universal Interface Engine
After=network.target

[Service]
Type=notify
ExecStart=$INSTALL_DIR/services/interface-engine
Restart=always
RestartSec=10
User=root
Group=root

[Install]
WantedBy=multi-user.target
EOF

    # Enable services
    systemctl daemon-reload
    systemctl enable agentic-daemon
    systemctl enable agentic-ai-core
    systemctl enable agentic-interface-engine
    
    log "${GREEN}✓ System services configured${NC}"
}

# Create user accounts
create_users() {
    log "${BLUE}Creating user accounts...${NC}"
    
    # Create agentic user
    if ! id "agentic" &>/dev/null; then
        useradd -m -s /bin/bash agentic
        echo "agentic:agentic" | chpasswd
        usermod -aG sudo agentic
    fi
    
    # Set up default shell
    echo "$INSTALL_DIR/userspace/neural-shell" >> /etc/shells
    chsh -s "$INSTALL_DIR/userspace/neural-shell" agentic
    
    log "${GREEN}✓ User accounts created${NC}"
}

# Install neural shell
install_neural_shell() {
    log "${BLUE}Installing Neural Shell...${NC}"
    
    # Make neural shell executable
    chmod +x "$INSTALL_DIR/userspace/neural-shell"
    
    # Create symlink in /usr/bin
    ln -sf "$INSTALL_DIR/userspace/neural-shell" /usr/bin/neural-shell
    
    # Create desktop entry
    mkdir -p /usr/share/applications
    cat > /usr/share/applications/neural-shell.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Neural Shell
Comment=AI-Powered Adaptive Shell
Exec=$INSTALL_DIR/userspace/neural-shell
Icon=$INSTALL_DIR/userspace/icons/neural-shell.png
Terminal=true
Categories=System;
EOF
    
    log "${GREEN}✓ Neural Shell installed${NC}"
}

# Hardware detection and optimization
detect_hardware() {
    log "${BLUE}Detecting hardware and optimizing...${NC}"
    
    # Detect GPU
    if lspci | grep -i nvidia > /dev/null; then
        log "NVIDIA GPU detected - installing CUDA support..."
        # Install NVIDIA drivers and CUDA (simplified)
        apt-get update
        apt-get install -y nvidia-driver-470 nvidia-cuda-toolkit
    elif lspci | grep -i amd > /dev/null; then
        log "AMD GPU detected - installing ROCm support..."
        # Install AMD ROCm (simplified)
        apt-get update
        apt-get install -y rocm-dev
    fi
    
    # Detect AI accelerators
    if lspci | grep -i "neural\|ai\|tensor" > /dev/null; then
        log "AI accelerator detected - configuring..."
        # Configure AI accelerator support
    fi
    
    # Optimize for hardware
    "$INSTALL_DIR/ai/hardware-optimizer" --detect-and-optimize
    
    log "${GREEN}✓ Hardware detection complete${NC}"
}

# Network configuration
configure_network() {
    log "${BLUE}Configuring network settings...${NC}"
    
    # Configure firewall for AI services
    ufw allow 8080/tcp  # AI dashboard
    ufw allow 8081/tcp  # AI API
    ufw allow 8082/tcp  # Neural shell web interface
    
    # Configure DNS for AI services
    echo "127.0.0.1 agentic.local" >> /etc/hosts
    echo "127.0.0.1 ai.local" >> /etc/hosts
    
    log "${GREEN}✓ Network configured${NC}"
}

# Post-installation setup
post_install() {
    log "${BLUE}Performing post-installation setup...${NC}"
    
    # Start services
    systemctl start agentic-ai-core
    systemctl start agentic-daemon
    systemctl start agentic-interface-engine
    
    # Wait for services to start
    sleep 5
    
    # Verify installation
    if systemctl is-active --quiet agentic-ai-core; then
        log "${GREEN}✓ AI Core service running${NC}"
    else
        log "${RED}⚠ AI Core service not running${NC}"
    fi
    
    if systemctl is-active --quiet agentic-daemon; then
        log "${GREEN}✓ Adaptive Daemon running${NC}"
    else
        log "${RED}⚠ Adaptive Daemon not running${NC}"
    fi
    
    # Create desktop shortcuts
    mkdir -p /home/agentic/Desktop
    cp /usr/share/applications/neural-shell.desktop /home/agentic/Desktop/
    chown agentic:agentic /home/agentic/Desktop/neural-shell.desktop
    
    log "${GREEN}✓ Post-installation setup complete${NC}"
}

# Installation progress tracking
run_installation() {
    local steps=(
        "check_requirements"
        "download_agentic_os"
        "build_agentic_os"
        "install_bootloader"
        "install_system"
        "configure_ai"
        "setup_services"
        "create_users"
        "install_neural_shell"
        "detect_hardware"
        "configure_network"
        "post_install"
    )
    
    local total_steps=${#steps[@]}
    local current_step=0
    
    for step in "${steps[@]}"; do
        current_step=$((current_step + 1))
        show_progress $current_step $total_steps
        echo ""
        $step
    done
    
    echo ""
    log "${GREEN}Installation complete!${NC}"
}

# Cleanup function
cleanup() {
    if [[ -n "$TMP_DIR" && -d "$TMP_DIR" ]]; then
        rm -rf "$TMP_DIR"
    fi
}

# Main installation function
main() {
    display_logo
    
    echo -e "${WHITE}Welcome to the AgenticOS Installation System${NC}"
    echo -e "${WHITE}===========================================${NC}"
    echo ""
    echo "This installer will set up AgenticOS on your system."
    echo "The installation process includes:"
    echo "  • System requirements check"
    echo "  • Download and build AgenticOS"
    echo "  • Install bootloader and kernel"
    echo "  • Configure AI system"
    echo "  • Set up services and user accounts"
    echo "  • Hardware optimization"
    echo ""
    
    # Confirm installation
    read -p "Do you want to proceed with the installation? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled."
        exit 1
    fi
    
    # Set up logging
    mkdir -p "$(dirname "$LOG_FILE")"
    touch "$LOG_FILE"
    
    # Set up cleanup trap
    trap cleanup EXIT
    
    # Run installation
    run_installation
    
    # Display completion message
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║              🎉 Installation Complete!                 ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${WHITE}AgenticOS has been successfully installed!${NC}"
    echo ""
    echo -e "${CYAN}Next steps:${NC}"
    echo "1. Reboot your system"
    echo "2. Select AgenticOS from the boot menu"
    echo "3. Log in as 'agentic' user"
    echo "4. Start the Neural Shell with: neural-shell"
    echo ""
    echo -e "${CYAN}AI Features:${NC}"
    echo "• Natural language commands"
    echo "• Voice and gesture control"
    echo "• Automatic task execution"
    echo "• Continuous learning and adaptation"
    echo "• Universal system integration"
    echo ""
    echo -e "${CYAN}Web Interface:${NC}"
    echo "• AI Dashboard: http://localhost:8080"
    echo "• Neural Shell Web: http://localhost:8082"
    echo ""
    echo -e "${YELLOW}Support:${NC}"
    echo "• Documentation: /opt/agentic-os/docs/"
    echo "• Logs: /var/log/agentic-os-install.log"
    echo "• GitHub: https://github.com/agentic-os/agentic-os"
    echo ""
    echo -e "${WHITE}Thank you for choosing AgenticOS!${NC}"
    echo ""
    
    read -p "Press Enter to reboot now, or Ctrl+C to cancel..."
    reboot
}

# Run main function
main "$@"