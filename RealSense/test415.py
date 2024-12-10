import pyrealsense2 as rs
import numpy as np

# Initialize the pipeline and configure the streams
pipeline = rs.pipeline()
config = rs.config()

# Enable left infrared stream (Y8 format, 640x480 resolution)
config.enable_stream(rs.stream.infrared, 1, 1280, 720, rs.format.y8, 30)

# Enable right infrared stream (Y8 format, 640x480 resolution)
config.enable_stream(rs.stream.infrared, 1280, 720, rs.format.y8, 30)

# Start the pipeline
pipeline.start(config)

try:
    while True:
        # Wait for a new set of frames
        frames = pipeline.wait_for_frames()

        # Get the depth frame
        depth_frame = frames.get_depth_frame()

        # Get the infrared frames from left and right IR sensors
        infrared_frame_left = frames.get_infrared_frame(1)  # Left IR sensor
        infrared_frame_right = frames.get_infrared_frame(2)  # Right IR sensor

        # Convert frames to numpy arrays for further processing
        depth_image = np.asanyarray(depth_frame.get_data())
        infrared_image_left = np.asanyarray(infrared_frame_left.get_data())
        infrared_image_right = np.asanyarray(infrared_frame_right.get_data())

        # Process or display the frames
        print("Depth and stereo infrared frames captured.")
finally:
    # Stop the pipeline
    pipeline.stop()
