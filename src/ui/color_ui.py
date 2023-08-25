from src.components.color import Color
from src.ui.utils import get_triplet


def create_color(object_type: str) -> Color:
    """Creates a color from user input."""
    while True:
        try:
            r, g, b = get_triplet(f"Enter the color of the {object_type} (r, g, b): ")
            return Color(int(r), int(g), int(b))
        except ValueError:
            print("Invalid color. Please try again.")
