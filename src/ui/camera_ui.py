from src.components.camera import Camera
from src.ui.point_ui import get_point
from src.ui.vector_ui import get_vector


def create_camera() -> Camera:
    """Creates a camera from user input."""
    while True:
        distance_from_screen = input("Enter the distance from the screen: ")
        vertical_resolution = input("Enter the vertical resolution: ")
        horizontal_resolution = input("Enter the horizontal resolution: ")
        try:
            return Camera(
                position=get_point("Enter the position of the camera (x, y, z): "),
                look_at=get_point(
                    "Enter the point the camera is looking at (x, y, z): "
                ),
                v_up=get_vector("Enter the up vector (x, y, z): "),
                distance_from_screen=float(distance_from_screen),
                vertical_resolution=int(vertical_resolution),
                horizontal_resolution=int(horizontal_resolution),
            )
        except ValueError:
            print("Invalid input. Please try again.")
