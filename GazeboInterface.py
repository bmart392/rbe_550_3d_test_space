import sys


def generate_path_yaml(path, filename):
	file = open(filename, 'w')
	sys.stdout = file

	print('inertial_frame_id: world')
	print('waypoints:')

	for node in path:
		print('  -')
		print(f'    point: [{node[0]}, {node[1]}, {node[2]}]')
		print('    max_forward_speed: 1.6')
		print('    heading: 0')
		print('    use_fixed_heading: False')


if __name__ == '__main__':
	test_file = 'test.yaml'
	test_path = [(0,0,0), (1,2,3), (10,10,10), (0,0,0)]
	generate_path_yaml(test_path, test_file)