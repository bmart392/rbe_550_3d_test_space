from os import makedirs, path

import numpy as np

from ObstacleField import ObstacleField
from Environment import World, Robot
from AStar import AStar
import matplotlib.pyplot as plt

if __name__ == '__main__':

	# Identify the path to store log file and visualizations
	folderName = "test_3d"
	folderPath = folderName + "/"

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
	# pull values from mapGrid
	for grid1 in newObstacleField.mapGrid:
		for grid2 in grid1:
			for grid3 in grid2:
				world_grid[grid3.positionX][grid3.positionY][grid3.positionZ] = not grid3.isCellOpen()

	# initiate world with mapGrid data
	world = World('Earth',map_size)
	world.occupancy_grid = world_grid

	robot = Robot('Sphere',1)

	start_p = (1, 1, 0)
	end_p = (40, 30, 45)

	fig = plt.figure()
	ax = plt.axes(projection='3d')
	ax.view_init(elev=90.0, azim=-90.0)
	world.plot_occupancy_grid(fig, ax)

	plan = AStar(world, robot)
	path = plan.plan(start_p, end_p)
	print(path)
	world.plot_path(ax, path)

	plt.show()
