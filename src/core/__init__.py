"""
Core modules for MusicFun project.

This package contains core functionality including logging, exceptions,
and base classes for the music crawler system.
"""

from .logger import setup_logger, get_logger, log_exception
from .exceptions import (
    MusicFunError,
    CrawlerError,
    NetworkError,
    ParseError,
    ConfigError,
    ValidationError,
    StorageError
)

__all__ = [
    # Logger functions
    'setup_logger',
    'get_logger',
    'log_exception',
    
    # Exception classes
    'MusicFunError',
    'CrawlerError',
    'NetworkError',
    'ParseError',
    'ConfigError',
    'ValidationError',
    'StorageError',
]
