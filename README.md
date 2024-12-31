# StereoCameras

Stereo camera code

## Install Realsense SDK

Installation guide here: [https://github.com/IntelRealSense/librealsense/blob/master/doc/distribution_linux.md](https://github.com/IntelRealSense/librealsense/blob/master/doc/distribution_linux.md)

Run `realsense-viewer` to view camera input

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

`python3 <filename>.py`

the filenames indicate what data it retrieves from the camera
