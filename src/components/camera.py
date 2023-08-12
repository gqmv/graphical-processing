from src.components.point import *
from src.components.ray import Ray
from src.components.vector import *


class Camera:
    """A movable camera that can be used to render a scene."""

    def __init__(
        self,
        position: Point,
        look_at: Point,
        v_up: Vector,
        distance_from_screen: float,
        vertical_resolution: int,
        horizontal_resolution: int,
    ):
        self.position = position
        self.look_at = look_at
        self.v_up = v_up
        self.distance_from_screen = distance_from_screen
        self.vertical_resolution = vertical_resolution
        self.horizontal_resolution = horizontal_resolution

    def __repr__(self):
        return f"Camera(Pos: {self.position.__repr__}, look_at: {self.look_at.__repr__}, v_up: {self.v_up.__repr__}"

    @property
    def v_w(self) -> Vector:
        return (self.look_at - self.position).normalized()

    @property
    def v_u(self) -> Vector:
        return cross_product(self.v_up, self.v_w).normalized()

    @property
    def v_v(self) -> Vector:
        return cross_product(self.v_w, self.v_u)

    def get_ray(self, i: int, j: int) -> Ray:
        """Returns a ray from the camera to the pixel (i, j)"""
        screen_center = (self.v_w * self.distance_from_screen) + self.position

        relative_i = (i - self.horizontal_resolution / 2) / self.horizontal_resolution
        relative_j = (j - self.vertical_resolution / 2) / self.vertical_resolution

        i_offset_vector = self.v_u * relative_i
        j_offset_vector = self.v_v * relative_j

        point = screen_center + i_offset_vector + j_offset_vector
        direction = point - self.position
        return Ray(self.position, direction)

    @property
    def phong(self):
        # TODO: Unfinished method. Do not rely
        raise NotImplementedError
        Ia = 1
        Ka = 1
        Ia = 0.2
        Ka = 0.5
        Ks = 0.4
        N = 0.2
        vetor_r = 2 * ()
        I = (Ia * Ka) + (Ks * ())
        pass
