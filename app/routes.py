from flask import Blueprint, Response, render_template, request
import cv2
import numpy as np

from app import app_logger
from app import Config
from app.camera import Camera
from app.cache import get_cached_frame

main = Blueprint("main", __name__)

# Create a global Camera instance
camera = Camera()


@main.route("/", methods=["GET", "POST"])
def index():
    # When a POST is received, update camera settings
    if request.method == "POST":
        scale_factor = request.form.get("scale_factor", Config.CAMERA_SCALE_FACTOR)
        gray_intensity = request.form.get(
            "gray_intensity", Config.CAMERA_GRAY_INTENSITY
        )
        channel = request.form.get("channel", Config.CAMERA_CHANNEL)

        camera.update_scale_factor(scale_factor)
        camera.update_gray_intensity(gray_intensity)
        camera.update_channel(channel)

    # Pass FPS and original frame dimensions to the template
    return render_template(
        "index.html", fps=camera.fps, width=camera.width, height=camera.height
    )


@main.route("/video_feed")
def video_feed():
    def generate():
        app_logger.info("Generate video feed from route '/video_feed'")
        while True:
            # Fetch live processed frame first
            frame = camera.get_processed_frame()

            if frame is not None:
                app_logger.info("Serving live frame")
                combined = frame  # Prioritize live frame
            else:
                # If live frame is unavailable, fallback to cached frames
                cached_bgr = get_cached_frame("bgr_frame")
                cached_gray = get_cached_frame("gray_frame")
                cached_channel = get_cached_frame("channel_frame")

                if (
                    cached_bgr is not None
                    and cached_gray is not None
                    and cached_channel is not None
                ):
                    combined = np.hstack([cached_bgr, cached_gray, cached_channel])
                    cv2.putText(
                        combined,
                        "CACHED",
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        2,
                    )
                    app_logger.info("Serving cached frames")
                else:
                    continue  # No frames available, skip this iteration

            ret, buffer = cv2.imencode(".jpg", combined)
            if not ret:
                continue
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n"
            )

    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")
