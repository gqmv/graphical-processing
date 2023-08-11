from .vector import *
from .point import *


class Camera:
    def __init__(
        self,
        location: Point,
        look_at: Point,
        v_up: Vector,
        distance_from_screen: float,
        vertical_resolution: int,
        horizontal_resolution: int,
    ):
        self.location = location
        self.look_at = look_at
        self.v_up = v_up
        self.distance_from_screen = distance_from_screen
        self.vertical_resolution = vertical_resolution
        self.horizontal_resolution = horizontal_resolution

    @property
    def v_w(self) -> Vector:
        return (self.look_at - self.location).normalized()

    @property
    def v_u(self) -> Vector:
        return cross_product(self.v_up, self.v_w).normalized()

    @property
    def v_v(self) -> Vector:
        return cross_product(self.v_w, self.v_u)

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
