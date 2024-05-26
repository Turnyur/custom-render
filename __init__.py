
import numpy as np
import trimesh
import pyrender
import cv2
import scipy.io
import trimesh.scene
import os


os.environ['PYOPENGL_PLATFORM'] = 'egl'

object_category_list = []



def make_camera_pose(azimuth_deg:float, elevation_deg:float):
    azimuth_rad = np.radians(azimuth_deg)
    elevation_rad = np.radians(elevation_deg)

    rotation_azimuth = np.array([[np.cos(azimuth_rad), 0, np.sin(azimuth_rad), 0],
                                [0, 1, 0, 0],
                                [-np.sin(azimuth_rad), 0, np.cos(azimuth_rad), 0],
                                [0, 0, 0, 1]])

    rotation_elevation = np.array([[1, 0, 0, 0],
                                    [0, np.cos(elevation_rad), -np.sin(elevation_rad), 0],
                                    [0, np.sin(elevation_rad), np.cos(elevation_rad), 0],
                                    [0, 0, 0, 1]])

    
    proj_rotation_matrix = np.dot(rotation_azimuth, rotation_elevation)
    pose =np.eye(4)
    pose[2, 3] = 1.0 
    camera_pose = np.dot(proj_rotation_matrix, pose)
    
    return camera_pose



def get_3d_obj(file_path:str)-> trimesh.Scene:
    #print("FILE_PATH: "+file_path)
    loadedMesh = trimesh.load(file_path)


   
    if isinstance(loadedMesh, trimesh.Trimesh):
        trimeshScene = trimesh.Scene()
        trimeshScene.add_geometry(loadedMesh)
    else:
        trimeshScene = loadedMesh
    scene = pyrender.Scene.from_trimesh_scene(trimeshScene)



    scene= pyrender.Scene.from_trimesh_scene(loadedMesh)
    return scene


    
def save_camera_matrix(camera_matrix, suffix, output_path):
    #projection_matrix = camera.get_projection_matrix()
    projection_matrix = camera_matrix

    #index_str = str(object_category_list.index(file_dir))
    output_filename = "camera_" + str(suffix) + ".mat"
    output_path = os.path.join(output_path, output_filename)

    projection_data = {"camera_" + str(suffix) : projection_matrix}
    scipy.io.savemat(output_path, projection_data)



def render_scene(scene, suffix, output_path):
    
    renderer = pyrender.OffscreenRenderer(viewport_width=500, viewport_height=400)
    color_image, depth_image = renderer.render(scene)

    #index_str = str(object_category_list.index(dir_path))
    output_filename = "render_" + str(suffix) + ".png"
    output_path_r = os.path.join(output_path, output_filename)
    cv2.imwrite(output_path_r, cv2.cvtColor(color_image, cv2.COLOR_RGB2BGR))

    # Normalize the depth image
    depth_image_normalized = (depth_image - np.min(depth_image)) / (np.max(depth_image) - np.min(depth_image)) * 255
    depth_image_normalized = depth_image_normalized.astype(np.uint8)

    output_filename = "depth_" + str(suffix )+ ".png"
    output_path_d = os.path.join(output_path, output_filename)
    cv2.imwrite(output_path_d, depth_image_normalized)

    renderer.delete()



def data_loader(obj_category_path) -> list:
    files_and_directories = os.listdir(obj_category_path) 
    directories = [d for d in files_and_directories if os.path.isdir(os.path.join(obj_category_path, d))]
    for directory in directories:
        object_category_list.append(directory)