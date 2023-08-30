from src.components.light import Light
from src.ui.color_ui import create_color
from src.ui.point_ui import get_point
from src.ui.utils import ask_continue


def create_lights() -> list[Light]:
    """Creates a list of lights from user input."""
    first_run = True
    lights: list[Light] = []
    while first_run or ask_continue("lights"):
        first_run = False
        color = create_color("light")
        try:
            lights.append(
                Light(
                    position=get_point("Enter the position of the light (x, y, z): "),
                    color=color,
                )
            )
        except ValueError:
            print("Invalid position. Please try again.")

    return lights
