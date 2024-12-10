
import pyrealsense2 as rs

# Create context to query connected devices
context = rs.context()

# Get all connected devices
devices = context.query_devices()

# List supported streams for each device
for device in devices:
    print(f"Device {device.get_info(rs.camera_info.name)}")
    for sensor in device.sensors:
        print(f"  Sensor: {sensor.get_info(rs.camera_info.name)}")
        for stream in sensor.get_stream_profiles():
            print(f"    Stream profile: {stream.stream_name()}")