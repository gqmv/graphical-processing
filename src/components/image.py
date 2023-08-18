from pathlib import Path

from src.components.color import Color


class Image:
    """A class representing an image."""

    def __init__(
        self,
        vertical_resolution: int,
        horizontal_resolution: int,
        pixels: list[list[Color]] | None = None,
    ):
        self.vertical_resolution = vertical_resolution
        self.horizontal_resolution = horizontal_resolution
        if pixels is None:
            self._pixels = [
                [Color(0, 0, 0) for _ in range(horizontal_resolution)]
                for _ in range(vertical_resolution)
            ]
        else:
            self._pixels = pixels

    def set_pixels(self, pixels: list[list[Color]]) -> None:
        """Set the pixels of the image."""
        self._pixels = pixels

    def get_pixel(self, x: int, y: int) -> Color:
        """Get the color of a pixel."""
        return self._pixels[y][x]

    def set_pixel(self, x: int, y: int, color: Color) -> None:
        """Set the color of a pixel."""
        self._pixels[y][x] = color

    def write_ppm(self, filename: str | Path) -> None:
        """Write the image to a PPM file located at the given path."""
        with open(filename, "w") as f:
            f.write(f"P3 {self.horizontal_resolution} {self.vertical_resolution} 255\n")

            for row in self._pixels:
                for color in row:
                    rgb_color = color.as_rgb()
                    f.write(f"{rgb_color[0]} {rgb_color[1]} {rgb_color[2]}")
                    f.write("\n")
