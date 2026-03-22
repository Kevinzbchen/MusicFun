"""
Custom exception classes for MusicFun project.

Defines a hierarchy of exceptions for different error types in the system.
"""

from typing import Optional, Dict, Any


class MusicFunError(Exception):
    """
    Base exception for all MusicFun errors.
    
    All custom exceptions in the project should inherit from this class.
    """
    
    def __init__(self, message: str, error_code: Optional[str] = None, **kwargs):
        """
        Initialize the exception.
        
        Args:
            message: Error message
            error_code: Optional error code for categorization
            **kwargs: Additional context data
        """
        self.message = message
        self.error_code = error_code
        self.context = kwargs
        super().__init__(self.message)
    
    def __str__(self) -> str:
        """String representation of the exception."""
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for serialization."""
        return {
            "error_type": self.__class__.__name__,
            "message": self.message,
            "error_code": self.error_code,
            "context": self.context
        }


class ConfigError(MusicFunError):
    """Exception for configuration-related errors."""
    
    def __init__(self, message: str, config_key: Optional[str] = None, **kwargs):
        """
        Initialize configuration error.
        
        Args:
            message: Error message
            config_key: Configuration key that caused the error
            **kwargs: Additional context
        """
        error_code = "CONFIG_ERROR"
        if config_key:
            message = f"Configuration error for '{config_key}': {message}"
        super().__init__(message, error_code, config_key=config_key, **kwargs)


class ValidationError(MusicFunError):
    """Exception for data validation errors."""
    
    def __init__(self, message: str, field: Optional[str] = None, value: Any = None, **kwargs):
        """
        Initialize validation error.
        
        Args:
            message: Error message
            field: Field that failed validation
            value: Value that caused the validation failure
            **kwargs: Additional context
        """
        error_code = "VALIDATION_ERROR"
        if field:
            message = f"Validation error for field '{field}': {message}"
            if value is not None:
                message = f"{message} (value: {value})"
        super().__init__(message, error_code, field=field, value=value, **kwargs)


class NetworkError(MusicFunError):
    """Exception for network-related errors."""
    
    def __init__(self, message: str, url: Optional[str] = None, status_code: Optional[int] = None, **kwargs):
        """
        Initialize network error.
        
        Args:
            message: Error message
            url: URL that caused the error
            status_code: HTTP status code if applicable
            **kwargs: Additional context
        """
        error_code = "NETWORK_ERROR"
        if url:
            message = f"Network error for URL '{url}': {message}"
        if status_code:
            message = f"{message} (status: {status_code})"
        super().__init__(message, error_code, url=url, status_code=status_code, **kwargs)


class ParseError(MusicFunError):
    """Exception for data parsing errors."""
    
    def __init__(self, message: str, data_type: Optional[str] = None, raw_data: Optional[str] = None, **kwargs):
        """
        Initialize parse error.
        
        Args:
            message: Error message
            data_type: Type of data being parsed (e.g., 'json', 'html', 'xml')
            raw_data: Raw data that failed to parse (truncated)
            **kwargs: Additional context
        """
        error_code = "PARSE_ERROR"
        if data_type:
            message = f"Parse error for {data_type} data: {message}"
        if raw_data:
            # Truncate raw data for readability
            truncated_data = raw_data[:100] + "..." if len(raw_data) > 100 else raw_data
            message = f"{message} (data: {truncated_data})"
        super().__init__(message, error_code, data_type=data_type, raw_data=raw_data, **kwargs)


class CrawlerError(MusicFunError):
    """Exception for crawler-specific errors."""
    
    def __init__(self, message: str, platform: Optional[str] = None, crawler_type: Optional[str] = None, **kwargs):
        """
        Initialize crawler error.
        
        Args:
            message: Error message
            platform: Music platform (e.g., 'netease', 'qq')
            crawler_type: Type of crawler (e.g., 'song', 'comment', 'user')
            **kwargs: Additional context
        """
        error_code = "CRAWLER_ERROR"
        if platform:
            message = f"Crawler error for platform '{platform}': {message}"
        if crawler_type:
            message = f"{message} (crawler type: {crawler_type})"
        super().__init__(message, error_code, platform=platform, crawler_type=crawler_type, **kwargs)


class StorageError(MusicFunError):
    """Exception for data storage errors."""
    
    def __init__(self, message: str, storage_type: Optional[str] = None, operation: Optional[str] = None, **kwargs):
        """
        Initialize storage error.
        
        Args:
            message: Error message
            storage_type: Type of storage (e.g., 'database', 'file', 'cache')
            operation: Storage operation (e.g., 'read', 'write', 'delete')
            **kwargs: Additional context
        """
        error_code = "STORAGE_ERROR"
        if storage_type:
            message = f"Storage error for {storage_type}: {message}"
        if operation:
            message = f"{message} (operation: {operation})"
        super().__init__(message, error_code, storage_type=storage_type, operation=operation, **kwargs)


class RateLimitError(NetworkError):
    """Exception for rate limiting errors."""
    
    def __init__(self, message: str, url: Optional[str] = None, retry_after: Optional[int] = None, **kwargs):
        """
        Initialize rate limit error.
        
        Args:
            message: Error message
            url: URL that hit rate limit
            retry_after: Seconds to wait before retrying
            **kwargs: Additional context
        """
        error_code = "RATE_LIMIT_ERROR"
        if not message:
            message = "Rate limit exceeded"
        if retry_after:
            message = f"{message}. Retry after {retry_after} seconds."
        super().__init__(message, url, error_code=error_code, retry_after=retry_after, **kwargs)


class AuthenticationError(MusicFunError):
    """Exception for authentication errors."""
    
    def __init__(self, message: str, auth_type: Optional[str] = None, **kwargs):
        """
        Initialize authentication error.
        
        Args:
            message: Error message
            auth_type: Type of authentication (e.g., 'cookie', 'token', 'oauth')
            **kwargs: Additional context
        """
        error_code = "AUTHENTICATION_ERROR"
        if auth_type:
            message = f"Authentication error for {auth_type}: {message}"
        super().__init__(message, error_code, auth_type=auth_type, **kwargs)


class ResourceNotFoundError(MusicFunError):
    """Exception for resource not found errors."""
    
    def __init__(self, message: str, resource_type: Optional[str] = None, resource_id: Optional[str] = None, **kwargs):
        """
        Initialize resource not found error.
        
        Args:
            message: Error message
            resource_type: Type of resource (e.g., 'song', 'user', 'playlist')
            resource_id: ID of the resource
            **kwargs: Additional context
        """
        error_code = "RESOURCE_NOT_FOUND"
        if resource_type and resource_id:
            message = f"{resource_type} with ID '{resource_id}' not found: {message}"
        elif resource_type:
            message = f"{resource_type} not found: {message}"
        super().__init__(message, error_code, resource_type=resource_type, resource_id=resource_id, **kwargs)


# Utility functions for exception handling

def wrap_exception(
    exception: Exception,
    wrapper_class: type,
    message: Optional[str] = None,
    **kwargs
) -> MusicFunError:
    """
    Wrap a generic exception in a MusicFun exception.
    
    Args:
        exception: Original exception to wrap
        wrapper_class: MusicFun exception class to wrap with
        message: Custom message (uses original if not provided)
        **kwargs: Additional context for the wrapper exception
        
    Returns:
        Wrapped exception
    """
    if message is None:
        message = str(exception)
    
    return wrapper_class(message, **kwargs)


def raise_with_context(
    exception_class: type,
    message: str,
    logger=None,
    log_level: str = "ERROR",
    **kwargs
) -> None:
    """
    Raise an exception and log it with context.
    
    Args:
        exception_class: Exception class to raise
        message: Error message
        logger: Logger instance (optional)
        log_level: Log level for the error
        **kwargs: Context data for the exception
        
    Raises:
        exception_class: The specified exception
    """
    # Create the exception
    exc = exception_class(message, **kwargs)
    
    # Log if logger is provided
    if logger:
        log_method = getattr(logger, log_level.lower(), logger.error)
        context_str = ", ".join(f"{k}={v}" for k, v in kwargs.items())
        log_msg = f"{message}"
        if context_str:
            log_msg = f"{log_msg} | Context: {context_str}"
        log_method(log_msg)
    
    raise exc


# Example usage
if __name__ == "__main__":
    # Test exception hierarchy
    try:
        raise ConfigError("Missing required configuration", config_key="api_key")
    except ConfigError as e:
        print(f"ConfigError caught: {e}")
        print(f"Exception dict: {e.to_dict()}")
    
    print()
    
    try:
        raise ValidationError("Value must be positive", field="duration", value=-10)
    except ValidationError as e:
        print(f"ValidationError caught: {e}")
    
    print()
    
    try:
        raise NetworkError("Connection failed", url="https://api.example.com", status_code=500)
    except NetworkError as e:
        print(f"NetworkError caught: {e}")
    
    print()
    
    # Test wrapping
    try:
        result = 1 / 0
    except ZeroDivisionError as e:
        wrapped = wrap_exception(e, CrawlerError, platform="netease")
        print(f"Wrapped exception: {wrapped}")
    
    print("\nAll exception tests completed.")
