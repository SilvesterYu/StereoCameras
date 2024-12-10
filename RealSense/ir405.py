import pyrealsense2 as rs
import numpy as np
import cv2  # Optional, if you want to display the image
from PIL import Image

# Initialize the pipeline
pipeline = rs.pipeline()

# Create a config object
config = rs.config()

# Enable infrared stream (left and right IR cameras)
config.enable_stream(rs.stream.infrared)  # Left IR stream (ID: 1)
config.enable_stream(rs.stream.infrared, 1)  # Right IR stream (ID: 2)

# Start the pipeline with the specified config
pipeline.start(config)

# frame counter
count = 0

# Wait for frames and capture the left and right IR frames
try:
    while True:
        count += 1

        # Wait for a new set of frames from the camera
        frames = pipeline.wait_for_frames()

        # Get the left IR frame (stream 1)
        left_ir_frame = frames.get_infrared_frame()

        # Get the right IR frame (stream 2)
        right_ir_frame = frames.get_infrared_frame(1)

        # Convert the frames to numpy arrays
        left_ir_image = np.asanyarray(left_ir_frame.get_data())
        right_ir_image = np.asanyarray(right_ir_frame.get_data())

        # Optionally, display the IR frames using OpenCV
        cv2.imshow('Left IR Frame', left_ir_image)
        cv2.imshow('Right IR Frame', right_ir_image)

        if count == 10:
            # Convert the NumPy array to a Pillow Image object
            image = Image.fromarray(left_ir_image)
            # Save the image as a PNG file
            image.save("images/left_ir.png")

            # Convert the NumPy array to a Pillow Image object
            image1 = Image.fromarray(right_ir_image)
            # Save the image as a PNG file
            image1.save("images/right_ir.png")

            # grayscale
            grayscale_image = Image.fromarray(left_ir_image)
            grayscale_image.save("images/grayscale_left_ir.png")

            grayscale_image1 = Image.fromarray(right_ir_image)
            grayscale_image1.save("images/grayscale_right_ir.png")

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Stop the pipeline after capture
    pipeline.stop()
    cv2.destroyAllWindows()

