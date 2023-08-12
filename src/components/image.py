from pathlib import Path

from components.color import Color


class Image:
    """A class representing an image."""

    def __init__(self, vertical_resolution: int, horizontal_resolution: int):
        self.vertical_resolution = vertical_resolution
        self.horizontal_resolution = horizontal_resolution
        self._pixels = [
            [Color(0, 0, 0) for _ in range(horizontal_resolution)]
            for _ in range(vertical_resolution)
        ]

    def get_pixel(self, x: int, y: int) -> Color:
        return self._pixels[y][x]

    def set_pixel(self, x: int, y: int, color: Color) -> None:
        self._pixels[y][x] = color

    def write_ppm(self, filename: str) -> None:
        with open(filename, "w") as f:
            f.write(f"P3 {self.horizontal_resolution} {self.vertical_resolution} 255\n")

            for row in self._pixels:
                for color in row:
                    rgb_color = color.as_rgb()
                    f.write(f"{rgb_color[0]} {rgb_color[1]} {rgb_color[2]}")
                    f.write("\n")
