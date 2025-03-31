Vision Stream
======================================

VisionStream is a real-time video streaming and processing application built with Flask and OpenCV. It captures live video, applies transformations (grayscale, color channel filtering, resizing), and caches frames for efficient retrieval. The application features a web UI for interactive control.

🚀 **Running the Application**
------------------------------

### 1\. **Flask Setup**

To run the application locally, use the following steps:

#### **Step 1: Clone the Repository**

Clone the repository to your local machine:

```bash
git clone https://your-repository-url.git
cd your-repository-folder
```


#### **Step 2: Install Dependencies**

Install the required Python dependencies. It's recommended to use a virtual environment.

```bash
python3 -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate  # For Windows
pip install -r requirements.txt
```


#### **Step 3: Running the Flask Application**

Run the Flask development server:
```bash
flask run
```
This will start the Flask application, and you can access the video stream at http://127.0.0.1:5000/.

### 2\. **Docker Setup**

If you prefer to run the application in a Docker container, follow these steps:

#### **Step 1: Build the Docker Image**

First, ensure that you have Docker installed. Then, build the Docker image:

```bash
docker build -t video-stream-app .
```
#### **Step 2: Run the Docker Container**

Run the Docker container:

```bash
docker run -p 5000:5000 video-stream-app
```
The application will be available at http://127.0.0.1:5000/video\_feed in your browser.

💻 **File Structure**
---------------------

```bash
├── app
│   ├── __init__.py
│   ├── camera.py       # Video capturing and processing logic
│   ├── cache.py        # Caching logic for frames
│   ├── config.py       # Configuration settings (e.g., camera source)
│   ├── routes.py       # Flask routes
│   └── tests           # Folder for unit and integration
├── Dockerfile          # Docker configuration
├── requirements.txt    # Python dependencies
├── run.py              # Entry point for running the Flask application
└── README.md           # Documentation (this file)
```

🔧 **Core Features**
--------------------

*   **Live Video Feed**: Streams video in real-time using OpenCV.

*   **Cached Video Frames**: Frames are cached for fast access, reducing the load on the system.

*   **Adjustable Settings**: Dynamic control of scale factor, grayscale intensity, and video channel via the Flask web UI.

*   **Real-Time Processing**: Processed frames (e.g., BGR, Grayscale, Channel) are concatenated and served live.

*   **Threading**: A background thread captures and processes video frames.


🛠 **Configuration**
--------------------

The configuration for the application is handled in app/config.py.

💡 **Caching**
--------------

The frames are cached using the cache.py module. Frames are stored in memory for quick access. The cache is updated every 30 seconds, and the cached frames are retrieved whenever possible to reduce processing time.

🖥 **Flask Routes**
-------------------

The main route (/video\_feed) serves the video stream. It checks if cached frames are available and serves them if they exist. If the cached frames are not available, it fetches the live frames from the camera.


🐳 **Dockerfile**
-----------------

The Dockerfile defines the steps required to create a Docker image for this application.

🔄 **Pre-commit Hook Setup**
----------------------------

To ensure code consistency and avoid errors, set up pre-commit hooks in your project. This can be done by following these steps:

### **Step 1: Install Pre-commit**

```bash
pip install pre-commit
```

### **Step 2: Install the Hooks**

Run the following command to install the hooks:

```bash
pre-commit install
```
This will automatically run the hooks on every commit to ensure that the code is properly formatted.

**Future Testing Plans**
------------------------

This project aims to maintain high code quality through comprehensive testing. Planning to implement the following tests:

* **Unit Tests:**
    * Individual components like `camera.py`, `cache.py`, and `config.py` will be tested in isolation to ensure their functionality.
    * These tests will cover various scenarios, including normal operations, edge cases, and error handling.
* **Integration Tests:**
    * The interaction between different modules, especially `routes.py` and its dependencies (camera, cache, config), will be tested.
    * These tests will verify that the application behaves correctly as a whole.

The `tests` directory within the project structure will house these tests, organized by module for clarity and maintainability.
