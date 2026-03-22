"""
Base crawler abstract class.
All output in English, ASCII only.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from src.core.logger import get_logger

# Get configured logger
logger = get_logger()


class BaseCrawler(ABC):
    """Abstract base class for all music platform crawlers."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize crawler with configuration."""
        self.config = config
        self.base_url = config.get("base_url", "")
        self.timeout = config.get("timeout", 10)
        self.request_delay = config.get("request_delay", 1)
        self.retry_times = config.get("retry_times", 3)

        # Create session with retry strategy
        self.session = self._create_session()

        # Set headers if provided
        headers = config.get("headers", {})
        if headers:
            self.session.headers.update(headers)

        logger.info(f"Crawler initialized: {self.__class__.__name__}")

    def _create_session(self) -> requests.Session:
        """Create a requests session with retry strategy."""
        session = requests.Session()

        # Configure retry strategy
        retry_strategy = Retry(
            total=self.retry_times,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    def _make_request(self, url: str, method: str = "GET", **kwargs) -> Optional[requests.Response]:
        """Make HTTP request with simple retry logic."""
        for attempt in range(self.retry_times):
            try:
                logger.debug(f"{method} {url}")
                response = self.session.request(
                    method=method.upper(),
                    url=url,
                    timeout=self.timeout,
                    **kwargs
                )
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt == self.retry_times - 1:
                    logger.error(f"All retries failed for {url}")
                    return None
                time.sleep(2 ** attempt)  # Exponential backoff

        return None

    def _delay(self):
        """Add delay between requests to avoid rate limiting."""
        if self.request_delay > 0:
            time.sleep(self.request_delay)

    @abstractmethod
    def search(self, keyword: str, limit: int = 50, **kwargs) -> List[Any]:
        """Search for items by keyword."""
        pass

    @abstractmethod
    def get_comments(self, item_id: int, limit: int = 20, **kwargs) -> List[Any]:
        """Get comments for an item."""
        pass

    @abstractmethod
    def get_song(self, song_id: int) -> Optional[Any]:
        """Get song details."""
        pass

    @abstractmethod
    def get_user(self, user_id: int) -> Optional[Any]:
        """Get user details."""
        pass

    def close(self):
        """Close the session."""
        if self.session:
            self.session.close()
            logger.debug("Session closed")