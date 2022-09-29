import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


def plotSurfaceCube(ax, cube_color, cube_edge_color, cube_transparency, cube_coordinates, cube_size):

    first_time_through_flag = True

    x = np.array([[[]]])
    y = np.array([[[]]])
    z = np.array([[[]]])

    coordinate_x = cube_coordinates[0]
    coordinate_y = cube_coordinates[1]
    coordinate_z = cube_coordinates[2]

    for offset in [0, cube_size]:

        # Make surfaces parallel to XY Plane.
        # Include differentiation between first time through and further runs.
        if first_time_through_flag:
            x = np.array([[[coordinate_x, coordinate_x], [coordinate_x + cube_size, coordinate_x + cube_size]]])
            y = np.array([[[coordinate_y, coordinate_y + cube_size], [coordinate_y, coordinate_y + cube_size]]])
            z = np.array([[[coordinate_z + offset, coordinate_z + offset],
                           [coordinate_z + offset, coordinate_z + offset]]])
            first_time_through_flag = False
        else:
            x = np.append(x,
                          np.array(
                              [[[coordinate_x, coordinate_x],
                                [coordinate_x + cube_size, coordinate_x + cube_size]]]),
                          0)
            y = np.append(y,
                          np.array(
                              [[[coordinate_y, coordinate_y + cube_size],
                                [coordinate_y, coordinate_y + cube_size]]]),
                          0)
            z = np.append(z,
                          np.array([[[coordinate_z + offset, coordinate_z + offset],
                                     [coordinate_z + offset, coordinate_z + offset]]]), 0)

        # Make surface parallel to YZ Plane.
        x = np.append(x,
                      np.array([[[coordinate_x + offset, coordinate_x + offset],
                                 [coordinate_x + offset, coordinate_x + offset]]]), 0)
        y = np.append(y,
                      np.array(
                          [[[coordinate_y, coordinate_y], [coordinate_y + cube_size, coordinate_y + cube_size]]]),
                      0)
        z = np.append(z,
                      np.array(
                          [[[coordinate_z, coordinate_z + cube_size], [coordinate_z, coordinate_z + cube_size]]]),
                      0)

        # Make surfaces parallel to XZ Plane.
        x = np.append(x,
                      np.array(
                          [[[coordinate_x, coordinate_x + cube_size], [coordinate_x, coordinate_x + cube_size]]]),
                      0)
        y = np.append(y,
                      np.array([[[coordinate_y + offset, coordinate_y + offset],
                                 [coordinate_y + offset, coordinate_y + offset]]]), 0)
        z = np.append(z,
                      np.array(
                          [[[coordinate_z, coordinate_z], [coordinate_z + cube_size, coordinate_z + cube_size]]]),
                      0)

    # Plot each surface.
    for index in range(x.shape[0]):
        ax.plot_surface(x[index], y[index], z[index], rstride=1, cstride=1, color=cube_color,
                        alpha=cube_transparency, linewidth=0.1, edgecolor=cube_edge_color, antialiased=False)
