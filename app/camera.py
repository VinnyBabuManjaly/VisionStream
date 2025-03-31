import cv2
import threading
import time
import numpy as np

from app.cache import cache_frame
from app.config import Config
from app import app_logger


class Camera:
    def __init__(
        self,
        src=Config.CAMERA_SRC,
        scale_factor=Config.CAMERA_SCALE_FACTOR,
        gray_intensity=Config.CAMERA_GRAY_INTENSITY,
        channel=Config.CAMERA_CHANNEL,
    ):
        self.src = src
        self.cap = cv2.VideoCapture(self.src, cv2.CAP_DSHOW)

        # Retrieve video properties
        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30  # fallback if FPS is 0
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.scale_factor = scale_factor
        self.gray_intensity = gray_intensity
        self.channel = channel  # expected values: 'blue', 'green', 'red'

        # Thread safety
        self.lock = threading.Lock()
        self.processed_frame = None

        # Cache variables: if a frame was updated less than cache_duration
        # seconds ago, mark it
        self.last_cache_time = Config.LAST_CACHE_TIME
        self.cache_duration = Config.CACHE_DURATION  # seconds

        self.running = True
        # Start background thread to capture and process frames
        self.thread = threading.Thread(target=self.update, daemon=True)
        self.thread.start()

    def update(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                continue
            with self.lock:
                new_width = int(frame.shape[1] * self.scale_factor)
                new_height = int(frame.shape[0] * self.scale_factor)
                resized_frame = cv2.resize(
                    frame, (new_width, new_height), interpolation=cv2.INTER_LINEAR
                )

                # Generate BGR (original)
                bgr_frame = resized_frame.copy()

                # Generate grayscale
                gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
                gray_frame = np.clip(
                    gray_frame.astype(np.float32) * float(self.gray_intensity), 0, 255
                ).astype(np.uint8)
                gray_bgr = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)

                # Generate channel-specific frames
                channel_idx = {"blue": 0, "green": 1, "red": 2}.get(self.channel, 0)
                channel_img = resized_frame.copy()
                for i in range(3):
                    if i != channel_idx:
                        channel_img[:, :, i] = 0

                # Always update self.processed_frame for live streaming
                # Concatenate images horizontally
                self.processed_frame = np.hstack([bgr_frame, gray_bgr, channel_img])

                # Cache handling
                # Check if frames are already cached
                current_time = time.time()
                if current_time - self.last_cache_time >= self.cache_duration:
                    app_logger.info("Updating cached frames")
                    cache_frame("bgr_frame", bgr_frame)
                    cache_frame("gray_frame", gray_bgr)
                    cache_frame("channel_frame", channel_img)
                    self.last_cache_time = current_time

            # Sleep briefly to match approximately the FPS of the source
            time.sleep(1.0 / self.fps)

    def get_processed_frame(self):
        with self.lock:
            if self.processed_frame is None:
                return None
            return self.processed_frame.copy()

    def update_scale_factor(self, scale_factor):
        try:
            scale_factor = float(scale_factor)
            with self.lock:
                if 0.1 <= scale_factor <= 3.0:  # Set a reasonable limit
                    self.scale_factor = scale_factor
        except ValueError:
            pass

    def update_gray_intensity(self, intensity):
        with self.lock:
            self.gray_intensity = intensity

    def update_channel(self, channel):
        with self.lock:
            self.channel = channel

    def release(self):
        self.running = False
        self.thread.join()
        self.cap.release()
