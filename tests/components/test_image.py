from src.components.color import Color
from src.components.image import Image


class TestImage:
    def test_image_get_pixel(self):
        img = Image(10, 10)
        assert img.get_pixel(0, 0) == Color(0, 0, 0)

    def test_image_write_ppm(self, tmp_path):
        file = tmp_path / "test.ppm"
        filename = file.as_posix()

        img = Image(10, 10)
        img.set_pixel(0, 0, Color.from_rgb(255, 255, 255))
        img.write_ppm(filename)

        img_text: str = file.read_text()
        img_lines = img_text.splitlines()
        assert img_lines[0] == "P3 10 10 255"
        assert img_lines[1] == "255 255 255"
        assert img_lines[2] == "0 0 0"
