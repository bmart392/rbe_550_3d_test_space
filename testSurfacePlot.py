import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
fig.set_size_inches(6.0, 6.0)
cube_color = 'green'
cube_transparency = 1.0
cords = [[0, 0, 0], [0, 0, 1], [5, 5, 5], [10, 10, 10]]
cube_size = 1.0

X = np.array([[[]]])
Y = np.array([[[]]])
Z = np.array([[[]]])

first_time_through_flag = True

for each in cords:
    coordinate_x = each[0]
    coordinate_y = each[1]
    coordinate_z = each[2]

    for offset in [0, cube_size]:

        # Make surfaces parallel to XY Plane.
        # Include differentiation between first time through and further runs.
        if first_time_through_flag:
            X = np.array([[[coordinate_x, coordinate_x], [coordinate_x + cube_size, coordinate_x + cube_size]]])
            Y = np.array([[[coordinate_y, coordinate_y + cube_size], [coordinate_y, coordinate_y + cube_size]]])
            Z = np.array([[[coordinate_z + offset, coordinate_z + offset],
                           [coordinate_z + offset, coordinate_z + offset]]])
            first_time_through_flag = False
        else:
            X = np.append(X,
                          np.array(
                              [[[coordinate_x, coordinate_x], [coordinate_x + cube_size, coordinate_x + cube_size]]]),
                          0)
            Y = np.append(Y,
                          np.array(
                              [[[coordinate_y, coordinate_y + cube_size], [coordinate_y, coordinate_y + cube_size]]]),
                          0)
            Z = np.append(Z,
                          np.array([[[coordinate_z + offset, coordinate_z + offset],
                                     [coordinate_z + offset, coordinate_z + offset]]]), 0)

        # Make surface parallel to YZ Plane.
        X = np.append(X,
                      np.array([[[coordinate_x + offset, coordinate_x + offset],
                                 [coordinate_x + offset, coordinate_x + offset]]]), 0)
        Y = np.append(Y,
                      np.array([[[coordinate_y, coordinate_y], [coordinate_y + cube_size, coordinate_y + cube_size]]]),
                      0)
        Z = np.append(Z,
                      np.array([[[coordinate_z, coordinate_z + cube_size], [coordinate_z, coordinate_z + cube_size]]]),
                      0)

        # Make surfaces parallel to XZ Plane.
        X = np.append(X,
                      np.array([[[coordinate_x, coordinate_x + cube_size], [coordinate_x, coordinate_x + cube_size]]]),
                      0)
        Y = np.append(Y,
                      np.array([[[coordinate_y + offset, coordinate_y + offset],
                                 [coordinate_y + offset, coordinate_y + offset]]]), 0)
        Z = np.append(Z,
                      np.array([[[coordinate_z, coordinate_z], [coordinate_z + cube_size, coordinate_z + cube_size]]]),
                      0)

# Plot each surface.
for index in range(X.shape[0]):
    surf = ax.plot_surface(X[index], Y[index], Z[index], color=cube_color,
                           alpha=cube_transparency, linewidth=0, antialiased=False)

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

plt.show()
