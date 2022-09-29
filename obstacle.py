# Import necessary packages
import numpy as np
from random import random
from gridCell import gridCell

class obstacle:
    def __init__(self) -> None:
        
        # Generate a random number to determine the shape of the cell
        self.shapeType = random()

        # Set the shape of the obstacle
        if self.shapeType < 0.2:
            self.obstacleShape = np.array([[True], [True], [True], [True]])
            self.shapeType = 0
        elif self.shapeType < 0.4:
            self.obstacleShape = np.array([[True, True], [True, True]])
            self.shapeType = 1
        elif self.shapeType < 0.6:
            self.obstacleShape = np.array([[True, False], [True, True], [False, True]])
            self.shapeType = 2
        elif self.shapeType < 0.8:
            self.obstacleShape = np.array([[True, False], [True, False], [True, False], [True, True]])
            self.shapeType = 3
        elif self.shapeType <= 1.0:
            self.obstacleShape = np.array([[False, True], [False, True], [False, True], [True, True]])
            self.shapeType = 4

        # Generate a random number to define the orientation of the obstacle
        rotationAboutZaxis = random()

        # Set change the orientation of the obstacle based on the orientation
        if 0.50 > rotationAboutZaxis >= 0.25:
            self.obstacleShape = np.rot90(self.obstacleShape)
        elif rotationAboutZaxis < 0.75:
            self.obstacleShape = np.rot90(self.obstacleShape, 2)
        elif rotationAboutZaxis <= 1.00:
            self.obstacleShape = np.rot90(self.obstacleShape, 3)

        # Get the size of the obstacle in each direction
        obstacleSize = self.obstacleShape.shape

        # Initialize the number of cells filled with an obstacle
        self.numberOfObstacleCells = 0

        # Store the individual sizes of the obstacle in the x and y direction
        self.xSize = obstacleSize[1]
        self.ySize = obstacleSize[0]
        self.zSize = 1
        
        # Iterate through each cell in the obstacle
        for x in range(self.xSize):
            for y in range(self.ySize):
                
                # Make a new cell object
                newGridCell = gridCell()

                # Set the position of the cell
                newGridCell.setPositions(x,y,1)
                
                # If the position in the obstacle is filled with an obstacle
                if self.obstacleShape[y][x]:
                    
                    # Set the status of the cell
                    newGridCell.fillWithObstacle()
                    
                    # Increase the count
                    self.numberOfObstacleCells = self.numberOfObstacleCells + 1
                
                # Replace the value in the obstacle array with the newly created grid cell
                self.obstacleShape[y][x] = newGridCell
