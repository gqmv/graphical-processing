from src.components.color import Color


class TestColor:
    def test_color_from_hex(self):
        color = Color.from_hex("#ffffff")
        assert color.r == 1.0
        assert color.g == 1.0
        assert color.b == 1.0

    def test_color_from_rgb(self):
        color = Color.from_rgb(255, 255, 255)
        assert color.r == 1.0
        assert color.g == 1.0
        assert color.b == 1.0
