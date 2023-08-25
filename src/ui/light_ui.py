from src.components.light import Light
from src.components.point import Point
from src.ui.color_ui import create_color
from src.ui.utils import ask_continue, get_triplet


def create_lights() -> list[Light]:
    """Creates a list of lights from user input."""
    first_run = True
    lights: list[Light] = []
    while first_run or ask_continue("lights"):
        first_run = False
        color = create_color("light")
        try:
            x, y, z = get_triplet("Enter the position of the light (x, y, z): ")
            lights.append(
                Light(
                    position=Point(float(x), float(y), float(z)),
                    color=color,
                )
            )
        except ValueError:
            print("Invalid position. Please try again.")

    return lights
