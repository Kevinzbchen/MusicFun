"""
Logging configuration for MusicFun project.

Uses loguru for flexible and powerful logging with file rotation and formatting.
"""

import sys
from pathlib import Path
from typing import Optional, Dict, Any
from loguru import logger

# Remove default handler
logger.remove()

# Default log format (ASCII only)
DEFAULT_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "<level>{message}</level>"
)

# Default log levels
LOG_LEVELS = {
    "DEBUG": "DEBUG",
    "INFO": "INFO",
    "WARNING": "WARNING",
    "ERROR": "ERROR",
    "CRITICAL": "CRITICAL",
}

# Global logger instance
_logger_instance = None


def setup_logger(
    log_dir: Optional[Path] = None,
    log_level: str = "INFO",
    log_file: str = "musicfun.log",
    error_file: str = "musicfun_error.log",
    rotation: str = "10 MB",
    retention: str = "30 days",
    compression: str = "zip",
    console_output: bool = True,
    file_output: bool = True,
    format_string: Optional[str] = None
) -> logger:
    """
    Setup and configure the logger.
    
    Args:
        log_dir: Directory for log files. If None, uses 'data/logs/'
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Name of the main log file
        error_file: Name of the error log file
        rotation: When to rotate logs (size or time)
        retention: How long to keep logs
        compression: Compression format for rotated logs
        console_output: Whether to output to console
        file_output: Whether to output to file
        format_string: Custom format string for logs
        
    Returns:
        Configured logger instance
    """
    global _logger_instance
    
    # Set default log directory
    if log_dir is None:
        # Use project root/data/logs
        project_root = Path(__file__).parent.parent.parent
        log_dir = project_root / "data" / "logs"
    
    # Create log directory if it doesn't exist
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Use default format if none provided
    if format_string is None:
        format_string = DEFAULT_FORMAT
    
    # Configure console output
    if console_output:
        logger.add(
            sys.stderr,
            format=format_string,
            level=log_level,
            colorize=True,
            backtrace=True,
            diagnose=True
        )
    
    # Configure file output for all logs
    if file_output:
        log_file_path = log_dir / log_file
        logger.add(
            str(log_file_path),
            format=format_string,
            level=log_level,
            rotation=rotation,
            retention=retention,
            compression=compression,
            backtrace=True,
            diagnose=True,
            encoding="utf-8"
        )
    
    # Configure error log file (only ERROR and above)
    if file_output:
        error_file_path = log_dir / error_file
        logger.add(
            str(error_file_path),
            format=format_string,
            level="ERROR",
            rotation=rotation,
            retention=retention,
            compression=compression,
            backtrace=True,
            diagnose=True,
            encoding="utf-8"
        )
    
    # Set the global instance
    _logger_instance = logger
    
    # Log initialization
    logger.info(f"Logger initialized. Log directory: {log_dir}")
    logger.info(f"Log level: {log_level}")
    logger.info(f"Log file: {log_file}")
    logger.info(f"Error file: {error_file}")
    
    return logger


def get_logger() -> logger:
    """
    Get the configured logger instance.
    
    Returns:
        Logger instance. If not configured, returns default logger.
    """
    global _logger_instance
    
    if _logger_instance is None:
        # Return default logger with basic configuration
        logger.warning("Logger not configured. Using default configuration.")
        return logger
    
    return _logger_instance


def log_exception(
    exception: Exception,
    message: Optional[str] = None,
    level: str = "ERROR",
    context: Optional[Dict[str, Any]] = None
) -> None:
    """
    Log an exception with additional context.
    
    Args:
        exception: The exception to log
        message: Custom message to include
        level: Log level (ERROR, WARNING, etc.)
        context: Additional context data to log
    """
    logger_instance = get_logger()
    
    # Build log message
    log_msg = message or f"Exception occurred: {type(exception).__name__}"
    
    # Add context if provided
    if context:
        context_str = ", ".join(f"{k}={v}" for k, v in context.items())
        log_msg = f"{log_msg} | Context: {context_str}"
    
    # Log with appropriate level
    if level.upper() == "DEBUG":
        logger_instance.debug(log_msg)
        logger_instance.debug(f"Exception details: {exception}")
    elif level.upper() == "INFO":
        logger_instance.info(log_msg)
        logger_instance.info(f"Exception details: {exception}")
    elif level.upper() == "WARNING":
        logger_instance.warning(log_msg)
        logger_instance.warning(f"Exception details: {exception}")
    elif level.upper() == "CRITICAL":
        logger_instance.critical(log_msg)
        logger_instance.critical(f"Exception details: {exception}")
    else:  # Default to ERROR
        logger_instance.error(log_msg)
        logger_instance.error(f"Exception details: {exception}")
    
    # Log traceback for debugging
    logger_instance.opt(exception=exception).error("Exception traceback:")


def create_module_logger(module_name: str) -> logger:
    """
    Create a logger for a specific module with module name in format.
    
    Args:
        module_name: Name of the module (e.g., 'crawler.netease')
        
    Returns:
        Logger instance configured for the module
    """
    # Create a custom format with module name
    module_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        f"<cyan>{module_name}</cyan>:<cyan>{{function}}</cyan>:<cyan>{{line}}</cyan> | "
        "<level>{message}</level>"
    )
    
    # Get base logger
    base_logger = get_logger()
    
    # Create a new logger with module-specific format
    # Note: loguru doesn't support changing format per logger easily,
    # so we return the base logger but log messages will include module name
    return base_logger.bind(module=module_name)


# Default logger configuration
if _logger_instance is None:
    # Auto-configure with defaults if not already configured
    try:
        setup_logger()
    except Exception as e:
        # Fallback to basic console logging
        logger.add(sys.stderr, format=DEFAULT_FORMAT, level="INFO")
        logger.warning(f"Failed to setup file logging: {e}")


# Example usage
if __name__ == "__main__":
    # Test the logger
    log = get_logger()
    
    log.debug("This is a debug message")
    log.info("This is an info message")
    log.warning("This is a warning message")
    log.error("This is an error message")
    
    # Test exception logging
    try:
        result = 1 / 0
    except ZeroDivisionError as e:
        log_exception(
            e,
            message="Division by zero error",
            context={"operation": "division", "numerator": 1, "denominator": 0}
        )
    
    # Test module logger
    module_logger = create_module_logger("test.module")
    module_logger.info("Module-specific log message")
    
    print("\nLogger test completed. Check log files in data/logs/ directory.")
