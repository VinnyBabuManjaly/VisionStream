# Handles caching of frames.

from app import app_logger, cache  # Import the global cache instance
from app.config import Config
from typing import Any, Optional  # Import typing utilities for type annotations
import time

# Dictionary to store last cache timestamps
last_cache_time = {}


def cache_frame(key: str, frame: Any, duration: int = Config.CACHE_DURATION) -> None:
    """
    Stores a frame in the cache.

    Args:
        key (str): The unique identifier for the frame in the cache.
        frame (Any): The frame object to be stored (e.g., a NumPy array for images).

    Returns:
        None
    """
    try:
        cache.set(key, frame, timeout=duration)  # Cache for 'duration' seconds
        last_cache_time[key] = time.time()  # Store last cache time
        app_logger.info(f"Frame cached successfully with key: {key}")
    except Exception as e:
        app_logger.error(f"Failed to cache frame with key: {key} - Error: {str(e)}")


def get_cached_frame(key: str) -> Optional[Any]:
    """
    Retrieves a cached frame.

    Args:
        key (str): The unique identifier for the frame in the cache.

    Returns:
        Optional[Any]: The cached frame if available; otherwise, None.
    """
    try:
        cached_frame = cache.get(key)
        if cached_frame is not None:
            app_logger.debug(f"Frame retrieved from cache with key: {key}")
            return cached_frame
        else:
            app_logger.warning(f"No frame found in cache for key: {key}")
            return None
    except Exception as e:
        app_logger.error(
            f"Failed to retrieve frame from cache with key: {key} - Error: {str(e)}"
        )
        return None
