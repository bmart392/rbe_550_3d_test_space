# Import necessary packages
import string


class gridCell:

    # Initialize cell values
    def __init__(self) -> None:
        self.positionX = 0
        self.positionY = 0
        self.positionZ = 0
        self.isStartingPosition = False
        self.isGoalPosition = False
        self.isOccupiedByRobot = False
        self.isOccupiedByObstacle = False
        self.isVisitedBySearchAlgorithm = False
        self.isOnPath = False
        self.parentCell = ""
        self.distanceToStartPosition = 0
        self.isInQueue = False
        self.cannotBeObstacle = False

    # Set the position values of the cell
    def setPositions(self, positionX, positionY, positionZ):
        self.positionX = positionX
        self.positionY = positionY
        self.positionZ = positionZ
    
    # Add a parent cell to the cell
    def addParentCell(self, parent):
        self.parentCell = parent

    # Set the cell as on the path to the goal
    def markAsOnPath(self):
        self.isOnPath = True

    # Reset all of the non-obstacle related flags
    def resetNonObstacleFlags(self):
        self.isStartingPosition = False
        self.isGoalPosition = False
        self.isOccupiedByRobot = False
        self.isVisitedBySearchAlgorithm = False
        self.isOnPath = False
        self.parentCell = ""
        self.cannotBeObstacle = False

    # Check if the cell is available for visiting based on whether or not to include having previously been visited
    def isAvailableForVisiting(self, includingVisited):
        return not(self.isStartingPosition or self.isOccupiedByRobot or self.isOccupiedByObstacle or (not(includingVisited) and self.isVisitedBySearchAlgorithm))

    # Check if the cell is open
    def isCellOpen(self):
        return not(self.isOccupiedByObstacle or
                   self.isOccupiedByRobot or
                   self.isStartingPosition or
                   self.isGoalPosition)
        
    # Fill the cell with an obstacle
    def fillWithObstacle(self):
        self.isOccupiedByObstacle = True

    # Mark the cell as having been visited by a search algorithm
    def markAsVisited(self):
        self.isVisitedBySearchAlgorithm = True
    
    # Set the cell as the staritng point
    def setAsStart(self):
        self.isStartingPosition = True
    
    # Set the cell as the goal point
    def setAsGoal(self):
        self.isGoalPosition = True

    # Prevent obstacles from being placed in a cell
    def blockFromBeingObstacle(self):
        self.cannotBeObstacle = True

    # Create a stirng representation of the string
    def visualizeAsString(self):
        
        # Create status string
        if self.isOccupiedByObstacle:
            status = 1
        elif self.isOccupiedByRobot:
            status = 2
        else:
            status = 0

        # Parse the cell into a string including its position and status
        stringVersion = f'{self.positionX:03}, {self.positionY:03}, {status:01}'
        
        # Return the string
        return stringVersion

    # Override the comparison operator for the cell compare the distance to the start position field
    def __lt__(self, other):
        return self.distanceToStartPosition < other.distanceToStartPosition
