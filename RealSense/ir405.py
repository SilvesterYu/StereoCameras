import pyrealsense2 as rs
import numpy as np
import cv2  # Optional, if you want to display the image

# Initialize the pipeline
pipeline = rs.pipeline()

# Create a config object
config = rs.config()

# Enable infrared stream (left and right IR cameras)
config.enable_stream(rs.stream.infrared)  # Left IR stream (ID: 1)
config.enable_stream(rs.stream.infrared, 1)  # Right IR stream (ID: 2)

# Start the pipeline with the specified config
pipeline.start(config)

# Wait for frames and capture the left and right IR frames
try:
    while True:
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

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Stop the pipeline after capture
    pipeline.stop()
    cv2.destroyAllWindows()


# import pyrealsense2 as rs

# # Create context to query connected devices
# context = rs.context()

# # Get all connected devices
# devices = context.query_devices()

# # List supported streams for each device
# for device in devices:
#     print(f"Device {device.get_info(rs.camera_info.name)}")
#     for sensor in device.sensors:
#         print(f"  Sensor: {sensor.get_info(rs.camera_info.name)}")
#         for stream in sensor.get_stream_profiles():
#             print(f"    Stream profile: {stream.stream_name()}")