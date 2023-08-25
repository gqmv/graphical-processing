from src.components.camera import Camera
from src.components.point import Point
from src.components.vector import Vector
from src.ui.utils import get_triplet


def create_camera() -> Camera:
    """Creates a camera from user input."""
    while True:
        distance_from_screen = input("Enter the distance from the screen: ")
        vertical_resolution = input("Enter the vertical resolution: ")
        horizontal_resolution = input("Enter the horizontal resolution: ")
        try:
            pos_x, pos_y, pos_z = get_triplet(
                "Enter the position of the camera (x, y, z): "
            )
            look_at_x, look_at_y, look_at_z = get_triplet(
                "Enter the look at of the camera (x, y, z): "
            )
            v_up_x, v_up_y, v_up_z = get_triplet(
                "Enter the v up of the camera (x, y, z): "
            )
            return Camera(
                position=Point(float(pos_x), float(pos_y), float(pos_z)),
                look_at=Point(float(look_at_x), float(look_at_y), float(look_at_z)),
                v_up=Vector(float(v_up_x), float(v_up_y), float(v_up_z)),
                distance_from_screen=float(distance_from_screen),
                vertical_resolution=int(vertical_resolution),
                horizontal_resolution=int(horizontal_resolution),
            )
        except ValueError:
            print("Invalid input. Please try again.")
