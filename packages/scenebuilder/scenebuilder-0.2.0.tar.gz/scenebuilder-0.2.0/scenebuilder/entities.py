from matplotlib.patches import Polygon
from numpy.typing import ArrayLike
from typing import List
import numpy as np


class Entity:
    """Class containing all necessary information about an Entity, such as ID and position"""

    def __init__(self, ID, position=None):
        self.ID = ID
        self.position = np.array(position)

    def move(self, new_position):
        self.position = new_position

    def distance_to_point(self, point):
        p = np.array(point)
        return np.linalg.norm(self.position - p)


class Drone(Entity):
    """Class containing all necessary information about a Drone Entity, not including its graphics"""

    def __init__(self, ID, position, goal: np.ndarray):
        super().__init__(ID, position)
        self.goal = np.array(goal)

    def is_near_goal(self, point, threshold=0.2):
        return np.linalg.norm(np.array(point) - self.goal[:2]) < threshold

    def move_end(self, new_position):
        self.goal = new_position

    def move_whole_drone(self, delta):
        self.position[:2] += delta
        self.goal[:2] += delta

    def click_near_arrow(self, p0, p1, event, threshold=0.2):
        click_position = np.array([event.xdata, event.ydata])
        p0 = np.array(p0)
        p1 = np.array(p1)
        dist_start = np.linalg.norm(click_position - p0)
        dist_end = np.linalg.norm(click_position - p1)
        arrow_length = np.linalg.norm(p1 - p0)

        # Using Heron's formula to compute area of triangle formed by start, end, and click points
        s = (dist_start + dist_end + arrow_length) / 2
        triangle_area = np.sqrt(
            s * (s - dist_start) * (s - dist_end) * (s - arrow_length)
        )

        # Distance from click to the line segment
        distance_to_line = 2 * triangle_area / arrow_length

        # Calculate projection of click point onto the arrow line segment
        dot_product = np.dot(p1 - p0, click_position - p0) / arrow_length**2
        projected_point = p0 + dot_product * (p1 - p0)

        # Check if the projected point lies between start and end
        is_within_segment = np.all(np.minimum(p0, p1) <= projected_point) and np.all(
            projected_point <= np.maximum(p0, p1)
        )

        if distance_to_line < threshold and is_within_segment:
            return True

        return False


class Obstacle(Entity):
    """Class containing all necessary information about a Building Entity, not including its graphics"""

    def __init__(self, vertices: ArrayLike):
        super().__init__(ID="building", position=None)
        # self.vertices = self.sort_vertices(vertices[:, :2])
        # Ensure the first and last vertices are not the same
        if np.array_equal(vertices[0, :2], vertices[-1, :2]):
            vertices = vertices[:-1, :2]  # Remove the last vertex if it's the same as the first one
        self.vertices = vertices[:, :2]

    def sort_vertices(self, vertices):
        """Sorts the vertices by angle around the centre of mass of the polygon"""
        Xavg = np.mean(vertices[:, 0:1])
        Yavg = np.mean(vertices[:, 1:2])
        angles = np.arctan2(
            (Yavg * np.ones(len(vertices[:, 1])) - vertices[:, 1]),
            (Xavg * np.ones(len(vertices[:, 0])) - vertices[:, 0]),
        )
        sorted_angles = sorted(zip(angles, vertices), reverse=True)
        points_sorted = np.vstack([x for y, x in sorted_angles])
        return points_sorted

    def move_vertex(self, vertex_index, new_position):
        self.vertices[vertex_index] = new_position

    def move_building(self, delta):
        """Move the entire building by a 2D array delta

        Args:
            delta (ArrayLike): 2D array
        """
        for vertex in self.vertices:
            vertex += delta

    def insert_vertex(self, position, tolerance=0.1):
        """Insert a vertex at a given position if near an edge"""
        for i in range(len(self.vertices)):
            start_point = self.vertices[i]
            end_point = self.vertices[(i + 1) % len(self.vertices)]

            if self._point_near_edge(position, start_point, end_point, tolerance):
                self.vertices = np.insert(self.vertices, i + 1, position, axis=0)
                return True
        return False

    def _point_near_edge(self, point, start, end, tolerance):
        """Check if the point is near the edge defined by start and end points"""
        # Compute the distance of the point from the line segment
        line_vector = np.array(end) - np.array(start)
        point_vector = np.array(point) - np.array(start)
        # Compute the projection of point_vector onto line_vector
        proj_length = np.dot(point_vector, line_vector) / np.linalg.norm(line_vector)

        if 0 <= proj_length <= np.linalg.norm(line_vector):
            # The projection is on the line segment
            proj_vector = proj_length * line_vector / np.linalg.norm(line_vector)
            distance = np.linalg.norm(point_vector - proj_vector)
            return distance < tolerance
        return False

    def contains_point(self, point):
        polygon = Polygon(self.vertices)
        return polygon.contains_point(point)
