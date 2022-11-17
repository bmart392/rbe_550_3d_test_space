from ObstacleField import ObstacleField
from VisualizationsAndCommunication.ObstacleCreationVisualization import ObstacleCreationVisualization
from VisualizationsAndCommunication.CommunicationFunctions import *
from os import path, makedirs

# Identify the path to store log file, visualizations, and obstacle locations.
basic_file_name = "test_11-16-2022"
log_file_name = basic_file_name + ".txt"
log_file_folder_name = "TestData/" + basic_file_name
log_file_path = log_file_folder_name + "/" + log_file_name
obstacle_locations_file_location = "../gazebo_interface/object_locations.csv"
visualization_name = log_file_folder_name + "/" + basic_file_name + ".png"


# If the path does not exist, make it
if not path.exists(log_file_folder_name):
    makedirs(log_file_folder_name)

# Log creation of log file.
log_messages_in_a_log_file(log_file_path,
                           "Log file and filepath created.")

# Generate a new obstacle field
new_obstacle_field = ObstacleField([[0, 200], [0, 300], [-75, 0]], .05, obstacle_free_points=[[0, 0, 0], [50, 50, -25]])

# Log successful creation of obstacle field
log_messages_in_a_log_file(log_file_path,
                           "Field Generated at " +
                           str(new_obstacle_field.get_actual_fill_density() * 100) + "% density.")

# Write the obstacles in the obstacle field to a csv file
write_obstacles_to_text_file(obstacle_locations_file_location, new_obstacle_field.generate_header_info(),
                             new_obstacle_field.get_origins_of_all_obstacle_primitives())

# Log successful creation of csv file.
log_messages_in_a_log_file(log_file_path,
                           "Obstacle locations generated in csv file in: " + obstacle_locations_file_location)
# Show the obstacle field
visualization = ObstacleCreationVisualization(new_obstacle_field)
visualization.update_grid_visualization()
visualization.save_grid_visualization(visualization_name)

# Log successful creation of visualization.
log_messages_in_a_log_file(log_file_path,
                           "Visualization saved at: " + visualization_name)

# Log end of program success.
log_messages_in_a_log_file(log_file_path, "File execution complete.")
