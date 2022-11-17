import numpy as np


# TODO - add drift compensation, look into basic point checks to, include Z depth
def basic_grid_search(initial_position, search_area_size, search_direction, target_size, sensor_view_width):
    # search_area_size = (x, y)
    row_spacing = (1 * sensor_view_width) + 0.5 * target_size
    distance_to_edge_of_search_area = row_spacing / 2

    row_width_bounds = [distance_to_edge_of_search_area - search_area_size[0]/2,
                        search_area_size[0]/2 - distance_to_edge_of_search_area]

    row_height_bound = search_area_size[1] - distance_to_edge_of_search_area

    current_row_height = 0
    creating_first_row = True
    basic_path_waypoints = []
    while current_row_height < row_height_bound:
        if current_row_height%(2*row_spacing) == 0:
            alternating_row_width_bounds = row_width_bounds
        else:
            alternating_row_width_bounds = [row_width_bounds[1], row_width_bounds[0]]
        for row_width_bound in alternating_row_width_bounds:
            if creating_first_row:
                new_waypoint = (0, current_row_height)
                creating_first_row = False
            else:

                new_waypoint = (row_width_bound, current_row_height)
            basic_path_waypoints.append(new_waypoint)
        current_row_height = current_row_height + row_spacing
    search_direction_in_radians = np.radians(search_direction)
    cos_search_heading = np.cos(search_direction_in_radians)
    sin_search_heading = np.sin(search_direction_in_radians)
    transformation_matrix = np.array([[cos_search_heading, -sin_search_heading, initial_position[0]],
                                      [sin_search_heading, cos_search_heading, initial_position[1]],
                                      [0, 0, 1]])
    actual_path_waypoints = []
    for waypoint in basic_path_waypoints:
        temp_waypoint_matrix = np.array([[waypoint[0]],
                                         [waypoint[1]],
                                         [1]])
        transformed_waypoint = transformation_matrix@temp_waypoint_matrix
        flattened_transformed_waypoint = np.array([transformed_waypoint[0], transformed_waypoint[1]]).flatten()
        tolist_transformed_waypoint = flattened_transformed_waypoint.tolist()
        rearranged_transformed_waypoint = [round(value, 4) for value in tolist_transformed_waypoint]
        actual_path_waypoints.append(rearranged_transformed_waypoint)
    return actual_path_waypoints


if __name__ == "__main__":
    print(basic_grid_search((0, 0), (20, 20), 0, 0, 1))
