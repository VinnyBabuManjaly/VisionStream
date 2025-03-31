from app import create_app

# Create an instance of the Flask application
app = create_app()

if __name__ == "__main__":
    # Run the Flask application with debug mode equal to False
    # Bind the application to all host "0.0.0.0" for external access
    # Use port 5000 to serve the application
    app.run(debug=False, host="0.0.0.0", port=5000)
