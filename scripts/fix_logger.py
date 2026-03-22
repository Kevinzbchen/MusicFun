"""
Logger configuration for MusicFun project.
All output in English, ASCII only.
"""
import sys
from pathlib import Path
from loguru import logger

# Global flag to prevent duplicate initialization
_LOGGER_INITIALIZED = False


def setup_logger(log_level: str = "INFO", log_dir: Path = None):
    """
    Setup logger configuration.
    
    Args:
        log_level: Log level (DEBUG, INFO, WARNING, ERROR)
        log_dir: Directory for log files
    
    Returns:
        Configured logger instance
    """
    global _LOGGER_INITIALIZED

    # Return existing logger if already initialized
    if _LOGGER_INITIALIZED:
        return logger

    # Remove default handler
    logger.remove()

    # Add console handler with colored output
    logger.add(
        sys.stdout,
        level=log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )

    # Add file handler if log_dir provided
    if log_dir:
        log_dir = Path(log_dir)
        log_dir.mkdir(parents=True, exist_ok=True)

        # Main log file
        logger.add(
            log_dir / "musicfun.log",
            level=log_level,
            rotation="500 MB",
            retention="10 days",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            encoding="utf-8"
        )

        # Error log file (only ERROR level)
        logger.add(
            log_dir / "musicfun_error.log",
            level="ERROR",
            rotation="100 MB",
            retention="30 days",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            encoding="utf-8"
        )

        logger.info(f"Logger initialized. Log directory: {log_dir}")
        logger.info(f"Log level: {log_level}")
        logger.info(f"Log file: musicfun.log")
        logger.info(f"Error file: musicfun_error.log")

    _LOGGER_INITIALIZED = True
    return logger


def get_logger():
    """Get the configured logger instance."""
    return logger


# Create a default logger instance
default_logger = logger