from src.components.camera import *
from src.components.vector import *
from src.components.point import *


def is_orthogonal(v1: Vector, v2: Vector, v3: Vector) -> bool:
    dp1 = round(dot_product(v1, v2), 10)
    dp2 = round(dot_product(v1, v3), 10)
    dp3 = round(dot_product(v2, v3), 10)
    return dp1 == 0 and dp2 == 0 and dp3 == 0

class TestCamera:
    def test_camera_init(self):
        location = Point(0, 0, 0)
        look_at = Point(0, 0, 1)
        v_up = Vector(0, 1, 0)

        cam = Camera(location, look_at, v_up, 90, 1, 1)

        assert cam.location == location
        assert cam.look_at == look_at
        assert cam.v_up == v_up

    def test_camera_orthogonal_vectors(self):
        location = Point(0, 0, 0)
        look_at = Point(0, 0, 1)
        v_up = Vector(0, 1, 0)

        cam = Camera(location, look_at, v_up, 90, 1, 1)

        assert cam.v_w == Vector(0, 0, 1)
        assert cam.v_u == Vector(1, 0, 0)
        assert cam.v_v == Vector(0, 1, 0)

        location = Point(10, 8, 3)
        look_at = Point(3, 4, 2)
        v_up = Vector(0, 1, 0)
        
        cam_2 = Camera(location, look_at, v_up, 90, 1, 1)
        
        assert is_orthogonal(cam_2.v_w, cam_2.v_u, cam_2.v_v)
    
