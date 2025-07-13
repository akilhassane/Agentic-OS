"""
NexusOS Application Manager - Universal Software Execution
Runs any application: games, IDEs, editors, SDKs, and all software
"""

import asyncio
import os
import sys
import subprocess
import signal
import shutil
import json
import time
import logging
import threading
import psutil
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import tempfile
import zipfile
import tarfile

logger = logging.getLogger(__name__)

class AppType(Enum):
    NATIVE = "native"
    WINE = "wine"
    CONTAINER = "container"
    FLATPAK = "flatpak"
    SNAP = "snap"
    APPIMAGE = "appimage"
    PYTHON = "python"
    NODEJS = "nodejs"
    JAVA = "java"
    DOTNET = "dotnet"
    BROWSER = "browser"

class AppState(Enum):
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPING = "stopping"
    CRASHED = "crashed"

@dataclass
class Application:
    app_id: str
    name: str
    executable: str
    app_type: AppType
    version: str
    description: str
    icon_path: Optional[str] = None
    install_path: Optional[str] = None
    config_path: Optional[str] = None
    data_path: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    environment: Dict[str, str] = field(default_factory=dict)
    arguments: List[str] = field(default_factory=list)
    working_directory: Optional[str] = None
    
@dataclass
class RunningApp:
    application: Application
    process: subprocess.Popen
    state: AppState
    started_at: float
    pid: int
    memory_usage: int = 0
    cpu_usage: float = 0.0
    
class AppManager:
    """Universal application manager"""
    
    def __init__(self):
        self.applications = {}
        self.running_apps = {}
        self.app_store = {}
        self.install_queue = []
        self.monitor_thread = None
        self.running = False
        
        # Application directories
        self.app_dir = Path.home() / ".nexus" / "apps"
        self.data_dir = Path.home() / ".nexus" / "data"
        self.config_dir = Path.home() / ".nexus" / "config"
        self.cache_dir = Path.home() / ".nexus" / "cache"
        
        # Create directories
        for directory in [self.app_dir, self.data_dir, self.config_dir, self.cache_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    async def start(self):
        """Start the application manager"""
        logger.info("Starting NexusOS Application Manager")
        self.running = True
        
        # Load installed applications
        await self._load_applications()
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self._monitor_apps, daemon=True)
        self.monitor_thread.start()
        
        # Initialize runtime environments
        await self._initialize_runtimes()
        
        logger.info("Application manager started successfully")
    
    async def _load_applications(self):
        """Load installed applications from disk"""
        try:
            apps_file = self.config_dir / "applications.json"
            if apps_file.exists():
                with open(apps_file, 'r') as f:
                    apps_data = json.load(f)
                    
                for app_data in apps_data:
                    app = Application(**app_data)
                    self.applications[app.app_id] = app
                    
            logger.info(f"Loaded {len(self.applications)} applications")
            
        except Exception as e:
            logger.error(f"Failed to load applications: {e}")
    
    async def _save_applications(self):
        """Save applications to disk"""
        try:
            apps_file = self.config_dir / "applications.json"
            apps_data = []
            
            for app in self.applications.values():
                app_dict = {
                    'app_id': app.app_id,
                    'name': app.name,
                    'executable': app.executable,
                    'app_type': app.app_type.value,
                    'version': app.version,
                    'description': app.description,
                    'icon_path': app.icon_path,
                    'install_path': app.install_path,
                    'config_path': app.config_path,
                    'data_path': app.data_path,
                    'dependencies': app.dependencies,
                    'environment': app.environment,
                    'arguments': app.arguments,
                    'working_directory': app.working_directory
                }
                apps_data.append(app_dict)
            
            with open(apps_file, 'w') as f:
                json.dump(apps_data, f, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to save applications: {e}")
    
    async def _initialize_runtimes(self):
        """Initialize runtime environments"""
        # Check for Wine
        if shutil.which("wine"):
            logger.info("Wine runtime available")
            
        # Check for Docker
        if shutil.which("docker"):
            logger.info("Docker runtime available")
            
        # Check for Flatpak
        if shutil.which("flatpak"):
            logger.info("Flatpak runtime available")
            
        # Check for Snap
        if shutil.which("snap"):
            logger.info("Snap runtime available")
            
        # Check for Python
        if shutil.which("python3"):
            logger.info("Python runtime available")
            
        # Check for Node.js
        if shutil.which("node"):
            logger.info("Node.js runtime available")
            
        # Check for Java
        if shutil.which("java"):
            logger.info("Java runtime available")
            
        # Check for .NET
        if shutil.which("dotnet"):
            logger.info(".NET runtime available")
    
    async def install_application(self, package_path: str, app_type: AppType = AppType.NATIVE) -> bool:
        """Install an application from package"""
        try:
            logger.info(f"Installing application from {package_path}")
            
            package_path = Path(package_path)
            if not package_path.exists():
                logger.error(f"Package not found: {package_path}")
                return False
            
            # Create temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # Extract package
                if package_path.suffix == '.zip':
                    with zipfile.ZipFile(package_path, 'r') as zip_ref:
                        zip_ref.extractall(temp_path)
                elif package_path.suffix in ['.tar.gz', '.tgz']:
                    with tarfile.open(package_path, 'r:gz') as tar_ref:
                        tar_ref.extractall(temp_path)
                elif package_path.suffix == '.AppImage':
                    # AppImage - just copy
                    shutil.copy2(package_path, temp_path / package_path.name)
                else:
                    # Copy as-is
                    shutil.copy2(package_path, temp_path / package_path.name)
                
                # Find executable
                executable = await self._find_executable(temp_path, app_type)
                if not executable:
                    logger.error("No executable found in package")
                    return False
                
                # Generate app ID
                app_id = package_path.stem.replace(' ', '_').lower()
                
                # Install to app directory
                install_path = self.app_dir / app_id
                install_path.mkdir(exist_ok=True)
                
                # Copy files
                for item in temp_path.iterdir():
                    if item.is_file():
                        shutil.copy2(item, install_path)
                    elif item.is_dir():
                        shutil.copytree(item, install_path / item.name, dirs_exist_ok=True)
                
                # Create application entry
                app = Application(
                    app_id=app_id,
                    name=package_path.stem,
                    executable=str(install_path / executable.name),
                    app_type=app_type,
                    version="1.0.0",
                    description=f"Installed from {package_path.name}",
                    install_path=str(install_path),
                    config_path=str(self.config_dir / app_id),
                    data_path=str(self.data_dir / app_id)
                )
                
                # Make executable
                os.chmod(app.executable, 0o755)
                
                # Register application
                self.applications[app_id] = app
                await self._save_applications()
                
                logger.info(f"Application {app.name} installed successfully")
                return True
                
        except Exception as e:
            logger.error(f"Failed to install application: {e}")
            return False
    
    async def _find_executable(self, path: Path, app_type: AppType) -> Optional[Path]:
        """Find executable in extracted package"""
        try:
            # Common executable patterns
            executable_patterns = [
                "*.exe", "*.run", "*.sh", "*.py", "*.jar", "*.AppImage"
            ]
            
            # Look for executables
            for pattern in executable_patterns:
                for file in path.rglob(pattern):
                    if file.is_file() and os.access(file, os.X_OK):
                        return file
            
            # Look for files with execute permission
            for file in path.rglob("*"):
                if file.is_file() and os.access(file, os.X_OK):
                    return file
            
            return None
            
        except Exception as e:
            logger.error(f"Error finding executable: {e}")
            return None
    
    async def launch_application(self, app_id: str, arguments: List[str] = None) -> bool:
        """Launch an application"""
        try:
            if app_id not in self.applications:
                logger.error(f"Application {app_id} not found")
                return False
            
            if app_id in self.running_apps:
                logger.warning(f"Application {app_id} is already running")
                return True
            
            app = self.applications[app_id]
            logger.info(f"Launching application: {app.name}")
            
            # Prepare command
            cmd = await self._prepare_command(app, arguments or [])
            
            # Set environment
            env = os.environ.copy()
            env.update(app.environment)
            
            # Set working directory
            cwd = app.working_directory or app.install_path or os.getcwd()
            
            # Launch process
            process = subprocess.Popen(
                cmd,
                env=env,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid
            )
            
            # Create running app entry
            running_app = RunningApp(
                application=app,
                process=process,
                state=AppState.STARTING,
                started_at=time.time(),
                pid=process.pid
            )
            
            self.running_apps[app_id] = running_app
            
            # Wait a moment to check if it started successfully
            await asyncio.sleep(0.5)
            
            if process.poll() is None:
                running_app.state = AppState.RUNNING
                logger.info(f"Application {app.name} started successfully (PID: {process.pid})")
                return True
            else:
                # Process exited immediately
                running_app.state = AppState.CRASHED
                logger.error(f"Application {app.name} failed to start")
                return False
                
        except Exception as e:
            logger.error(f"Failed to launch application {app_id}: {e}")
            return False
    
    async def _prepare_command(self, app: Application, arguments: List[str]) -> List[str]:
        """Prepare command based on application type"""
        cmd = []
        
        if app.app_type == AppType.NATIVE:
            cmd = [app.executable] + app.arguments + arguments
            
        elif app.app_type == AppType.WINE:
            cmd = ["wine", app.executable] + app.arguments + arguments
            
        elif app.app_type == AppType.PYTHON:
            cmd = ["python3", app.executable] + app.arguments + arguments
            
        elif app.app_type == AppType.NODEJS:
            cmd = ["node", app.executable] + app.arguments + arguments
            
        elif app.app_type == AppType.JAVA:
            cmd = ["java", "-jar", app.executable] + app.arguments + arguments
            
        elif app.app_type == AppType.DOTNET:
            cmd = ["dotnet", app.executable] + app.arguments + arguments
            
        elif app.app_type == AppType.APPIMAGE:
            cmd = [app.executable] + app.arguments + arguments
            
        elif app.app_type == AppType.FLATPAK:
            cmd = ["flatpak", "run", app.executable] + app.arguments + arguments
            
        elif app.app_type == AppType.SNAP:
            cmd = ["snap", "run", app.executable] + app.arguments + arguments
            
        elif app.app_type == AppType.CONTAINER:
            cmd = ["docker", "run", "--rm", "-it", app.executable] + app.arguments + arguments
            
        else:
            cmd = [app.executable] + app.arguments + arguments
        
        return cmd
    
    async def stop_application(self, app_id: str) -> bool:
        """Stop a running application"""
        try:
            if app_id not in self.running_apps:
                logger.warning(f"Application {app_id} is not running")
                return True
            
            running_app = self.running_apps[app_id]
            running_app.state = AppState.STOPPING
            
            logger.info(f"Stopping application: {running_app.application.name}")
            
            # Try graceful shutdown first
            try:
                os.killpg(os.getpgid(running_app.process.pid), signal.SIGTERM)
                
                # Wait for graceful shutdown
                for _ in range(10):  # Wait up to 10 seconds
                    if running_app.process.poll() is not None:
                        break
                    await asyncio.sleep(1)
                
                # Force kill if still running
                if running_app.process.poll() is None:
                    os.killpg(os.getpgid(running_app.process.pid), signal.SIGKILL)
                    
            except ProcessLookupError:
                # Process already dead
                pass
            
            # Clean up
            running_app.state = AppState.STOPPED
            del self.running_apps[app_id]
            
            logger.info(f"Application {running_app.application.name} stopped")
            return True
            
        except Exception as e:
            logger.error(f"Failed to stop application {app_id}: {e}")
            return False
    
    async def pause_application(self, app_id: str) -> bool:
        """Pause a running application"""
        try:
            if app_id not in self.running_apps:
                return False
            
            running_app = self.running_apps[app_id]
            if running_app.state != AppState.RUNNING:
                return False
            
            # Send SIGSTOP to pause
            os.killpg(os.getpgid(running_app.process.pid), signal.SIGSTOP)
            running_app.state = AppState.PAUSED
            
            logger.info(f"Application {running_app.application.name} paused")
            return True
            
        except Exception as e:
            logger.error(f"Failed to pause application {app_id}: {e}")
            return False
    
    async def resume_application(self, app_id: str) -> bool:
        """Resume a paused application"""
        try:
            if app_id not in self.running_apps:
                return False
            
            running_app = self.running_apps[app_id]
            if running_app.state != AppState.PAUSED:
                return False
            
            # Send SIGCONT to resume
            os.killpg(os.getpgid(running_app.process.pid), signal.SIGCONT)
            running_app.state = AppState.RUNNING
            
            logger.info(f"Application {running_app.application.name} resumed")
            return True
            
        except Exception as e:
            logger.error(f"Failed to resume application {app_id}: {e}")
            return False
    
    def _monitor_apps(self):
        """Monitor running applications"""
        while self.running:
            try:
                current_time = time.time()
                crashed_apps = []
                
                for app_id, running_app in self.running_apps.items():
                    try:
                        # Check if process is still running
                        if running_app.process.poll() is not None:
                            # Process has exited
                            if running_app.state == AppState.RUNNING:
                                running_app.state = AppState.CRASHED
                                crashed_apps.append(app_id)
                        else:
                            # Update resource usage
                            try:
                                proc = psutil.Process(running_app.pid)
                                running_app.memory_usage = proc.memory_info().rss
                                running_app.cpu_usage = proc.cpu_percent()
                            except psutil.NoSuchProcess:
                                crashed_apps.append(app_id)
                                
                    except Exception as e:
                        logger.error(f"Error monitoring app {app_id}: {e}")
                
                # Clean up crashed apps
                for app_id in crashed_apps:
                    if app_id in self.running_apps:
                        running_app = self.running_apps[app_id]
                        logger.warning(f"Application {running_app.application.name} crashed")
                        del self.running_apps[app_id]
                
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"App monitoring error: {e}")
                time.sleep(5)
    
    async def get_running_applications(self) -> List[RunningApp]:
        """Get list of running applications"""
        return list(self.running_apps.values())
    
    async def get_installed_applications(self) -> List[Application]:
        """Get list of installed applications"""
        return list(self.applications.values())
    
    async def uninstall_application(self, app_id: str) -> bool:
        """Uninstall an application"""
        try:
            if app_id not in self.applications:
                return False
            
            # Stop if running
            if app_id in self.running_apps:
                await self.stop_application(app_id)
            
            app = self.applications[app_id]
            
            # Remove files
            if app.install_path and Path(app.install_path).exists():
                shutil.rmtree(app.install_path)
            
            if app.config_path and Path(app.config_path).exists():
                shutil.rmtree(app.config_path)
            
            if app.data_path and Path(app.data_path).exists():
                shutil.rmtree(app.data_path)
            
            # Remove from registry
            del self.applications[app_id]
            await self._save_applications()
            
            logger.info(f"Application {app.name} uninstalled")
            return True
            
        except Exception as e:
            logger.error(f"Failed to uninstall application {app_id}: {e}")
            return False
    
    async def tick(self):
        """Application manager tick - called by kernel"""
        # Process install queue
        if self.install_queue:
            package_path, app_type = self.install_queue.pop(0)
            await self.install_application(package_path, app_type)
    
    async def shutdown(self):
        """Shutdown application manager"""
        logger.info("Shutting down application manager")
        self.running = False
        
        # Stop all running applications
        for app_id in list(self.running_apps.keys()):
            await self.stop_application(app_id)
        
        # Save applications
        await self._save_applications()
        
        logger.info("Application manager shutdown complete")