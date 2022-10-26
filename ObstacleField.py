# Import necessary packages
from os import makedirs, path
import numpy as np
from gridCell import gridCell
from obstacle import obstacle
import random
from matplotlib import pyplot, patches
from mpl_toolkits.mplot3d import Axes3D
from plotSurfaceCube import plotSurfaceCube
"""
from breadthFirstSearch import breadthFirstSearch
from depthFirstSearch import depthFirstSearch
from djikstrasSearch import djikstrasSearch
from randomSearch import randomSearch
"""


# Define a class for working with the obstacle field
class ObstacleField:

    # Constructor for the class
    def __init__(self, size_x, size_y, size_z, fill_percentage, log_file_name) -> None:

        # Define visualization variables
        self.visualizationPlot = None
        self.visualizationContainer = None

        # Define location and name of logging file
        self.logFileLocation = log_file_name + "/" + log_file_name + '_DebugLog.txt'
        
        # Set size of obstacle field
        self.sizeX = size_x
        self.sizeY = size_y
        self.sizeZ = size_z
        self.theoreticalFillPercentage = fill_percentage
        self.actualFillPercentage = 0

        # Define array for storing number of each type of obstacles located in the field
        self.obstacleTypes = [0, 0, 0, 0, 0]

        # Define array to store the grid in
        self.mapGrid = np.array([])

        # Set flag
        first_plane_added_to_grid = True

        # Iterate over size of the desired field in the z-axis
        for z in range(self.sizeZ):

            # Define an array in which to store the cells placed in the current z plane
            plane_array = np.array([])

            # Set flag
            first_row_added_to_plane = True

            # Iterate over size of the desired field in the y-axis
            for y in range(self.sizeY):

                # Define an array in which to store the cells placed in the current row
                row_array = np.array([])

                # Iterate over the size of the desired field in the x-axis
                for x in range(self.sizeX):

                    # Instantiate new cell to place in the obstacle field
                    new_empty_cell = gridCell()
                    new_empty_cell.setPositions(x, y, z)

                    # Add a new empty cell to the current row
                    row_array = np.append([row_array], [new_empty_cell])

                """
                # If this is the first row inserted into the obstacle field
                if firstTimeThroughRow:
    
                    # Set the map as the row array
                    self.mapGrid = rowArray
    
                    # Reset flags accordingly
                    firstTimeThroughRow = False
                    secondTimeThroughRow = True
                
                # If this is the second row inserted into the obstacle field
                elif secondTimeThroughRow:
    
                    # Append the current row to the existing obstacle field
                    self.mapGrid = np.append([self.mapGrid], [rowArray], axis=0)
    
                    # Reset flags accordingly
                    secondTimeThroughRow = False
                
                # Else append the current row into the map
                else:
                """
                # Add new row of empty cells to current plane
                if first_row_added_to_plane:
                    plane_array = np.array([row_array])
                    first_row_added_to_plane = False
                else:
                    plane_array = np.append(plane_array, [row_array], axis=0)

            # Add new plane of empty cells to mapGrid
            if first_plane_added_to_grid:
                self.mapGrid = np.array([plane_array])
                first_plane_added_to_grid = False
            else:
                self.mapGrid = np.append(self.mapGrid, [plane_array], axis=0)

        # Calculate the number of cells needed to fill based on desired percentage
        number_of_cells_to_fill = (self.sizeX * self.sizeY * self.sizeZ)*self.theoreticalFillPercentage
        
        # Set counter for number of cells filled so far
        number_of_cells_filled_currently = 0

        # Declare variable to track how many times a new object has been re-generated 
        new_obstacle_loop_counter = 0

        # Declare obstacle loop limit
        max_obstacle_loop_index = 10

        # Declare coordinate loop limit
        max_coordinate_loop_index = 25

        # While the desired number of filled cells is less than the goal number
        while number_of_cells_filled_currently < number_of_cells_to_fill and new_obstacle_loop_counter < max_obstacle_loop_index:

            # Generate a new obstacle
            new_obstacle = obstacle()

            # Increment the count for the type of obstacle created to ensure even distribution of obstacles
            self.obstacleTypes[new_obstacle.shapeType] = self.obstacleTypes[new_obstacle.shapeType] + 1

            # Calculate the bounds of all possible locations that the obstacle could be placed
            valid_field_bounds_x = self.sizeX - new_obstacle.xSize
            valid_field_bounds_y = self.sizeY - new_obstacle.ySize
            valid_field_bounds_z = self.sizeZ - new_obstacle.zSize

            # Flag that a valid origin for the new obstacle have not been found
            coordinates_are_valid = False

            # Declare a variable to track how many times a new coordinate has been generated for the exisiting obstacle
            new_coordinate_loop_counter = 0

            # While the coordinates of the origin have not found
            while not coordinates_are_valid:

                # Generate new obstacle origin 
                new_obstacle_coordinates = self.generate_random_coordinates(valid_field_bounds_x, valid_field_bounds_y, valid_field_bounds_z)

                # Check that the possible origin of the new obstacle is open
                coordinates_are_valid = self.mapGrid[int(new_obstacle_coordinates[2]),
                                                     int(new_obstacle_coordinates[0]),
                                                     int(new_obstacle_coordinates[1])].isCellOpen()

                # If the coordinate is valid
                if coordinates_are_valid:

                    # Declare an array in which to store the coordinates of each cell of the obstacle
                    set_of_obstacle_coordinates = np.array([])
                    
                    # Create flags for controlling iteration over the obstacle
                    first_time_through = True
                    second_time_through = False

                    # Iterate over each cell in the obstacle
                    for x in range(new_obstacle.xSize):
                        for y in range(new_obstacle.ySize):

                            # Calculate the location of the proposed cell in the obstacle field based on its
                            # location in the obstacle
                            x_location = new_obstacle_coordinates[0] + x
                            y_location = new_obstacle_coordinates[1] + y

                            # Check that if the specified location in the field is open
                            coordinates_are_valid = self.mapGrid[int(new_obstacle_coordinates[2]), int(y_location),
                                                                 int(x_location)].isCellOpen()

                            # Proceed only if the coordinates are valid
                            if coordinates_are_valid:
                                
                                # If this is the first set of coordinates added into the list
                                if first_time_through:
                                    
                                    # Set the list of coordinates equal to the current coordinates
                                    set_of_obstacle_coordinates = [x_location, y_location, new_obstacle_coordinates[2]]

                                    # Reset flags accordingly
                                    first_time_through = False
                                    second_time_through = True
                                
                                # If this is the second set of coordinates added into the list
                                elif second_time_through:

                                    # Append the new coordinates on to the existing one as a new row
                                    set_of_obstacle_coordinates = np.append([set_of_obstacle_coordinates],
                                                                            [[x_location,
                                                                              y_location,
                                                                              new_obstacle_coordinates[2]]], axis=0)

                                    # Reset flags accordingly
                                    second_time_through = False

                                # Else append the new coordinates on to the existing list of coordinates
                                else:
                                    set_of_obstacle_coordinates = np.append(set_of_obstacle_coordinates,
                                                                            [[x_location,
                                                                              y_location,
                                                                              new_obstacle_coordinates[2]]], axis=0)

                            # If the coordinate is not valid, exit the iterative loop in the y axis
                            else:
                                break

                        # If the coordinate is not valid, exit the iterative loop in the x axis
                        if not coordinates_are_valid:
                            break
                
                # Increment the number of times generating a new coordinate by one
                new_coordinate_loop_counter = new_coordinate_loop_counter + 1

                # If the coordinates are not valid and the loop counter has been exceeded, break out of the loop
                if not coordinates_are_valid and new_coordinate_loop_counter > max_coordinate_loop_index:
                    break
            
            # If all coordinates in the obstacle are valid
            if coordinates_are_valid:

                # Record the origin of the new obstacle to be inserted
                origin = set_of_obstacle_coordinates[0]
                
                # For each coordinate pair in the obstacle
                for coordinatePair in set_of_obstacle_coordinates:

                    # Find the corresponding value of the coordinate in reference to the obstacle origin
                    obstacle_coordinate_x = int(coordinatePair[0] - origin[0])
                    obstacle_coordinate_y = int(coordinatePair[1] - origin[1])
                    obstacle_coordinate_z = int(coordinatePair[2] - origin[2])
                    
                    # If the specified cell is occupied by an obstacle
                    if new_obstacle.obstacleShape[obstacle_coordinate_y,
                                                  obstacle_coordinate_x]:

                        # Set the corresponding cell in the obstacle field as occupied by an obstacle
                        corresponding_cell_in_field = self.mapGrid[int(coordinatePair[2]),
                                                                   int(coordinatePair[1]),
                                                                   int(coordinatePair[0])]
                        corresponding_cell_in_field.fillWithObstacle()

                        # Increment the number of cells filled with obstacles
                        number_of_cells_filled_currently = number_of_cells_filled_currently + 1
                
                # Reset the new obstacle loop counter indicating an obstacle had been successfully inserted
                new_obstacle_loop_counter = 0
            
            # Increment the number of times an object could not be inserted successfully
            else:
                new_obstacle_loop_counter = new_obstacle_loop_counter + 1

        # Calculate the percentage of cells successfully filled with obstacles
        self.actualFillPercentage = number_of_cells_filled_currently/(self.sizeX * self.sizeY * self.sizeZ)
        
    """# Create a string representation for the obstacle grid
    def visualizeGridAsText(self):

        # Define an array to hold the string representation of each row
        rowStrings = []

        # For each row of the obstacle field
        for y3 in range(2*self.sizeY):
            
            # If it is an even row, create a string for each cell
            if y3%2 == 0 :
                y3 = int(y3/2)

                # Add a character to create a bounding box
                currentRowString = "|"

                # Create a string for each cell
                for x3 in range(self.sizeX):
                    cellToVisualize = self.mapGrid[y3][x3]
                    currentRowString = currentRowString + " " + cellToVisualize.visualizeAsString() + " |"
                
                # Measure the width of each row to ensure consistency
                rowWidth = len(currentRowString)
            else:

                # Add extra rows of dashes to to make the result easier to read
                rowStrings = np.append(rowStrings, "-"*rowWidth)

            # Add the row to the array
            rowStrings = np.append(rowStrings, currentRowString)

        # Return the array  
        return rowStrings
"""
    # Create a visualization of the obstacle grid     
    def initialize_grid_visualization(self):
        
        # Set up the figure
        self.visualizationContainer = pyplot.figure()
        self.visualizationPlot = self.visualizationContainer.add_subplot(projection='3d')
        self.visualizationContainer.set_size_inches(6.0, 6.0)
        self.visualizationPlot.set_xticks(range(self.sizeX), minor=True)
        self.visualizationPlot.set_yticks(range(self.sizeY), minor=True)
        self.visualizationPlot.set_zticks(range(self.sizeZ), minor=True)
        self.visualizationPlot.set_xbound(lower=0, upper=self.sizeX)
        self.visualizationPlot.set_ybound(lower=0, upper=self.sizeY)
        self.visualizationPlot.set_zbound(lower=0, upper=self.sizeZ)
        self.visualizationPlot.grid(which='both')
        self.visualizationPlot.grid(which='major', alpha=0.5)
        self.visualizationPlot.grid(which='minor', alpha=0.2)

        # For each cell in the obstacle field
        for plane in self.mapGrid:
            for row in plane:
                for cell in row:

                    plot_cell = True

                    # Assign it a color based on the status of the cell
                    if cell.isStartingPosition:
                        cell_color = 'green'
                        cell_transparency = 1.0
                    elif cell.isGoalPosition:
                        cell_color = 'red'
                        cell_transparency = 1.0
                    elif cell.isOnPath:
                        cell_color = 'blue'
                        cell_transparency = 0.75
                    elif cell.isVisitedBySearchAlgorithm:
                        cell_color = 'orange'
                        cell_transparency = 0.5
                    elif cell.isOccupiedByRobot:
                        cell_color = 'purple'
                        cell_transparency = 1.0
                    elif cell.isOccupiedByObstacle:
                        cell_color = 'black'
                        cell_transparency = 1.0
                    else:
                        cell_color = 'white'
                        cell_transparency = 0.0
                        plot_cell = False

                    if cell_color == 'black':
                        cell_edge_color = 'white'
                    else:
                        cell_edge_color = cell_color

                    if plot_cell:
                        # Draw a cube to represent the cell
                        plotSurfaceCube(self.visualizationPlot,
                                        cell_color,
                                        cell_edge_color,
                                        cell_transparency,
                                        [cell.positionX, cell.positionY, cell.positionZ],
                                        1.0)
        
        # Show the figure when debugging the code
        # pyplot.show()

    # Save the visualization of the obstacle field to an image file
    @staticmethod
    def save_grid_visualization(image_name):
        pyplot.savefig(image_name)

    # Update the visualization of the obstacle grid at the specified cells
    def update_grid_visualization(self, changed_cells):
        
        # If only one cell is given, create an array for iteration
        if isinstance(changed_cells, gridCell):
            changed_cells = [changed_cells]

        # For each given cell, update the map    
        for cell in changed_cells:

            plot_cell = True

            # Assign it a color based on the status of the cell
            if cell.isStartingPosition:
                cell_color = 'green'
                cell_transparency = 1.0
            elif cell.isGoalPosition:
                cell_color = 'red'
                cell_transparency = 1.0
            elif cell.isOnPath:
                cell_color = 'blue'
                cell_transparency = 0.75
            elif cell.isVisitedBySearchAlgorithm:
                cell_color = 'orange'
                cell_transparency = 0.5
            elif cell.isOccupiedByRobot:
                cell_color = 'purple'
                cell_transparency = 1.0
            elif cell.isOccupiedByObstacle:
                cell_color = 'black'
                cell_transparency = 1.0
            else:
                cell_color = 'white'
                cell_transparency = 0.0
                plot_cell = False

            if cell_color == 'black':
                cell_edge_color = 'white'
            else:
                cell_edge_color = cell_color

            if plot_cell:
                # Draw a cube to represent the cell
                plotSurfaceCube(self.visualizationPlot,
                                cell_color,
                                cell_edge_color,
                                cell_transparency,
                                [cell.positionX, cell.positionY, cell.positionZ],
                                1.0)
        
        # Show the figure for debugging
        # pyplot.show()

    # Log messages in an external text file for debugging purposes    
    def log_messages_in_a_log_file(self, messages):
        with open(self.logFileLocation, 'a') as logFile:
            
            # If there is only one message, create an array for iteration
            if isinstance(messages, str):
                messages = [messages]

            # Append each message to the existing text in the file
            for message in messages:
                logFile.write(message)
                logFile.write('\n')

    # Generate a random coordinate within the obstacle field
    @staticmethod
    def generate_random_coordinates(x_limit, y_limit, z_limit):
        return [round(random.random() * x_limit, 0),
                round(random.random() * y_limit, 0),
                round(random.random() * z_limit, 0)]

    # Generate a random coordinate within the obstacle field that is open
    def generate_random_open_coordinate(self):
        
        # Set a flag for the validity of the coordinates
        coordinates_are_valid = False

        # Set default coordinates for result
        possible_coordinates = [0, 0, 0]

        # While valid coordinates have not been found, generate new coordinates
        while not coordinates_are_valid:
            
            # Generate a new coordinate
            possible_coordinates = self.generate_random_coordinates(self.sizeX - 1, self.sizeY - 1, self.sizeZ - 1)

            # Check that the coordinate is open
            coordinate_being_investigated = self.mapGrid[int(possible_coordinates[2]),
                                                         int(possible_coordinates[1]),
                                                         int(possible_coordinates[0])]
            coordinates_are_valid = coordinate_being_investigated.isCellOpen()
        
        # Return the x, y, and z position of the coordinate
        return [int(possible_coordinates[0]), int(possible_coordinates[1]), int(possible_coordinates[2])]

    # Find the neighboring cells to any given cell with the option to include or exclude cells that have already been
    # visited by a search algorithm
    def get_reachable_cells(self, single_cell, including_visited):
        
        # Define an array to store the neighboring cells
        reachable_cells = []

        # Iterate through the three planes around the starting point
        for z in [-1, 0, 1]:

            # Get the absolute z coordinate of the plane
            z_location = single_cell.positionZ + z

            # Check that the z location is within the grid
            if not (z_location >= self.sizeZ or z_location < 0):

                # Iterate through the three rows around the starting point
                for y in [-1, 0, 1]:

                    # Get the absolute y coordinate of the row
                    y_location = single_cell.positionY + y

                    # Check that the y location is within the plane
                    if not (y_location >= self.sizeY or y_location < 0):

                        # Iterate through the three columns around the starting point
                        for x in [1, 0, -1]:

                            # Skip the starting point
                            if not (y == 0 and x == 0 and z == 0):

                                # Get the absolute x coordinate of the column
                                x_location = single_cell.positionX + x

                                # Check that the x location is within the row
                                if not (x_location >= self.sizeX or x_location < 0):

                                    # Get the cell object at the given x, y, and z position
                                    next_neighboring_cell = self.mapGrid[z_location][y_location][x_location]

                                    # If the next neighboring cell is available to visit, add it to the list
                                    if next_neighboring_cell.isAvailableForVisiting(including_visited):
                                        if len(reachable_cells) == 0:
                                            reachable_cells = [next_neighboring_cell]
                                        else:
                                            reachable_cells.append(next_neighboring_cell)

        # Return the list of reachable cells
        return reachable_cells
    
    # Reset the all data in the grid excluding data about obstacles
    def reset_grid_to_obstacles(self):
        
        # For each cell in the grid, clear all flags
        for row in self.mapGrid:
            for cell in row:
                if not cell.isOccupiedByObstacle:
                    cell.resetNonObstacleFlags()

    # Write array of obstacle locations to a text file
    def write_obstacles_to_text_file(self, filename):
        with open(filename, 'w') as obstacle_file:
            for plane in self.mapGrid:
                for row in plane:
                    for cell in row:
                        if cell.isOccupiedByObstacle:
                            x_position = str(cell.positionX)
                            y_position = str(cell.positionY)
                            z_position = str(-cell.positionZ)
                            position_string = x_position + "," + y_position + ...
                            "," + z_position
                            obstacle_file.write(position_string + "\n")

# Define file behaviour when ran as main
if __name__ == '__main__':

    # Identify the path to store log file and visualizations
    folderName = "test_3"
    folderPath = folderName + "/"

    # If the path does not exist, make it
    if not path.exists(folderName):
        makedirs(folderName)
    
    # For each obstacle density, run each search algorithm
    for density in [1]:

        # Generate a new obstacle field
        newObstacleField = ObstacleField(50, 50, 50, density / 100, folderName)
        newObstacleField.log_messages_in_a_log_file("Field Generated at " + str(density) + "%.")
        newObstacleField.write_obstacles_to_text_file()
        """ # Show the obstacle field
        newObstacleField.initialize_grid_visualization()
        newObstacleField.log_messages_in_a_log_file("Visualization Complete.")

        # Save a visualization of the result
        newObstacleField.save_grid_visualization(folderPath + 'emptyWorld_' + str(density) + 'percent.png')
        newObstacleField.log_messages_in_a_log_file("Visualization Saved.")"""
        
        """
        # Generate the start and finish points for the search algorithms
        startPoint = newObstacleField.generate_random_open_coordinate()
        goalPoint = newObstacleField.generate_random_open_coordinate()
        newObstacleField.log_messages_in_a_log_file("Goal points determined.")

        # Implement a depth first search algorithm over the field
        depthSearch = depthFirstSearch(startPoint, goalPoint)
        depthSearch.executeSearch(newObstacleField)
        newObstacleField.log_messages_in_a_log_file("Depth Search Complete.")
        newObstacleField.log_messages_in_a_log_file("Cells visited: " + str(depthSearch.numberOfCellsVisited))
        newObstacleField.log_messages_in_a_log_file("Number of Iterations: " + str(depthSearch.numberOfiterations))
        newObstacleField.log_messages_in_a_log_file("Length of path: " + str(len(depthSearch.pathToObstacle)))

        # Save a visualization of the result
        newObstacleField.save_grid_visualization(folderPath + 'depthFirstSearch_' + str(density) + 'percent_' + 
            str(len(depthSearch.pathToObstacle)) + 'unitPath.png')
        newObstacleField.log_messages_in_a_log_file("Visualization Saved.")

        # Reset the world for the next search algorithm
        newObstacleField.reset_grid_to_obstacles()
        newObstacleField.log_messages_in_a_log_file("Obstacle Field Reset.")

        # Show the obstacle field
        newObstacleField.initialize_grid_visualization()
        newObstacleField.log_messages_in_a_log_file("Visualization Complete.")

        # Implement a depth first search algorithm over the field
        #print(newObstacleField.breadthFirstSearch(startPoint, goalPoint))
        breadthSearch = breadthFirstSearch(startPoint, goalPoint)
        breadthSearch.executeSearch(newObstacleField)
        newObstacleField.log_messages_in_a_log_file("Breadth Search Complete.")
        newObstacleField.log_messages_in_a_log_file("Cells visited: " + str(breadthSearch.numberOfCellsVisited))
        newObstacleField.log_messages_in_a_log_file("Number of Iterations: " + str(breadthSearch.numberOfiterations))
        newObstacleField.log_messages_in_a_log_file("Length of path: " + str(len(breadthSearch.pathToObstacle)))

        # Save a visualization of the result
        newObstacleField.save_grid_visualization(folderPath + 'breadthFirstSearch_' + str(density) + 'percent_' + 
            str(len(breadthSearch.pathToObstacle)) + 'unitPath.png')
        newObstacleField.log_messages_in_a_log_file("Visualization Saved.")

        # Reset the world for the next search algorithm
        newObstacleField.reset_grid_to_obstacles()
        newObstacleField.log_messages_in_a_log_file("Obstacle Field Reset.")

        # Show the obstacle field
        newObstacleField.initialize_grid_visualization()
        newObstacleField.log_messages_in_a_log_file("Visualization Complete.")

        # Implement a depth first search algorithm over the field
        #print(newObstacleField.breadthFirstSearch(startPoint, goalPoint))
        djikstras = djikstrasSearch(startPoint, goalPoint)
        djikstras.executeSearch(newObstacleField)
        newObstacleField.log_messages_in_a_log_file("Djikstras Search Complete.")
        newObstacleField.log_messages_in_a_log_file("Djikstras visited: " + str(djikstras.numberOfCellsVisited))
        newObstacleField.log_messages_in_a_log_file("Number of Iterations: " + str(djikstras.numberOfiterations))
        newObstacleField.log_messages_in_a_log_file("Length of path: " + str(len(djikstras.pathToObstacle)))

        # Save a visualization of the result
        newObstacleField.save_grid_visualization(folderPath + 'djikstraSearch_' + str(density) + 'percent_' + 
            str(len(djikstras.pathToObstacle)) + 'unitPath.png')
        newObstacleField.log_messages_in_a_log_file("Visualization Saved.")

        # Reset the world for the next search algorithm
        newObstacleField.reset_grid_to_obstacles()
        newObstacleField.log_messages_in_a_log_file("Obstacle Field Reset.")

        # Show the obstacle field
        newObstacleField.initialize_grid_visualization()
        newObstacleField.log_messages_in_a_log_file("Visualization Complete.")

        # Implement a random search algorithm over the field
        #print(newObstacleField.breadthFirstSearch(startPoint, goalPoint))
        searchRandom = randomSearch(startPoint, goalPoint)
        searchRandom.executeSearch(newObstacleField)
        newObstacleField.log_messages_in_a_log_file("Random Search Complete.")
        newObstacleField.log_messages_in_a_log_file("Random visited: " + str(searchRandom.numberOfCellsVisited))
        newObstacleField.log_messages_in_a_log_file("Number of Iterations: " + str(searchRandom.numberOfiterations))
        newObstacleField.log_messages_in_a_log_file("Length of path: " + str(len(searchRandom.pathToObstacle)))

        # Save a visualization of the result
        newObstacleField.save_grid_visualization(folderPath + 'randomSearch_' + str(density) + 'percent_' + 
            str(len(searchRandom.pathToObstacle)) + 'unitPath.png')
        newObstacleField.log_messages_in_a_log_file("Visualization Saved.")"""
