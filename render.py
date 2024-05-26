
import __init__ as c_render
import numpy as np
import pyrender
import os
import logging


#os.environ['PYOPENGL_PLATFORM'] = 'egl'



#Constants
shapenet_base_path  = "/home/turnyur/sommer-sem-2024/project/supersizing_3d/code/render/shapenet/"
output_dir = os.path.join(shapenet_base_path, '../render_output/shapenet_objects')


#dataloader_path  =  os.path.join(shapenet_base_path, '02691156')
#Log config
logging.basicConfig(filename=os.path.join(output_dir, 'error.log'), level=logging.ERROR)



#Shapenet categories/synseth path
shapenet_synsets = []
files_and_directories = os.listdir(shapenet_base_path) 
directories = [d for d in files_and_directories if os.path.isdir(os.path.join(shapenet_base_path, d))]
for directory in directories:
    shapenet_synsets.append(directory)
    #print(directory)




obj_path = 'models/model_normalized.obj'
for synset_id in shapenet_synsets: # Traverse all categories
   
   c_render.object_category_list = []

   obj_category_path = os.path.join(shapenet_base_path, str(synset_id))
   print("Rendering objects in SYNSET_ID:", str(synset_id))
   print("\tOUTPUT_PATH: ", str(output_dir))
   print("\n")

   #load Shapenet Data
   c_render.data_loader(obj_category_path)
   cat_list = []
   for i in range(len(c_render.object_category_list)):
      obj_category_path = os.path.join(synset_id, c_render.object_category_list[i])
      shapenet_obj = os.path.join(obj_category_path, obj_path)
      cat_list.append(shapenet_obj)




   #render and save image of objects in a given category
   obj_category_output_path = os.path.join(output_dir, synset_id)
   os.makedirs(obj_category_output_path, exist_ok=True)
   
   suffix_counter = 0
   for i in range(15): #render each object in a specific catgeory
   #for i in range(len(obj_category_path)): 
      try:
         shapenet_obj = os.path.join(shapenet_base_path, cat_list[i])
         

         for i in range(5): # Render each object from 4 different views

            scene = c_render.get_3d_obj(shapenet_obj)

            azimuth_deg = np.random.uniform(0, 360)
            elevation_deg = np.random.uniform(-75, 75)
            #azimuth_deg = 90
            #elevation_deg = 0

            camera_pose = c_render.make_camera_pose(azimuth_deg, elevation_deg)
            #print(camera_pose)
            #print()

            #render
  
            yfov_degrees = 60  
            yfov_radians = np.radians(yfov_degrees)
            aspect_ratio =1.0 # square
            camera = pyrender.PerspectiveCamera(yfov=yfov_radians, aspectRatio=aspect_ratio)

            scene.add(camera, pose= camera_pose)
            light = pyrender.PointLight(color=[1.0, 1.0, 1.0], intensity=5.0)
            scene.add(light)


            camera_intrinsics = camera.get_projection_matrix()
            
            #print("INTRINSICS", camera_intrinsics)
            #print("EXTRINSIC", camera_pose)

            #print("\n\n")

            camera_matrix = {
                  'K': camera_intrinsics,
                  'RT': camera_pose
               }

            c_render.render_scene(scene, suffix_counter, os.path.join(output_dir, str(synset_id)))
            c_render.save_camera_matrix(camera_matrix, suffix_counter, os.path.join(output_dir, str(synset_id)))
            
            suffix_counter+=1
         
      except Exception as e:
         error_msg = f"\n\tRendering failed for object:\n \tPATH: {os.path.join(output_dir, cat_list[i])} \n \tERROR: {e}"
         logging.error(error_msg)
         continue
      
      





