from src.components.point import *


class TestPoint:
    def test_init(self):
        point = Point(1, 2, 3)
        assert point.x == 1
        assert point.y == 2
        assert point.z == 3
    
    def test_add(self):
        point1 = Point(1, 2, 3)
        point2 = Point(4, 5, 6)
        point3 = point1 + point2
        assert point3.x == 5
        assert point3.y == 7
        assert point3.z == 9
        
    def test_sub(self):
        point1 = Point(1, 2, 3)
        point2 = Point(4, 5, 6)
        point3 = point1 - point2
        assert point3.x == -3
        assert point3.y == -3
        assert point3.z == -3
        
    def test_mul(self):
        point = Point(1, 2, 3)
        point = point * 2
        assert point.x == 2
        assert point.y == 4
        assert point.z == 6
        
    def test_neg(self):
        point = Point(1, 2, 3)
        point = -point
        assert point.x == -1
        assert point.y == -2
        assert point.z == -3