"""
Screenshot Capture Service - Logging Module
Centralized logging with rotation and structured format
"""
import logging
import logging.handlers
from pathlib import Path
import json
from datetime import datetime
import config


class StructuredFormatter(logging.Formatter):
    """Custom formatter for structured logging"""
    
    def format(self, record):
        # Base format: [timestamp] [level] [component] message
        timestamp = datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')
        level = record.levelname
        component = getattr(record, 'component', 'GENERAL')
        message = record.getMessage()
        
        # Add extra data if present
        extra_data = {}
        if hasattr(record, 'data') and record.data:
            extra_data = record.data
        
        # Format base log line
        log_line = f"[{timestamp}] [{level}] [{component}] {message}"
        
        # Append extra data as JSON if present
        if extra_data:
            log_line += f" | Data: {json.dumps(extra_data)}"
        
        return log_line


def setup_logger(name="screenshot-capture", log_file=None, level=None):
    """
    Setup logger with rotation and structured formatting
    
    Args:
        name: Logger name
        log_file: Path to log file (default: from config)
        level: Logging level (default: from config)
    
    Returns:
        Configured logger instance
    """
    # Use config defaults if not provided
    if log_file is None:
        log_file = config.LOG_FILE
    
    if level is None:
        level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)
    
    # Ensure log directory exists
    log_file = Path(log_file)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers to avoid duplicates and ensure fresh handlers
    # This is important when restarting the service
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)
    
    # Create rotating file handler
    file_handler = logging.handlers.RotatingFileHandler(
        str(log_file),
        maxBytes=config.LOG_MAX_SIZE,
        backupCount=config.LOG_BACKUP_COUNT,
        encoding='utf-8'
    )
    file_handler.setLevel(level)
    
    # Create console handler (for development)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # Set formatter
    formatter = StructuredFormatter()
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def get_logger(component="GENERAL"):
    """
    Get logger instance with component name
    
    Args:
        component: Component name (SERVICE, WATCHER, API, etc.)
    
    Returns:
        Logger instance with component set
    """
    logger = logging.getLogger("screenshot-capture")
    
    # Create adapter to add component to all log records
    class ComponentAdapter(logging.LoggerAdapter):
        def process(self, msg, kwargs):
            kwargs.setdefault('extra', {})['component'] = self.extra['component']
            return msg, kwargs
    
    return ComponentAdapter(logger, {'component': component})


# Initialize default logger
default_logger = setup_logger()

# Convenience functions
def log_info(component, message, data=None):
    """Log info message"""
    logger = get_logger(component)
    logger.info(message, extra={'data': data} if data else {})


def log_warning(component, message, data=None):
    """Log warning message"""
    logger = get_logger(component)
    logger.warning(message, extra={'data': data} if data else {})


def log_error(component, message, data=None, exc_info=False):
    """Log error message"""
    logger = get_logger(component)
    logger.error(message, extra={'data': data} if data else {}, exc_info=exc_info)


def log_debug(component, message, data=None):
    """Log debug message"""
    logger = get_logger(component)
    logger.debug(message, extra={'data': data} if data else {})

