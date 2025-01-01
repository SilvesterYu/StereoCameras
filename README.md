# StereoCameras

Camera code for 3D reconstruction. Cameras used: Realsense & Kinect. SDK installation guide for both can be found below. Make sure that the cameras' data cables are connected to your computer's USB3 ports.

## 📷 Install Realsense SDK

First follow guide here: [https://github.com/IntelRealSense/librealsense/blob/master/doc/distribution_linux.md](https://github.com/IntelRealSense/librealsense/blob/master/doc/distribution_linux.md)

To check if it's correctly installed, open a new terminal and run `realsense-viewer` to view camera input

If `realsense-viewer` command not found, run:

`sudo apt-get install librealsense2-dkms librealsense2-utils`

## Environment Setup

Must create a conda environment with python==3.7

`conda create -m realsense python=3.7`

`conda activate realsense`

`pip install pyrealsense2`

`pip install opencv-python`

`pip install numpy`

`pip install Pillow`

Finally, create a folder to store images `mkdir images`

## To Run

`cd RealSense`

`python3 <filename>.py`

the filenames indicate what data it retrieves from the camera

## 📷 Install Kinect SDK

`cd Kinect`

Run the bash script, change the ubuntu version to yours `bash install_azure_kinect_camera_u_20.04.sh`

Open a new terminal and run `k4aviewer`
