import pyrealsense2 as rs
import numpy as np
import cv2
from PIL import Image
import keyboard

######## Must create a new environment and reinstall all dependenciees with sudo! ###############

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

# Enable color stream (BGR8 format, 640x480 resolution)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Enable infrared stream (Y8 format, 640x480 resolution, from left IR sensor)
config.enable_stream(rs.stream.infrared, 1, 640, 480, rs.format.y8, 30)

# Enable infrared stream (Y8 format, 640x480 resolution, from right IR sensor)
config.enable_stream(rs.stream.infrared, 2, 640, 480, rs.format.y8, 30)


# Start streaming
pipeline.start(config)

# frame counter
count = 0

try:
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()

        ################ RGB and Depth ################
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        color_image = color_image[..., [2, 1, 0]] 

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        # Stack both images horizontally
        images = np.hstack((color_image, depth_colormap))

        # save images

        ####################### IR #######################
        left_ir_frame = frames.get_infrared_frame(1)

        # Get the right IR frame (stream 2)
        right_ir_frame = frames.get_infrared_frame(2)

        # Convert the frames to numpy arrays
        left_ir_image = np.asanyarray(left_ir_frame.get_data())
        right_ir_image = np.asanyarray(right_ir_frame.get_data())

        # Optionally, display the IR frames using OpenCV
        cv2.imshow('Left IR Frame', left_ir_image)
        cv2.imshow('Right IR Frame', right_ir_image)

        # Show images
        cv2.imshow('RealSense', images)
        cv2.waitKey(1)

        # save images
        if keyboard.is_pressed('c'):

            # IR
            image = Image.fromarray(left_ir_image)
            image.save("images/left_ir " + str(count) + " .png")

            image1 = Image.fromarray(right_ir_image)
            image1.save("images/right_ir " + str(count) + " .png")

            # depth
            image2 = Image.fromarray(depth_image)
            image2.save("images/depth_image " + str(count) + " .png")
            print(depth_image.shape)

            # RGB
            image3 = Image.fromarray(color_image)
            image3.save("images/color_image " + str(count) + " .png")
            print(color_image.shape)

            count += 1

        if keyboard.is_pressed('q'):
            break


finally:
    # Stop streaming
    pipeline.stop()