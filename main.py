from os import makedirs, path

import numpy as np

from ObstacleField import ObstacleField
from Environment import World, Robot
from AStar import AStar
import matplotlib.pyplot as plt
import GazeboInterface

# Identify the path to store log file and visualizations
folderName = "test_3d"
folderPath = folderName + "/"

# Filename for gazebo interface
gazebo_pathgen_file = 'gazebo_interface/path_waypoints.yaml'

# If the path does not exist, make it
if not path.exists(folderName):
	makedirs(folderName)

density = 2.5
map_size = [50, 50, 50]

# Generate a new obstacle field
newObstacleField = ObstacleField(map_size[0], map_size[1], map_size[2], density / 100, folderName)
newObstacleField.log_messages_in_a_log_file("Field Generated at " + str(density) + "%.")

# TODO: update temporary workaround and move into planner environment
# start empty grid
world_grid = np.empty((map_size[0], map_size[1], map_size[2]))
# pull values from mapGrid generation
for grid1 in newObstacleField.mapGrid:
	for grid2 in grid1:
		for node in grid2:
			world_grid[node.positionX][node.positionY][node.positionZ] = not node.isCellOpen()

# initiate world with mapGrid data
world = World('Earth',map_size)
world.occupancy_grid = world_grid

robot = Robot('Sphere',1)

start_p = (1, 1, 0)
end_p = (40, 30, 45)

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.view_init(elev=90.0, azim=-90.0)
world.plot_occupancy_grid(ax)

plan = AStar(world, robot)
path = plan.plan(start_p, end_p)
print(path)
world.plot_path(ax, path)

GazeboInterface.generate_path_yaml(path, gazebo_pathgen_file)

plt.show()
