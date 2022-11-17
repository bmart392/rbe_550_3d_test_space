# Import necessary packages
import numpy as np
from random import random
from ObstacleFieldGeneration.PrimitiveClasses.ObstactleFieldConstants import *
from ObstacleFieldGeneration.PrimitiveClasses.PrimitiveZone import PrimitiveZone
from math import floor


class Obstacle:
    def __init__(self, shape_type=None, input_block_size=None) -> None:

        self.origin = [0, 0, 0]

        if shape_type is None:
            # Generate a random number between 1 and 10 to determine the shape of the cell
            self.shape_type = floor(random() * NUMBER_OF_OBSTACLE_SHAPES)
            if self.shape_type == NUMBER_OF_OBSTACLE_SHAPES:
                self.shape_type = SQUARE_SHAPE
        else:
            self.shape_type = shape_type

        # TODO Create 3D obstacle shapes
        # Set the shape of the obstacle
        if self.shape_type == LINE_SHAPE:
            obstacle_shape = [[True], [True], [True], [True]]
        elif self.shape_type == SQUARE_SHAPE:
            obstacle_shape = [[True, True], [True, True]]
        elif self.shape_type == Z_SHAPE:
            obstacle_shape = [[True, False], [True, True], [False, True]]
        elif self.shape_type == L_SHAPE:
            obstacle_shape = [[True, False], [True, False], [True, False], [True, True]]
        elif self.shape_type == INV_L_SHAPE:
            obstacle_shape = [[False, True], [False, True], [False, True], [True, True]]
        else:
            self.shape_type = SINGLE_UNIT_SHAPE
            obstacle_shape = [[True]]

        # Generate a random number to define the orientation of the obstacle
        rotation_about_z_axis = random()

        # TODO add rotation into 3D
        # Set change the orientation of the obstacle based on the orientation
        if 0.50 > rotation_about_z_axis >= 0.25:
            obstacle_shape = np.rot90(obstacle_shape)
        elif rotation_about_z_axis < 0.75:
            obstacle_shape = np.rot90(obstacle_shape, 2)
        elif rotation_about_z_axis <= 1.00:
            obstacle_shape = np.rot90(obstacle_shape, 3)

        # Get the size of the obstacle in each direction
        # NOTE: this should be changed if 3D obstacles are implemented
        obstacle_size = (obstacle_shape.shape[0], obstacle_shape.shape[1], 1)

        # Store the individual sizes of the obstacle in the x and y direction
        self.size_in_primitives = [obstacle_size[1], obstacle_size[0], obstacle_size[2]]

        # Create an array to store the primitive zones that make up the obstacle
        self.obstacle_primitive_zones = []

        # Iterate through each cell in the obstacle
        for x_index in range(self.size_in_primitives[0]):
            for y_index in range(self.size_in_primitives[1]):
                for z_index in range(self.size_in_primitives[2]):

                    if obstacle_shape[y_index][x_index]:
                        scaled_x = x_index * UNIT_OBSTACLE_SIZE
                        scaled_y = y_index * UNIT_OBSTACLE_SIZE
                        scaled_z = z_index * UNIT_OBSTACLE_SIZE

                        # Make a new cell object
                        new_primitive_zones = PrimitiveZone()

                        # Set the position of the cell
                        new_primitive_zones.set_origin([scaled_x, scaled_y, scaled_z])
                        self.obstacle_primitive_zones.append(new_primitive_zones)

        self.obstacle_bounds = self.generate_obstacle_bounds()

    def generate_obstacle_bounds(self, point=None):
        if point is None:
            point = self.origin

        temp_result = []
        for dimension, size in zip(point, self.size_in_primitives):
            temp_result.append([dimension, dimension + size * UNIT_OBSTACLE_SIZE])
        return temp_result

    def set_obstacle_origin(self, new_origin):
        self.origin = new_origin
        for obstacle_primitive_zone in self.obstacle_primitive_zones:
            obstacle_primitive_zone.offset_origin(new_origin)
        self.obstacle_bounds = self.generate_obstacle_bounds()

    def get_obstacle_origin(self):
        return self.origin

    def is_point_in_obstacle(self, point):
        for zone in self.obstacle_primitive_zones:
            if zone.is_point_within_zone(point):
                return True
        return False

    def get_obstacle_shape_type(self):
        return self.shape_type

    def get_obstacle_bounds(self):
        return self.obstacle_bounds

    def get_all_obstacle_points(self):
        list_of_all_points = []
        for primitive in self.obstacle_primitive_zones:
            for each in primitive.get_vertices():
                if each not in list_of_all_points:
                    list_of_all_points.append(each)
        return list_of_all_points

    def get_obstacle_primitives(self):
        return self.obstacle_primitive_zones

    def get_number_of_obstacle_primitives(self):
        return len(self.obstacle_primitive_zones)


if __name__ == "__main__":

    # Test creating a random obstacle
    new_obstacle = Obstacle()

    print("Done")
