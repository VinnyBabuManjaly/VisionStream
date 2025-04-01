from flask import Flask
from flask_caching import Cache
from app.config import Config
import logging

# Initialize a Cache object to be used across the application
cache = Cache()

app_logger = logging.getLogger(__name__)  # Create a global logger


def create_app():
    """
    Factory function to create and configure a Flask application instance.
    This pattern enables modularity and flexibility for scaling and testing.
    """
    # Create an instance of the Flask application
    app = Flask(__name__, template_folder="../templates")

    # Load configuration settings from the Config class
    app.config.from_object(Config)

    # Configure application-wide logging
    logging.basicConfig(
        level=app.config.get("LOGGING_LEVEL", "INFO"),  # Set logging level
        format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    )
    app.logger.info("Application initialized successfully")

    cache.init_app(app)  # Initialize cache with Flask

    # Import routes after initializing Flask to prevent circular imports
    from app.routes import main

    # Register the main blueprint
    app.register_blueprint(main)

    # Return the configured Flask application instance
    return app
