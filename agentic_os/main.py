#!/usr/bin/env python3
"""
Agentic OS - Main Entry Point
"""

import asyncio
import signal
import sys
from pathlib import Path
import uvicorn
from dotenv import load_dotenv

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from agentic_os.core.os_controller import AgenticOSController
from agentic_os.api.server import create_app
from agentic_os.core.logger import setup_logging

class AgenticOS:
    def __init__(self):
        self.controller = None
        self.app = None
        self.running = False
    
    async def start(self):
        """Start the Agentic OS"""
        print("🚀 Starting Agentic OS...")
        
        # Load environment variables
        load_dotenv('config/.env')
        
        # Setup logging
        setup_logging()
        
        # Initialize core controller
        self.controller = AgenticOSController()
        await self.controller.start()
        
        # Create FastAPI app
        self.app = create_app(self.controller)
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        self.running = True
        print("✅ Agentic OS started successfully!")
        print("📊 Dashboard: http://localhost:8080")
        print("📚 API Docs: http://localhost:8080/docs")
        
        # Start the web server
        config = uvicorn.Config(
            self.app,
            host="0.0.0.0",
            port=8080,
            log_level="info"
        )
        server = uvicorn.Server(config)
        await server.serve()
    
    def _signal_handler(self, sig, frame):
        """Handle shutdown signals"""
        print("\n🛑 Shutting down Agentic OS...")
        self.running = False
        if self.controller:
            asyncio.create_task(self.controller.stop())
        sys.exit(0)
    
    async def stop(self):
        """Stop the Agentic OS"""
        if self.controller:
            await self.controller.stop()
        self.running = False

async def main():
    """Main function"""
    os_instance = AgenticOS()
    try:
        await os_instance.start()
    except KeyboardInterrupt:
        await os_instance.stop()
    except Exception as e:
        print(f"❌ Failed to start Agentic OS: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())