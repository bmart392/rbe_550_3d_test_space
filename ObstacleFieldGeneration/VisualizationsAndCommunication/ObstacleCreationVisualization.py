from matplotlib import pyplot
from ObstacleFieldGeneration.ObstacleField import ObstacleField
from ObstacleFieldGeneration.PrimitiveClasses.ObstactleFieldConstants import UNIT_OBSTACLE_SIZE
from ObstacleFieldGeneration.PrimitiveClasses.Obstacle import Obstacle
from ObstacleFieldGeneration.PrimitiveClasses.PrimitiveZone import PrimitiveZone
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


class ObstacleCreationVisualization:

    def __init__(self, obstacle_field: ObstacleField):
        self.obstacle_field = obstacle_field
        # Set up the figure
        self.visualization_container = pyplot.figure()
        self.visualization_plot = self.visualization_container.add_subplot(projection='3d')
        self.visualization_container.set_size_inches(6.0, 6.0)
        self.visualization_plot.set_xbound(lower=self.obstacle_field.field_bounds[0][0],
                                           upper=self.obstacle_field.field_bounds[0][1])
        self.visualization_plot.set_ybound(lower=self.obstacle_field.field_bounds[1][0],
                                           upper=self.obstacle_field.field_bounds[1][1])
        self.visualization_plot.set_zbound(lower=self.obstacle_field.field_bounds[2][0],
                                           upper=self.obstacle_field.field_bounds[2][1])
        self.visualization_plot.grid(which='both')
        self.visualization_plot.grid(which='major', alpha=0.5)
        self.visualization_plot.grid(which='minor', alpha=0.2)

        # Show the figure when debugging the code
        # pyplot.show()

    # Update the visualization of the obstacle grid at the specified cells
    def update_grid_visualization(self):

        # For each cell in the obstacle field
        for obstacle in self.obstacle_field.get_obstacles_in_field():
            obstacle: Obstacle  # Object type hint
            for primitive in obstacle.get_obstacle_primitives():
                primitive: PrimitiveZone  # Object type hint

                # Draw a cube to represent the cell
                self.plot_surface_cube(self.visualization_plot,
                                       'black',
                                       'black',
                                       1.0,
                                       primitive.get_origin(),
                                       UNIT_OBSTACLE_SIZE)

    @staticmethod
    def plot_surface_cube(ax, cube_color, cube_edge_color, cube_transparency, cube_coordinates, cube_size):

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

    # Save the visualization of the obstacle field to an image file
    @staticmethod
    def save_grid_visualization(image_name):
        pyplot.savefig(image_name)
