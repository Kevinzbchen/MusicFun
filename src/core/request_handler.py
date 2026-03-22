"""
HTTP request handler for MusicFun project.

Provides advanced HTTP request functionality with caching, rate limiting,
and connection pooling.
"""

import time
import random
from typing import Dict, List, Optional, Any, Union, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
from urllib.parse import urlparse, urljoin

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

from src.core.logger import create_module_logger
from src.core.exceptions import (
    NetworkError,
    RateLimitError,
    ParseError,
    CrawlerError
)


class RequestHandler:
    """
    Advanced HTTP request handler with caching, rate limiting, and connection pooling.
    """
    
    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3,
        request_delay: float = 1.0,
        user_agent: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
        proxy: Optional[str] = None,
        verify_ssl: bool = True,
        enable_cache: bool = False,
        cache_ttl: int = 300,  # 5 minutes
        rate_limit_per_minute: Optional[int] = None,
        logger_name: Optional[str] = None
    ):
        """
        Initialize the request handler.
        
        Args:
            base_url: Base URL for all requests
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries
            request_delay: Base delay between requests in seconds
            user_agent: User-Agent header
            headers: Additional HTTP headers
            cookies: Cookies to set
            proxy: Proxy server URL
            verify_ssl: Whether to verify SSL certificates
            enable_cache: Enable response caching
            cache_ttl: Cache time-to-live in seconds
            rate_limit_per_minute: Maximum requests per minute
            logger_name: Optional custom logger name
        """
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.request_delay = request_delay
        self.verify_ssl = verify_ssl
        self.enable_cache = enable_cache
        self.cache_ttl = cache_ttl
        self.rate_limit_per_minute = rate_limit_per_minute
        
        # Setup logger
        self.logger = create_module_logger(logger_name or "request_handler")
        
        # Setup session
        self.session = requests.Session()
        self._setup_session(user_agent, headers, cookies, proxy)
        
        # Initialize request tracking
        self.request_count = 0
        self.error_count = 0
        self.start_time = datetime.now()
        self.domain_requests = defaultdict(list)
        
        # Initialize cache
        self.cache: Dict[str, Tuple[datetime, Any]] = {}
        
        self.logger.info(f"RequestHandler initialized with base_url: {base_url}")
    
    def _setup_session(
        self,
        user_agent: Optional[str],
        headers: Optional[Dict[str, str]],
        cookies: Optional[Dict[str, str]],
        proxy: Optional[str]
    ) -> None:
        """Setup HTTP session with advanced configuration."""
        # Set default headers
        default_headers = {
            "User-Agent": user_agent or (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "application/json, text/html, application/xhtml+xml, application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        }
        
        # Update with custom headers
        if headers:
            default_headers.update(headers)
        
        self.session.headers.update(default_headers)
        
        # Set cookies
        if cookies:
            self.session.cookies.update(cookies)
        
        # Set proxy
        if proxy:
            self.session.proxies = {
                "http": proxy,
                "https": proxy
            }
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"],
            raise_on_status=False
        )
        
        # Mount adapters
        adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=10, pool_maxsize=100)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Set SSL verification
        self.session.verify = self.verify_ssl
    
    def _get_cache_key(self, method: str, url: str, params: Dict, data: Any) -> str:
        """Generate cache key for request."""
        import hashlib
        import json
        
        key_data = {
            "method": method,
            "url": url,
            "params": params,
            "data": data
        }
        
        key_str = json.dumps(key_data, sort_keys=True, default=str)
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def _get_from_cache(self, cache_key: str) -> Optional[Any]:
        """Get response from cache if valid."""
        if not self.enable_cache or cache_key not in self.cache:
            return None
        
        cached_time, cached_response = self.cache[cache_key]
        if datetime.now() - cached_time < timedelta(seconds=self.cache_ttl):
            self.logger.debug(f"Cache hit for key: {cache_key[:8]}...")
            return cached_response
        
        # Cache expired
        del self.cache[cache_key]
        return None
    
    def _save_to_cache(self, cache_key: str, response: Any) -> None:
        """Save response to cache."""
        if self.enable_cache:
            self.cache[cache_key] = (datetime.now(), response)
            self.logger.debug(f"Cache saved for key: {cache_key[:8]}...")
    
    def _check_rate_limit(self, url: str) -> None:
        """Check and enforce rate limiting."""
        if not self.rate_limit_per_minute:
            return
        
        domain = urlparse(url).netloc
        now = datetime.now()
        one_minute_ago = now - timedelta(minutes=1)
        
        # Clean old requests
        self.domain_requests[domain] = [
            req_time for req_time in self.domain_requests[domain]
            if req_time > one_minute_ago
        ]
        
        # Check if rate limit exceeded
        if len(self.domain_requests[domain]) >= self.rate_limit_per_minute:
            wait_time = 60 - (now - self.domain_requests[domain][0]).total_seconds()
            self.logger.warning(f"Rate limit exceeded for {domain}. Waiting {wait_time:.1f} seconds.")
            time.sleep(max(0.1, wait_time))
            
            # Re-check after waiting
            self._check_rate_limit(url)
    
    def _apply_request_delay(self, url: str) -> None:
        """Apply delay between requests."""
        # Check rate limit first
        self._check_rate_limit(url)
        
        # Apply base delay with jitter
        jitter = random.uniform(-0.2, 0.2) * self.request_delay
        delay = max(0.1, self.request_delay + jitter)
        
        if delay > 0:
            time.sleep(delay)
        
        # Record request for rate limiting
        domain = urlparse(url).netloc
        self.domain_requests[domain].append(datetime.now())
    
    def request(
        self,
        method: str,
        url: str,
        use_cache: bool = True,
        **kwargs
    ) -> requests.Response:
        """
        Make HTTP request with advanced features.
        
        Args:
            method: HTTP method
            url: Request URL
            use_cache: Whether to use cache for GET requests
            **kwargs: Additional arguments for requests.request
            
        Returns:
            Response object
            
        Raises:
            NetworkError: If request fails
            RateLimitError: If rate limited
        """
        # Define retry decorator
        @retry(
            retry=retry_if_exception_type((NetworkError, RateLimitError)),
            stop=stop_after_attempt(3),
            wait=wait_exponential(multiplier=1, min=2, max=10)
        )
        def _request_with_retry():
            # Build full URL
            if self.base_url and not url.startswith(('http://', 'https://')):
                url_full = urljoin(self.base_url, url)
            else:
                url_full = url
            
            # Check cache for GET requests
            if method.upper() == "GET" and use_cache and self.enable_cache:
                cache_key = self._get_cache_key(method, url_full, kwargs.get('params', {}), kwargs.get('data', {}))
                cached_response = self._get_from_cache(cache_key)
                if cached_response:
                    return cached_response
            
            # Update request count
            self.request_count += 1
            
            # Apply request delay and rate limiting
            self._apply_request_delay(url_full)
            
            try:
                # Make request
                response = self.session.request(
                    method,
                    url_full,
                    timeout=self.timeout,
                    **kwargs
                )
                
                # Check for rate limiting
                if response.status_code == 429:
                    retry_after = response.headers.get("Retry-After", 60)
                    raise RateLimitError(
                        "Rate limit exceeded",
                        url=url_full,
                        retry_after=int(retry_after)
                    )
                
                # Check for other HTTP errors
                if not response.ok:
                    raise NetworkError(
                        f"HTTP {response.status_code}: {response.reason}",
                        url=url_full,
                        status_code=response.status_code,
                        response_text=response.text[:200]
                    )
                
                self.logger.debug(f"Request successful: {method} {url_full} - {response.status_code}")
                
                # Cache successful GET responses
                if method.upper() == "GET" and use_cache and self.enable_cache and response.ok:
                    self._save_to_cache(cache_key, response)
                
                return response
                
            except (requests.RequestException, NetworkError, RateLimitError) as e:
                self.error_count += 1
                self.logger.warning(f"Request failed: {method} {url_full} - {e}")
                raise
        
        return _request_with_retry()
    
    def get(self, url: str, **kwargs) -> requests.Response:
        """Make GET request."""
        return self.request("GET", url, **kwargs)
    
    def post(self, url: str, **kwargs) -> requests.Response:
        """Make POST request."""
        return self.request("POST", url, **kwargs)
    
    def get_json(self, url: str, **kwargs) -> Dict[str, Any]:
        """Make GET request and return JSON."""
        response = self.get(url, **kwargs)
        try:
            return response.json()
        except ValueError as e:
            raise ParseError(
                "Failed to parse JSON response",
                data_type="json",
                raw_data=response.text[:200]
            ) from e
    
    def post_json(self, url: str, **kwargs) -> Dict[str, Any]:
        """Make POST request and return JSON."""
        response = self.post(url, **kwargs)
        try:
            return response.json()
        except ValueError as e:
            raise ParseError(
                "Failed to parse JSON response",
                data_type="json",
                raw_data=response.text[:200]
            ) from e
    
    def get_html(self, url: str, **kwargs) -> str:
        """Make GET request and return HTML."""
        response = self.get(url, **kwargs)
        return response.text
    
    def clear_cache(self) -> None:
        """Clear response cache."""
        self.cache.clear()
        self.logger.info("Cache cleared")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get request handler statistics."""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        
        return {
            "request_count": self.request_count,
            "error_count": self.error_count,
            "success_rate": (self.request_count - self.error_count) / max(self.request_count, 1),
            "elapsed_seconds": elapsed,
            "requests_per_second": self.request_count / max(elapsed, 1),
            "cache_size": len(self.cache),
            "start_time": self.start_time.isoformat(),
        }
    
    def close(self) -> None:
        """Close the request handler."""
        self.session.close()
        stats = self.get_statistics()
        self.logger.info(f"RequestHandler closed. Statistics: {stats}")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# Example usage
if __name__ == "__main__":
    # Create request handler
    handler = RequestHandler(
        base_url="https://httpbin.org",
        timeout=10,
        request_delay=0.5,
        enable_cache=True,
        rate_limit_per_minute=30
    )
    
    try:
        # Test GET request
        response = handler.get("/get")
        print(f"GET request status: {response.status_code}")
        print(f"Response JSON: {response.json()}")
        
        # Test POST request
        response = handler.post("/post", json={"test": "data"})
        print(f"\nPOST request status: {response.status_code}")
        
        # Test cache
        print(f"\nCache test (should be faster):")
        response2 = handler.get("/get")
        print(f"Cached GET request status: {response2.status_code}")
        
        # Get statistics
        stats = handler.get_statistics()
        print(f"\nStatistics: {stats}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        handler.close()
