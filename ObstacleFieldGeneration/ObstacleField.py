# Import necessary packages
from ObstacleFieldGeneration.PrimitiveClasses.PrimitiveZone import PrimitiveZone
from ObstacleFieldGeneration.PrimitiveClasses.ObstactleFieldConstants import *
from ObstacleFieldGeneration.PrimitiveClasses.Obstacle import Obstacle
from random import random


# Define a class for working with the obstacle field
class ObstacleField:

    # Constructor for the class
    def __init__(self, field_bounds, fill_percentage, log_file_name=None,
                 obstacle_free_points=None) -> None:

        # Define visualization variables
        self.visualization_plot = None
        self.visualization_container = None

        # Define location and name of logging file
        if log_file_name is None:
            log_file_name = "test"
        self.log_file_location = log_file_name + "/" + log_file_name + '_DebugLog.txt'
        self.output_file_location = None
        
        # Set size of obstacle field
        self.field_bounds = field_bounds

        # Define variables to control how many obstacles will be created
        self.theoretical_fill_percentage = fill_percentage
        self.actual_fill_percentage = 0

        # Define array for storing number of each type of obstacles located in the field
        self.obstacle_types = [0, 0, 0, 0, 0]

        # Define an array to store zones that cannot have obstacles placed in them
        if obstacle_free_points is None:
            obstacle_free_points = []

        self.obstacle_free_zones = []

        # Create protected zones at any point given in the function
        for center_of_free_zone in obstacle_free_points:
            self.obstacle_free_zones.append(
                PrimitiveZone(origin=[center_of_free_zone[0] - (.5 * UNIT_PROTECTED_ZONE_SIZE),
                                      center_of_free_zone[1] - (.5 * UNIT_PROTECTED_ZONE_SIZE),
                                      center_of_free_zone[2] - (.5 * UNIT_PROTECTED_ZONE_SIZE)],
                              zone_type=PROTECTED_ZONE,
                              zone_size=UNIT_PROTECTED_ZONE_SIZE)
            )

        # Define array to store the obstacles created
        self.obstacles_in_field = []

        # Calculate the number of cells needed to fill based on desired percentage
        number_of_primitive_zones_to_make = self.calc_volume_of_field() * self.theoretical_fill_percentage / UNIT_OBSTACLE_VOLUME
        
        # Set counter for number of cells filled so far
        number_of_primitive_zones_created = 0

        # Declare variable to track how many times a new object has been re-generated 
        new_obstacle_loop_counter = 0

        # Declare obstacle loop limit
        max_obstacle_loop_index = 10

        # While the desired number of primitives has not been made
        while number_of_primitive_zones_created < number_of_primitive_zones_to_make and \
                new_obstacle_loop_counter < max_obstacle_loop_index:

            # Generate a new obstacle
            new_obstacle = Obstacle()

            # Increment the count for the type of obstacle created to ensure even distribution of obstacles
            new_obstacle_type = new_obstacle.get_obstacle_shape_type()
            self.obstacle_types[new_obstacle_type] = self.obstacle_types[new_obstacle_type] + 1

            # Try to place the obstacle in the field at a random location
            obstacle_is_valid, properly_placed_obstacle = self.generate_random_open_coordinates(new_obstacle)

            # If the obstacle was successfully placed, add it to the list of obstacles in the
            # field and increment the counter
            if obstacle_is_valid:
                self.obstacles_in_field.append(new_obstacle)
                number_of_primitive_zones_created = number_of_primitive_zones_created + \
                                                    new_obstacle.get_number_of_obstacle_primitives()

            # Else increment the counter for the number of times an obstacle couldn't be placed
            else:
                new_obstacle_loop_counter = new_obstacle_loop_counter + 1

        # Calculate the percentage of cells successfully filled with obstacles
        self.actual_fill_percentage = (number_of_primitive_zones_created * UNIT_OBSTACLE_VOLUME) / self.calc_volume_of_field()

    def is_point_open(self, point):
        return not self.is_point_within_obstacle(point) and \
               not self.is_point_within_protected_zones(point) and \
               self.is_point_within_bounds(point)

    def is_point_obstacle_free(self, point):
        result_a = not self.is_point_within_obstacle(point)
        result_b = self.is_point_within_bounds(point)
        return result_a and result_b

    def is_point_within_obstacle(self, point):
        for obstacle in self.obstacles_in_field:
            if obstacle.is_point_in_obstacle(point):
                return True
        return False

    def is_point_within_protected_zones(self, point):
        if len(self.obstacle_free_zones) > 0:
            for zone in self.obstacle_free_zones:
                if zone.is_point_within_zone(point):
                    return True
        return False

    def is_point_within_bounds(self, point):
        for dimension_of_point, bound_of_field in zip(point, self.field_bounds):
            if not bound_of_field[0] <= dimension_of_point <= bound_of_field[1]:
                return False
        return True

    # Generate a random coordinate within the obstacle field
    @staticmethod
    def generate_random_coordinates(field_bounds):
        result = []
        for bound in field_bounds:
            random_coordinate = round((random() * (bound[1] - bound[0]) + bound[0]), 2)
            result.append(UNIT_OBSTACLE_SIZE * round(random_coordinate / UNIT_OBSTACLE_SIZE))
        return result

    # Generate a random coordinate within the obstacle field that is open
    def generate_random_open_coordinates(self, obstacle_to_place: Obstacle):
        
        # Get obstacle bounds of new obstacle
        obstacle_bounds = obstacle_to_place.get_obstacle_bounds()

        valid_field_bounds = []

        # Calculate the bounds of all possible locations that the obstacle can be placed
        for obstacle_bound, field_size in zip(obstacle_bounds, self.field_bounds):
            valid_field_bounds.append((field_size[0]-obstacle_bound[0], field_size[1] - obstacle_bound[1]))

        # Set a flag for the validity of the coordinates
        coordinates_are_valid = False

        # Set default coordinates for result
        new_obstacle_coordinates = [0, 0, 0]

        new_coordinate_loop_counter = 0
        max_coordinate_loop_index = 1000

        # While valid coordinates have not been found, generate new coordinates
        while not coordinates_are_valid:

            coordinates_are_valid = True
            
            # Generate a new coordinate
            new_obstacle_coordinates = self.generate_random_coordinates(valid_field_bounds)

            # Move the new obstacle to the proposed coordinates
            obstacle_to_place.set_obstacle_origin(new_obstacle_coordinates)

            for obstacle_vertex in obstacle_to_place.get_all_obstacle_points():
                if not coordinates_are_valid:
                    break
                if not self.is_point_open(obstacle_vertex):
                    coordinates_are_valid = False
                    break

            # Increment the number of times generating a new coordinate by one
            new_coordinate_loop_counter = new_coordinate_loop_counter + 1

            # if the coordinates are not valid and the loop counter has been exceeded, break out of the loop
            if not coordinates_are_valid and new_coordinate_loop_counter > max_coordinate_loop_index:
                return False, None

        # Return the x, y, and z position of the coordinate
        return True, obstacle_to_place

    def calc_volume_of_field(self):
        temp_result = 1
        for dimension in self.field_bounds:
            temp_result = temp_result * abs(dimension[1] - dimension[0])
        return temp_result

    def get_obstacles_in_field(self):
        return self.obstacles_in_field

    def get_actual_fill_density(self):
        return self.actual_fill_percentage

    def generate_header_info(self):
        temp_result = []
        for bound in self.field_bounds:
            temp_result.append(bound[1] - bound[0])
        temp_result.append(UNIT_OBSTACLE_SIZE)
        return temp_result

    def get_origins_of_all_obstacle_primitives(self):
        data = []
        for obstacle in self.obstacles_in_field:
            for primitive in obstacle.get_obstacle_primitives():
                data.append(primitive.get_origin())
        return data


# Define file behaviour when ran as main
if __name__ == '__main__':

    # Generate a new obstacle field
    newObstacleField = ObstacleField([[0, 200], [0, 300], [-75, 0]], .05, obstacle_free_points=[[0, 0, 0], [50, 50, -25]])
    print("done")
