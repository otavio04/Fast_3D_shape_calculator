import open3d as o3d
import os
import numpy as np
import pandas as pd

class Save():
    def __init__(self):
        pass

    def save_ply(self, points):
        #Putting points
        lineset = o3d.geometry.PointCloud()
        lineset.points = o3d.utility.Vector3dVector(points)

        #Path
        absolute_path = str(os.path.dirname(__file__))
        path = os.path.join(absolute_path, "PLY_files")
        if not os.path.exists(path) and not os.path.isdir(path):
            os.mkdir(path)
        name_file = path + "/processed_particles.ply"
        #Saving
        o3d.io.write_point_cloud(name_file, lineset)

    def save_lenghts(self, array_lenght):
        #Path
        absolute_path = str(os.path.dirname(__file__))
        path = os.path.join(absolute_path, "CSV_files")
        if not os.path.exists(path) and not os.path.isdir(path):
            os.mkdir(path)
        name_file = path + "/processed_particles.csv"

        #Dataframe
        data_freme = {
            "X Axis": array_lenght[:, 0],
            "Y Axis": array_lenght[:, 1],
            "Z Axis": array_lenght[:, 2]
        }
        df = pd.DataFrame(data_freme)

        #Save
        df.to_csv(name_file, sep=';', decimal=",", index=False)