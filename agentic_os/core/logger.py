import logging
import os
from datetime import datetime
from pathlib import Path

def setup_logging():
    """Setup centralized logging for Agentic OS"""
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Create log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d")
    log_file = log_dir / f"agentic_os_{timestamp}.log"
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    # Create logger
    logger = logging.getLogger("AgenticOS")
    logger.info("Logging system initialized")
    
    return logger

def get_logger(name: str):
    """Get a logger instance for a specific component"""
    return logging.getLogger(f"AgenticOS.{name}")