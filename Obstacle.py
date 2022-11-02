# Import necessary packages
import numpy as np
from random import random
from gridCell import gridCell


class Obstacle:
    def __init__(self, shape_type=None, input_block_size=None) -> None:

        if shape_type is None:
            # Generate a random number to determine the shape of the cell
            self.shapeType = random()
        else:
            self.shapeType = shape_type

        if input_block_size is None:
            default_obstacle_size = 5
            block_size = np.ones((default_obstacle_size, default_obstacle_size))
        else:
            block_size = np.ones((input_block_size, input_block_size))

        # Set the shape of the obstacle
        if self.shapeType < 0.2:
            template_shape = [[False], [True], [True], [True]]
            self.shapeType = 0
        elif self.shapeType < 0.4:
            template_shape = [[True, True], [True, True]]
            self.shapeType = 1
        elif self.shapeType < 0.6:
            template_shape = [[True, False], [True, True], [False, True]]
            self.shapeType = 2
        elif self.shapeType < 0.8:
            template_shape = [[True, False], [True, False], [True, False], [True, True]]
            self.shapeType = 3
        else:
            template_shape = [[False, True], [False, True], [False, True], [True, True]]
            self.shapeType = 4

        # Scale the size of the obstacle up by the block_size
        self.obstacle_shape = np.kron(template_shape, block_size)

        # Convert all values in the obstacle shape to boolean
        for y_index in range(len(self.obstacle_shape)):
            for x_index in range(len(self.obstacle_shape[y_index])):
                if self.obstacle_shape[y_index][x_index] == 1:
                    self.obstacle_shape[y_index][x_index] = True
                else:
                    self.obstacle_shape[y_index][x_index] = False

        # Generate a random number to define the orientation of the obstacle
        rotation_about_z_axis = random()

        # Set change the orientation of the obstacle based on the orientation
        if 0.50 > rotation_about_z_axis >= 0.25:
            self.obstacle_shape = np.rot90(self.obstacle_shape)
        elif rotation_about_z_axis < 0.75:
            self.obstacle_shape = np.rot90(self.obstacle_shape, 2)
        elif rotation_about_z_axis <= 1.00:
            self.obstacle_shape = np.rot90(self.obstacle_shape, 3)

        # Get the size of the obstacle in each direction
        obstacle_size = self.obstacle_shape.shape

        # Initialize the number of cells filled with an obstacle
        self.number_of_obstacle_cells = 0

        # Store the individual sizes of the obstacle in the x and y direction
        self.x_size = obstacle_size[1]
        self.y_size = obstacle_size[0]
        self.z_size = 1
        
        # Iterate through each cell in the obstacle
        for x_index in range(self.x_size):
            for y_index in range(self.y_size):
                
                # Make a new cell object
                new_grid_cell = gridCell()

                # Set the position of the cell
                new_grid_cell.setPositions(x_index, y_index, 1)
                
                # If the position in the obstacle is filled with an obstacle
                if self.obstacle_shape[y_index][x_index]:
                    
                    # Set the status of the cell
                    new_grid_cell.fillWithObstacle()
                    
                    # Increase the count
                    self.number_of_obstacle_cells = self.number_of_obstacle_cells + 1
                
                # Replace the value in the obstacle array with the newly created grid cell
                self.obstacle_shape[y_index][x_index] = new_grid_cell


if __name__ == "__main__":

    # Test creating a random obstacle
    new_obstacle = Obstacle(shape_type=.1)
