from tkinter import *
from tkinter import filedialog
import os
import open3d as o3d
import numpy as np
import cv2

class Open:
    def __init__(self, initial_path):
        if initial_path == "":
            self.absolute_path = str(os.path.dirname(__file__))
        else:
            self.absolute_path = initial_path
        #building GUI
        self.root = Tk()
        self.root.withdraw()

    def get_file_name(self):
        try:
            # Abre a janela de seleção de arquivos
            file_name = filedialog.askopenfilename(initialdir=self.absolute_path,
                                                   title="Select a file", 
                                                   filetypes=(("PLY File", "*.ply"),
                                                              ("OBJ File", "*.obj"),
                                                              ("JPG File", "*.jpg"),
                                                              ("JPEG File", "*.jpeg"),
                                                              ("PNG File", "*.png"),
                                                              ("All files", "*.*"),))
            
        except Exception as e:
            print(f"Erro ao abrir o arquivo: {e}")
            file_name = "error"
        
        return file_name
    
    def get_3D_file(self, name_3d_file):
        if name_3d_file == "error":
            return "error"
        else:
            #get a 3D cloud in numpy array
            pcd = o3d.io.read_point_cloud(name_3d_file)
            return np.asarray(pcd.points)

    def get_image(self, name_image):
        if name_image == "error":
            return "error"
        else:
            #get a image in numpy array
            imgBGRA = cv2.imread(name_image, cv2.IMREAD_UNCHANGED)
            imgRGBA = cv2.cvtColor(imgBGRA, cv2.COLOR_BGRA2RGBA)
            return imgRGBA