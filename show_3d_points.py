import open3d as o3d
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt

class Show3DPoints():
    def __init__(self):
        pass

    def show(self, points_numpy, x_list, y_list, z_list):
        #--------------WITH LINES--------------
        if x_list is not None:
            # Pegando o array de pontos
            self.points = points_numpy.copy()
            points_z_cte = self.points
            # points_z_cte[:, 2] = 1

            # Criar a nuvem de pontos
            nuvem_de_pontos = o3d.geometry.PointCloud()
            nuvem_de_pontos.points = o3d.utility.Vector3dVector(points_z_cte)

            # Normalizar os valores de Z para o intervalo [0, 1]
            z_values = self.points[:, 2]
            z_min, z_max = np.min(z_values), np.max(z_values)
            z_norm = (z_values - z_min) / (z_max - z_min)

            # Aplicar um mapa de cores
            colormap = cm.get_cmap("plasma")  # "jet" vai de azul para vermelho | magma de roxo para amarelo
            colors = colormap(z_norm)[:, :3]  # Pega apenas as 3 primeiras componentes (RGB)

            # Definir as cores na nuvem de pontos
            nuvem_de_pontos.colors = o3d.utility.Vector3dVector(colors)

            # Criar um quadro de coordenadas para referência
            coordinate_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=5, origin=[0, 0, 0])

            # ---------- ADICIONANDO AS LINHAS ----------
            #X axis
            line_x_set = o3d.geometry.LineSet()
            line_x_set.points = o3d.utility.Vector3dVector(x_list)
            #pairs
            lines_x = np.array([[i, i+1] for i in range(0, len(x_list)-1, 2)])
            line_x_set.lines = o3d.utility.Vector2iVector(lines_x)
            line_x_set.paint_uniform_color([1, 0, 0])

            #Y axis
            line_y_set = o3d.geometry.LineSet()
            line_y_set.points = o3d.utility.Vector3dVector(y_list)
            #pairs
            lines_y = np.array([[i, i+1] for i in range(0, len(y_list)-1, 2)])
            line_y_set.lines = o3d.utility.Vector2iVector(lines_y)
            line_y_set.paint_uniform_color([0, 1, 0])

            #Z axis
            line_z_set = o3d.geometry.LineSet()
            line_z_set.points = o3d.utility.Vector3dVector(z_list)
            #pairs
            lines_z = np.array([[i, i+1] for i in range(0, len(z_list)-1, 2)])
            line_z_set.lines = o3d.utility.Vector2iVector(lines_z)
            line_z_set.paint_uniform_color([0, 0, 1])

            # Exibir a nuvem de pontos
            o3d.visualization.draw_geometries([nuvem_de_pontos, coordinate_frame, line_x_set, line_y_set, line_z_set], width=800, height=600)

        #--------------WITHOUT LINES--------------
        else:
            # Pegando o array de pontos
            self.points = points_numpy

            # Criar a nuvem de pontos
            nuvem_de_pontos = o3d.geometry.PointCloud()
            nuvem_de_pontos.points = o3d.utility.Vector3dVector(self.points)

            # Normalizar os valores de Z para o intervalo [0, 1]
            z_values = self.points[:, 2]
            z_min, z_max = np.min(z_values), np.max(z_values)
            z_norm = (z_values - z_min) / (z_max - z_min)

            # Aplicar um mapa de cores
            colormap = cm.get_cmap("magma")  # "jet" vai de azul para vermelho | magma de roxo para amarelo
            colors = colormap(z_norm)[:, :3]  # Pega apenas as 3 primeiras componentes (RGB)

            # Definir as cores na nuvem de pontos
            nuvem_de_pontos.colors = o3d.utility.Vector3dVector(colors)

            # Criar um quadro de coordenadas para referência
            coordinate_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=5, origin=[0, 0, 0])

            # Exibir a nuvem de pontos
            o3d.visualization.draw_geometries([nuvem_de_pontos, coordinate_frame], width=800, height=600)

class ShowImage():
    def __init__(self):
        pass

    def show(self, image_numpy):
        # Exibir a imagem com Matplotlib
        plt.imshow(image_numpy)
        plt.axis("off")  # Remove os eixos para uma exibição mais limpa
        plt.show()