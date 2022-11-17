# Import necessary packages
from ObstacleFieldGeneration.PrimitiveClasses.ObstactleFieldConstants import UNIT_OBSTACLE_SIZE, OBSTACLE_ZONE, PROTECTED_ZONE, UNALLOCATED_ZONE


class PrimitiveZone:

    # Initialize cell values
    def __init__(self, origin=None, zone_type=OBSTACLE_ZONE, zone_size=None):
        # If the origin of the zone is not given, set it as the origin
        if origin is None:
            # Define origin of the zone
            self.origin = [0, 0, 0]
        else:
            self.origin = origin

        # If the zone size is not given, use the default size
        if zone_size is None:
            zone_size = UNIT_OBSTACLE_SIZE

        # Save the size of the zone created
        self.zone_size = zone_size

        # Generate the bounding values of the zone
        self.bounds = []
        self.generate_bounds()

        # Generate the vertices of zone
        self.vertices = []
        self.generate_vertices()

        # Save the type of the zone
        self.zone_type = zone_type

    # Set the position values of the cell
    def set_origin(self, origin):
        self.origin = origin
        self.generate_bounds()
        self.generate_vertices()

    # Offset the origin of the zone by a given amount in each direction
    def offset_origin(self, offsets):

        for single_offset, i in zip(offsets, range(3)):
            self.origin[i] = self.origin[i] + single_offset
        self.generate_bounds()
        self.generate_vertices()

    # Set the zone as an obstacle zone
    def set_as_obstacle(self):
        self.zone_type = OBSTACLE_ZONE

    # Set the zone as a protected zone
    def set_as_protected(self):
        self.zone_type = PROTECTED_ZONE

    # Set the zone as unallocated
    def set_as_unallocated(self):
        self.zone_type = UNALLOCATED_ZONE

    # Get the zone origin
    def get_origin(self):
        return self.origin

    # Get the zone type
    def get_type(self):
        return self.zone_type

    # Check if a given point is within the zone
    def is_point_within_zone(self, point):
        for bound, dimension in zip(self.bounds, point):
            if not bound[0] <= dimension <= bound[1]:
                return False
        return True

    def generate_vertices(self):
        self.vertices = []
        coordinates_to_generate = [0, .5, 1]
        for x in coordinates_to_generate:
            for y in coordinates_to_generate:
                for z in coordinates_to_generate:

                    temp_result = []
                    for dimension_of_vertex, dimension_of_origin in zip([x, y, z], self.origin):
                        temp_result.append(dimension_of_vertex * self.zone_size + dimension_of_origin)

                    if x == y == z == coordinates_to_generate[1]:
                        self.vertices.insert(0, temp_result)
                    else:

                        self.vertices.append(temp_result)

    def generate_bounds(self):
        self.bounds = []
        for dimension in self.origin:
            self.bounds.append([i + dimension for i in [0, self.zone_size]])

    def get_vertices(self):
        return self.vertices

    # Create a string representation of the string
    def visualize_as_string(self):
        return f'{self.origin[0]:03}, {self.origin[1]:03}, {self.origin[2]:03}, {self.zone_type:01}'


if __name__ == "__main__":
    test_zone_1 = PrimitiveZone()
    test_zone_1.set_origin([5, 5, 5])
    print("Done")