#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
from matplotlib.patches import Rectangle


class World:

	def __init__(self, name, size, map_image=None):
		self.name = name
		self.xx = size[0]
		self.yy = size[1]
		if len(size) == 3:
			self.zz = size[2]
		else:
			self.zz = None

		self.occupancy_grid = None
		if map_image is not None:
			self.import_obstacle_map(map_image)

		print(f'Initialized world with name {self.name}, size [{self.xx},{self.yy},{self.zz}], and generated obstacles')

	def import_obstacle_map(self, map_image):
		image = Image.open(map_image)
		image = image.resize((self.xx, self.yy))  # resize to map size
		thresh = 200
		fn = lambda x: 255 if x > thresh else 0
		out = image.convert('L').point(fn, mode='1')
		out = np.flip(out, 0)

		res = ~np.asarray(out)

		if self.zz is not None:
			res = np.repeat(res[:, :, np.newaxis], self.zz, axis=2)

		self.occupancy_grid = res

	def is_occupied(self, cell):
		# checks if cell is occupied by obstacle
		if len(cell) == 3:
			return self.occupancy_grid[cell[1]][cell[0]][cell[2]]
		else:
			return self.occupancy_grid[cell[1]][cell[0]]

	def is_valid_cell(self, cell):
		# checks cell validity based on occupied and visited conditions and returns. Also checks if it is in range of the map
		if len(cell) == 3:
			if not ((0 <= cell[0] < self.xx) and (0 <= cell[1] < self.yy) and (0 <= cell[2] < self.zz)):
				return False
		else:
			if not ((0 <= cell[0] < self.xx) and (0 <= cell[1] < self.yy)):
				return False

		if self.is_occupied(cell):
			return False

		return True

	def grid_cell_to_index(self, cell):
		return cell[1] * self.xx + cell[0]

	@staticmethod
	def axis_equal_3d(axis):
		extents = np.array([getattr(axis, 'get_{}lim'.format(dim))() for dim in 'xyz'])
		sz = extents[:, 1] - extents[:, 0]
		centers = np.mean(extents, axis=1)
		maxsize = max(abs(sz))
		r = maxsize / 2
		for ctr, dim in zip(centers, 'xyz'):
			getattr(axis, 'set_{}lim'.format(dim))(ctr - r, ctr + r)

	def plot_occupancy_grid(self, axis):
		# plots occupancy grid on map

		if self.zz is not None:  # 3d
			axis.set(xlim=(0, self.xx), ylim=(0, self.yy), zlim=(0, self.zz))  # forces axis limits
			self.axis_equal_3d(axis)

			occ_to_plot = np.transpose(self.occupancy_grid, axes=(1, 0, 2))
			axis.voxels(occ_to_plot, edgecolor='k')  # plot a voxel in the cell
			plt.xlabel('x')
			plt.ylabel('y')
		else:  # 2d
			axis.set_aspect('equal', 'box')
			axis.set(xlim=(0, self.xx), ylim=(0, self.yy))  # forces axis limits

			for y in range(0, self.xx):
				for x in range(0, self.yy):
					if self.is_occupied([x, y]):  # if cell is occupied
						axis.add_patch(Rectangle((x, y), 1, 1, color='black'))  # plot a rectangle in the cell

	@staticmethod
	def plot_cell(axis, cell, marker_color, marker_width):
		if len(cell.position) == 3:
			axis.scatter(cell.position[0] + 0.5, cell.position[1] + 0.5, cell.position[2] + 0.5, marker='x', c=marker_color, linewidths=marker_width),
		else:
			plt.plot(cell.position[0] + 0.5, cell.position[1] + 0.5, 'x' + marker_color, markeredgewidth=marker_width)

	@staticmethod
	def plot_path(axis, path):
		if path is not None:
			for i in range(0, len(path) - 1):
				x_vals = [path[i][0] + 0.5, path[i + 1][0] + 0.5]  # x start and end centered in cell
				y_vals = [path[i][1] + 0.5, path[i + 1][1] + 0.5]  # y start and end centered in cell

				if len(path[0]) == 3:
					z_vals = [path[i][2] + 0.5, path[i + 1][2] + 0.5]  # y start and end centered in cell
					axis.plot(x_vals, y_vals, z_vals, 'r-', markersize=5)
				else:
					plt.plot(x_vals, y_vals, 'r-', markersize=5)


class Robot:

	def __init__(self, name, diameter):
		self.name = name
		self.diameter = diameter
		self.pose = None

	@staticmethod
	def motion_options(cell):
		ops = [-1, 0, 1] # potential motions
		poss_ops = []
		if len(cell) == 3: # 3D
			for i in ops: # x
				for j in ops: # y
					for k in ops: # z
						poss_ops.append((cell[0] + i, cell[1] + j, cell[2] + k))
			if cell in poss_ops:
				poss_ops.remove(cell)
		elif len(cell) == 2: # 2D
			for i in ops: # x
				for j in ops: # y
					poss_ops.append((cell[0] + i, cell[1] + j))
			if cell in poss_ops:
				poss_ops.remove(cell) # remove cell if it is all zeros
		else:
			print('warn: bad cell length')
		return poss_ops


if __name__ == '__main__':
	world = World('Earth', [50, 50, 10], 'room_map.png')
	robot = Robot('Sphere', 1)

	fig = plt.figure()
	ax = plt.axes(projection='3d')
	world.plot_occupancy_grid(ax)
	plt.show()
