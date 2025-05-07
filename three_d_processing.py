import numpy as np
from sklearn.linear_model import RANSACRegressor
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA

class Processing():
    def __init__(self, cloud_of_point):
        #get x, y and z coordinates
        self.points = cloud_of_point
        self.x_coordinate = cloud_of_point[:, 0]
        self.y_coordinate = cloud_of_point[:, 1]
        self.z_coordinate = cloud_of_point[:, 2]

    def Cut(self, x_lim, y_lim, z_lim):
        #cutting cloud of point space to delet outliers
        cutted_points = self.points[(self.y_coordinate > -y_lim) & (self.y_coordinate < y_lim)]
        x_new = cutted_points[:, 0]
        cutted_points = cutted_points[(x_new > -x_lim) & (x_new < x_lim)]
        z_new = cutted_points[:, 2]
        cutted_points = cutted_points[z_new > z_lim]

        return cutted_points
    
    def fit_plane_ransac(self, points_cutted):
        # Verifique se os pontos têm a forma correta (n_samples, 3)
        if points_cutted.shape[1] != 3:
            raise ValueError("The points must have 3 coordinates (x, y, z).")

        # Separete the coordinates x, y, z
        x_ransac = points_cutted[:, :2]  # Get the fist 2 columns (x e y)
        y_ransac = points_cutted[:, 2]   # Get the 3 column (z)

        # Fitting with RANSAC
        ransac = RANSACRegressor()
        ransac.fit(x_ransac, y_ransac)
        inlier_mask = ransac.inlier_mask_
        outlier_mask = np.logical_not(inlier_mask)

        # Coeficientes do plano estimados
        a, b = ransac.estimator_.coef_
        c = -1
        d = ransac.estimator_.intercept_

        # Pontos inliers
        inliers = points_cutted[inlier_mask]
        # Pontos outliers
        outliers = points_cutted[outlier_mask]

        return a, b, c, d, inliers, outliers
    
    def rotate_cloud_of_points(self, vec1, vec2, points):
        """
        Find the rotation matrix that aligns vec1 to vec2
        :param vec1: A 3d "source" vector
        :param vec2: A 3d "destination" vector
        :rotate_mat: A transform matrix (3x3) which when applied to vec1, aligns it with vec2
        :return points rotated to xy plan
        """
        a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
        v = np.cross(a, b)
        c = np.dot(a, b)
        s = np.linalg.norm(v)
        kmat = np.array([[ 0, -v[2],  v[1]],
                        [ v[2],  0, -v[0]],
                        [-v[1],  v[0],  0]])
        rotate_mat = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))

        rotated_points = points.dot(rotate_mat.T)
        z_flip_points = rotated_points.copy()
        z_flip_points[:, 2] = np.abs(z_flip_points[:, 2])

        points_without_plan = z_flip_points[z_flip_points[:, 2] > 1]

        return z_flip_points, points_without_plan
        
    def find_particles(self, group_particles):
        #get particles out the plan
        z_coord = group_particles[:, 2]
        cutted_plan = group_particles[z_coord > 1]
        #detecting clusters by DBSCAN
        dbscan = DBSCAN(eps=0.56, min_samples=5)    #adjust eps and min_samples as needed
        labels = dbscan.fit_predict(cutted_plan)

        #Ignoring outliers by labels
        unique_clusters = set(labels)
        if -1 in unique_clusters:
            unique_clusters.remove(-1)  # Remover outliers

        #storing particle points in a list
        list_of_particles = []
        for i in range(len(unique_clusters)):
            particle = cutted_plan[labels == i+1]
            num_points = len(particle)
            if num_points > 10:
                list_of_particles.append(particle)

        return list_of_particles

    def find_axis(self, list_of_particles):
        num_particles = len(list_of_particles)
        axis = []
        x_draw = []
        y_draw = []
        z_draw = []

        for i, particle in enumerate(list_of_particles):
            #finding Z axis of particle
            z_max = max(particle[:, 2]) - 1
            z_med = (max(particle[:, 2]) + 1)/2
            #finding X and Y axes of particles
            xy_points = particle[:, :2]
            #rotation matrix
            pca = PCA(n_components=2)
            pca.fit(xy_points)
            r = np.array(pca.components_)
            r = np.transpose(r)
            #rotating points
            rotation = np.dot(xy_points, r.copy())
            #translating points
            cx = np.average(rotation[:, 0])
            cy = np.average(rotation[:, 1])
            
            # rotation[:, 0] = rotation[:, 0] - cx
            # rotation[:, 1] = rotation[:, 1] - cy
            #Finding lenghts of the 3 axis
            x = rotation[:, 0]
            y = rotation[:, 1]
            
            x_lenght_max = np.amax(x) - np.amin(x)
            y_lenght_max = np.amax(y) - np.amin(y)
            axis.append(np.array([x_lenght_max, y_lenght_max, z_max]))

            #indexes of points to draw perpendicular lines
            x_index_max = np.argmax(x)
            x_index_min = np.argmin(x)
            y_index_max = np.argmax(y)
            y_index_min = np.argmin(y)
            z_index_max = np.argmax(particle[:, 2])
            #matrixes of lines rotated
            array_x_draw = np.array([   [rotation[x_index_min][0], cy],
                                        [rotation[x_index_max][0], cy]
                                    ])
            array_y_draw = np.array([   [cx, rotation[y_index_min][1]],
                                        [cx, rotation[y_index_max][1]]
                                    ])
            array_z_draw = np.array([   [cx, cy],
                                        [cx, cy]
                                    ])
            #matrixes of lines unrotated
            array_x_draw_rotated = np.dot(array_x_draw, r.copy().T)
            array_y_draw_rotated = np.dot(array_y_draw, r.copy().T)
            array_z_draw_rotated = np.dot(array_z_draw, r.copy().T)

            #points to draw perpendicular lines
            x_i = np.array([array_x_draw_rotated[0][0], array_x_draw_rotated[0][1], z_med])
            x_f = np.array([array_x_draw_rotated[1][0], array_x_draw_rotated[1][1], z_med])

            y_i = np.array([array_y_draw_rotated[0][0], array_y_draw_rotated[0][1], z_med])
            y_f = np.array([array_y_draw_rotated[1][0], array_y_draw_rotated[1][1], z_med])

            z_i = np.array([array_z_draw_rotated[0][0], array_z_draw_rotated[0][1], 1])
            z_f = np.array([array_z_draw_rotated[1][0], array_z_draw_rotated[1][1], particle[z_index_max][2]])

            x_draw.append(x_i)
            x_draw.append(x_f)
            y_draw.append(y_i)
            y_draw.append(y_f)
            z_draw.append(z_i)
            z_draw.append(z_f)
        
        return np.array(axis), np.array(x_draw), np.array(y_draw), np.array(z_draw)
            

    
    def c():
        pass