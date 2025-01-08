import matplotlib.pyplot as plt
import numpy as np
import open3d as o3d
import threading
from pyzed import sl
import pyzed
import argparse

# Originally written by: Mino Nakura

class ZedCameraManager:
    
    def __init__(self):
        self.id_to_cam = self.init_zed_cameras()

    def capture_pcd(self):
        """Capture images from all zed cameras.
        
        Returns:
            dict of camera id to image
        """
        condition = threading.Condition()
        id_to_pcd = {}
        threads = []
        for cam_id, camera in self.id_to_cam.items():
            t = threading.Thread(target=ZedCameraManager.get_single_pcd,
                                 args=(cam_id, camera, id_to_pcd, condition))
            t.start()
            threads.append(t)    
        with condition:
            condition.notify_all()
        for t in threads:
            t.join()
        return id_to_pcd

    def capture_images(self):
        """Capture images from all zed cameras.
        
        Returns:
            dict of camera id to image {int: np.array[H,W,3]}
        """
        condition = threading.Condition()
        id_to_image = {}
        threads = []
        for cam_id, camera in self.id_to_cam.items():
            t = threading.Thread(target=ZedCameraManager.get_single_image,
                                 args=(cam_id, camera, id_to_image, condition))
            t.start()
            threads.append(t)    
        with condition:
            condition.notify_all()
        for t in threads:
            t.join()
        return id_to_image

    @staticmethod
    def get_single_image(cam_id, camera, id_to_image, condition=None):
        """Capture a single image from a zed camera. Modifies id_to_image[cam_id]
           to store the captured image. Captured image is stored as numpy array
        
        Args:
            cam_id: int, camera id
            camera: zed camera object
            id_to_image: dict where the captured image is stored
            condition: threading.Condition object, used to synchronize camera capture time
        """
        if condition is not None:
            with condition:
                condition.wait()
        image = sl.Mat()
        runtime_parameters = sl.RuntimeParameters()
        if camera.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            camera.retrieve_image(image, sl.VIEW.LEFT)
            id_to_image[cam_id] = image.get_data().copy()

    @staticmethod
    def get_image_pair(cam_id, camera, image_pair, condition=None):
        """Capture a single image from a zed camera. Modifies id_to_image[cam_id]
           to store the captured image. Captured image is stored as numpy array
        
        Args:
            cam_id: int, camera id
            camera: zed camera object
            image_pair: dict where the captured image pair is stored
            condition: threading.Condition object, used to synchronize camera capture time
        """
        if condition is not None:
            with condition:
                condition.wait()
        image = sl.Mat()
        runtime_parameters = sl.RuntimeParameters()
        if camera.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            camera.retrieve_image(image, sl.VIEW.LEFT)
            image_pair["left"] = image.get_data().copy()
            camera.retrieve_image(image, sl.VIEW.RIGHT)
            image_pair["right"] = image.get_data().copy()

    @staticmethod
    def get_single_pcd(cam_id, camera, id_to_pcd, condition=None):
        """Capture a single pointcloud from a zed camera. Modifies id_to_pcd[cam_id]
           to store the captured image. Captured pcd is stored as numpy array
        
        Args:
            cam_id: int, camera id
            camera: zed camera object
            id_to_image: dict where the captured pcd is stored
            condition: threading.Condition object, used to synchronize camera capture time
        """
        if condition is not None:
            with condition:
                condition.wait()
        pcd = sl.Mat()
        runtime_parameters = sl.RuntimeParameters()
        if camera.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            camera.retrieve_measure(pcd, sl.MEASURE.XYZRGBA,sl.MEM.CPU)
            id_to_pcd[cam_id] = pcd.get_data().copy()

    @staticmethod
    def init_zed_cameras():
        """Returns a dictionary of camera id to zed camera objects.
        e.g:
        {
            0: zed_camera_object_0,
            1: zed_camera_object_1,
            ...
        }
        """
        id_to_cam = {}
        camera_list = sl.Camera.get_device_list()
        for i, camera in enumerate(camera_list):
            zed = sl.Camera()
            init_params = sl.InitParameters()
            init_params.coordinate_units = sl.UNIT.METER
            init_params.camera_resolution = sl.RESOLUTION.AUTO #HD1080
            init_params.depth_mode = sl.DEPTH_MODE.NEURAL #_PLUS
            init_params.camera_fps = 30
            init_params.set_from_camera_id(i)
            err = zed.open(init_params)
            if (err != sl.ERROR_CODE.SUCCESS):
                exit(-1)
            id_to_cam[i] = zed
        return id_to_cam

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Aargparse.")
    parser.add_argument('--rootdir', type=str, help='The path to save the data', default = "")
    parser.add_argument('--obj', type=str, help='The object to record', required=True)
    args = parser.parse_args()

    cameras = ZedCameraManager()

    images = cameras.capture_images()
    # pcds = {}
    # ZedCameraManager.get_single_pcd(0, cameras.id_to_cam[0], pcds, None)
    # print(pcds[0].shape)
    # points = pcds[0][:,:,:3].reshape(-1, 3)
    # colors = pcds[0][:,:,3]
    # colors = np.ravel(colors).view('uint8').reshape((720, 1280, 4))[:,:,:3]
    # plt.imshow(colors); plt.show()
    # colors = colors.reshape(-1,3)
    # points[np.isnan(points)] = 0
    # pcd = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(points))
    # pcd.colors = o3d.utility.Vector3dVector(colors / 255.0)
    # o3d.visualization.draw_geometries([pcd])

    # get left / right image pair
    rootdir = args.rootdir
    if rootdir[-1] != "/":
        rootdir = rootdir + "/"
    obj = args.obj

    image_pair = {}
    cameras.get_image_pair(0, cameras.id_to_cam[0], image_pair)

    array_left = image_pair["left"]
    corrected_array_left = array_left[:, :, [2, 1, 0]]
    
    plt.imshow(corrected_array_left)
    plt.title("RGB Image from NumPy Array")
    plt.axis('off')  # Turn off axis labels
    plt.show()
    np.save(rootdir + obj + "_left.npy", corrected_array_left)

    array_right = image_pair["right"]
    corrected_array_right = array_right[:, :, [2, 1, 0]]
    plt.imshow(corrected_array_right)
    plt.title("RGB Image from NumPy Array")
    plt.axis('off')  # Turn off axis labels
    plt.show()
    np.save(rootdir + obj + "_right.npy", corrected_array_right)