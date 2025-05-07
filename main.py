from tkinter import *
from tkinter import font
import numpy as np

from open_file import Open
from show_3d_points import Show3DPoints, ShowImage
from three_d_processing import Processing
from save import Save

class Gui():
    #--------------INITIALIZATION--------------
    def __init__(self):
        #GUI configuration----------------------------
        self.root = Tk()
        self.root.title("Fast Shape 3D")
        self.root.resizable(False, False)

        #GUI widgets parameters----------------------------
        #Main
        font_main = font.Font(family = "Montserrat", size = 14, weight = "bold")
        h_main = 2
        w_main = 15
        #Show
        font_show = font.Font(family = "Montserrat", size = 12)
        h_show = 1
        w_show = 20

        #GUI widgets----------------------------
        #Main
        self.bt_load3d = Button(self.root, text="Load 3D file", width = w_main, height = h_main, font = font_main, command = lambda: self.load3d())
        self.bt_loadimg = Button(self.root, text="Load Image file", width = w_main, height = h_main, font = font_main, command = lambda: self.loadimg())
        self.bt_process = Button(self.root, text="Process", width = w_main, height = h_main, font = font_main, command = lambda: self.process3d())
        self.bt_reset = Button(self.root, text="Reset", width = w_main, height = h_main, font = font_main)
        #Show
        self.bt_show3d = Button(self.root, text="Show CLOUD OF POINT", width = w_show, height = h_show, font = font_show, command = lambda: self.show3d())
        self.bt_showimg = Button(self.root, text="Show IMAGE", width = w_show, height = h_show, font = font_show, command = lambda: self.showimg())


        #GUI widgets position----------------------------
        self.bt_load3d.grid(row=0, column=0, padx=5, pady=10)
        self.bt_loadimg.grid(row=0, column=1, padx=5, pady=10)
        self.bt_process.grid(row=0, column=2, padx=5, pady=10)
        self.bt_reset.grid(row=0, column=3, padx=5, pady=10)
        #Show
        self.bt_show3d.grid(row=1, column=0, padx=5, pady=10)
        self.bt_showimg.grid(row=1, column=1, padx=5, pady=10)


        #Running GUI----------------------------
        self.root.mainloop()
    
    #--------------LOAD 3D FILE--------------
    def load3d(self):
        initial_path = "C:/programas_python/fast_3D_shape_analysis/sample/3D"
        file_opener = Open(initial_path)
        file_name = file_opener.get_file_name()
        self.file3d = file_opener.get_3D_file(file_name)
    
    #--------------LOAD IMAGE FILE--------------
    def loadimg(self):
        initial_path = "C:/programas_python/form_3D/3D"
        file_opener = Open(initial_path)
        file_name = file_opener.get_file_name()
        self.fileimg = file_opener.get_image(file_name)

    #--------------SHOWING THE POINT CLOUD--------------
    def show3d(self):
        if len(self.file3d) > 0:
            display = Show3DPoints()
            display.show(self.file3d, 0, 0, 0)

    #--------------SHOWING THE IMAGE--------------
    def showimg(self):
        if len(self.fileimg) > 0:
            display = ShowImage()
            display.show(self.fileimg)

    def process3d(self):
        #Sending cloud of point
        processing = Processing(self.file3d.copy())
        #Cutting points
        points_cutted = processing.Cut(x_lim = 20, y_lim = 30, z_lim = 0)
        #Fitting plan and selecting inliers and outliers
        a_plan, b_plan, c_plan, d_plan, inliers_points, outliers_points = processing.fit_plane_ransac(points_cutted.copy())
        #Rotating cloud of point
        vector_of_plan = np.array([a_plan, b_plan, c_plan]) # Normal vector of plan fitted
        vector_of_alignment = np.array([0, 0, 1]) # Normal vector desired
        points_rotated, points_without_plan = processing.rotate_cloud_of_points(vector_of_plan.copy(), vector_of_alignment.copy(), points_cutted.copy())
        #clustering points of particles
        list_of_particles = processing.find_particles(points_rotated.copy()) # To np.array, needs np.vstack
        #Find the 3 axis of each particle
        list_of_axes, array_x_draw, array_y_draw, array_z_draw = processing.find_axis(list_of_particles.copy())
        #Saving data
        saving = Save()
        saving.save_ply(np.vstack(list_of_particles))
        saving.save_lenghts(list_of_axes)

        Show3DPoints().show(np.vstack(list_of_particles), array_x_draw, array_y_draw, array_z_draw)

#--------------RUN THE GUI CLASS AUTOMATICALLY--------------
if __name__ == '__main__':
    Gui()