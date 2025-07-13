#!/usr/bin/env python3
"""
NexusOS Installation Script
Production-ready operating system installer
"""

import os
import sys
import subprocess
import shutil
import logging
from pathlib import Path

def setup_logging():
    """Setup logging for installation"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('/tmp/nexus_install.log', mode='w')
        ]
    )
    return logging.getLogger(__name__)

def check_system_requirements():
    """Check if system meets requirements"""
    logger = logging.getLogger(__name__)
    
    # Check Python version
    if sys.version_info < (3, 8):
        logger.error("Python 3.8 or higher is required")
        return False
    
    # Check available memory
    try:
        import psutil
        memory = psutil.virtual_memory()
        if memory.total < 2 * 1024 * 1024 * 1024:  # 2GB
            logger.warning("Less than 2GB RAM available, performance may be affected")
    except ImportError:
        logger.warning("Cannot check memory requirements")
    
    # Check disk space
    disk = shutil.disk_usage('/')
    if disk.free < 10 * 1024 * 1024 * 1024:  # 10GB
        logger.error("At least 10GB free disk space is required")
        return False
    
    logger.info("System requirements check passed")
    return True

def install_dependencies():
    """Install Python dependencies"""
    logger = logging.getLogger(__name__)
    
    try:
        # Install pip if not available
        subprocess.run([sys.executable, '-m', 'ensurepip', '--default-pip'], check=True)
        
        # Upgrade pip
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], check=True)
        
        # Install requirements
        requirements_file = Path(__file__).parent / 'requirements.txt'
        if requirements_file.exists():
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)], check=True)
            logger.info("Dependencies installed successfully")
        else:
            # Install essential packages manually
            packages = ['psutil>=5.9.0', 'cryptography>=41.0.0']
            for package in packages:
                subprocess.run([sys.executable, '-m', 'pip', 'install', package], check=True)
            logger.info("Essential packages installed")
        
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install dependencies: {e}")
        return False

def create_system_directories():
    """Create NexusOS system directories"""
    logger = logging.getLogger(__name__)
    
    # System directories
    directories = [
        Path.home() / '.nexus',
        Path.home() / '.nexus' / 'apps',
        Path.home() / '.nexus' / 'data',
        Path.home() / '.nexus' / 'config',
        Path.home() / '.nexus' / 'cache',
        Path.home() / '.nexus' / 'security',
        Path.home() / '.nexus' / 'logs',
        Path.home() / '.nexus' / 'runtime'
    ]
    
    for directory in directories:
        try:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {directory}")
        except Exception as e:
            logger.error(f"Failed to create directory {directory}: {e}")
            return False
    
    return True

def create_startup_script():
    """Create startup script for NexusOS"""
    logger = logging.getLogger(__name__)
    
    try:
        startup_script = Path.home() / '.nexus' / 'start_nexus.py'
        
        script_content = f'''#!/usr/bin/env python3
"""
NexusOS Startup Script
"""

import sys
import os
import asyncio
from pathlib import Path

# Add NexusOS to Python path
nexus_path = Path(__file__).parent.parent / 'nexus_os'
sys.path.insert(0, str(nexus_path))

try:
    from system.runtime.nexus import run_nexus
    
    if __name__ == "__main__":
        # Set high priority
        try:
            os.nice(-10)
        except PermissionError:
            print("Warning: Could not set high priority (requires root)")
        
        # Run NexusOS
        asyncio.run(run_nexus())
        
except ImportError as e:
    print(f"Error importing NexusOS: {{e}}")
    print("Please ensure NexusOS is properly installed")
    sys.exit(1)
'''
        
        with open(startup_script, 'w') as f:
            f.write(script_content)
        
        # Make executable
        os.chmod(startup_script, 0o755)
        
        logger.info(f"Created startup script: {startup_script}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to create startup script: {e}")
        return False

def create_service_file():
    """Create systemd service file for NexusOS"""
    logger = logging.getLogger(__name__)
    
    try:
        service_content = f'''[Unit]
Description=NexusOS - Advanced Operating System
After=network.target

[Service]
Type=simple
User={os.getenv('USER', 'nexus')}
WorkingDirectory={Path.home() / '.nexus'}
ExecStart={sys.executable} {Path.home() / '.nexus' / 'start_nexus.py'}
Restart=always
RestartSec=2
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
'''
        
        service_file = Path('/tmp/nexus-os.service')
        with open(service_file, 'w') as f:
            f.write(service_content)
        
        logger.info(f"Created service file: {service_file}")
        logger.info("To install as system service, run:")
        logger.info(f"  sudo cp {service_file} /etc/systemd/system/")
        logger.info("  sudo systemctl daemon-reload")
        logger.info("  sudo systemctl enable nexus-os")
        logger.info("  sudo systemctl start nexus-os")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to create service file: {e}")
        return False

def main():
    """Main installation function"""
    logger = setup_logging()
    
    logger.info("Starting NexusOS installation...")
    
    # Check system requirements
    if not check_system_requirements():
        logger.error("System requirements not met")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        logger.error("Failed to install dependencies")
        sys.exit(1)
    
    # Create system directories
    if not create_system_directories():
        logger.error("Failed to create system directories")
        sys.exit(1)
    
    # Create startup script
    if not create_startup_script():
        logger.error("Failed to create startup script")
        sys.exit(1)
    
    # Create service file
    create_service_file()
    
    logger.info("NexusOS installation completed successfully!")
    logger.info("")
    logger.info("To start NexusOS:")
    logger.info(f"  python3 {Path.home() / '.nexus' / 'start_nexus.py'}")
    logger.info("")
    logger.info("For system-wide installation, follow the systemd service instructions above.")
    
    print("\n🎉 NexusOS is ready to use!")
    print(f"📁 Installation directory: {Path.home() / '.nexus'}")
    print(f"📜 Logs: {Path.home() / '.nexus' / 'logs'}")
    print(f"🚀 Start with: python3 {Path.home() / '.nexus' / 'start_nexus.py'}")

if __name__ == "__main__":
    main()