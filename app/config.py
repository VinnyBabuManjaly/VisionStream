class Config:
    # Cache configuration
    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 30
    LAST_CACHE_TIME = 0
    CACHE_DURATION = 30

    # Default camera settings
    CAMERA_SRC = 1  # Default source (e.g., webcam)
    CAMERA_SCALE_FACTOR = 1.0  # Default scale factor
    CAMERA_GRAY_INTENSITY = 1.0  # Default gray intensity
    CAMERA_CHANNEL = "blue"  # Default color channel ('blue', 'green', 'red')

    # Logging configuration
    LOGGING_LEVEL = "INFO"  # Set default logging level
