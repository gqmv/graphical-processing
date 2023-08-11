from src.components.vector import *
import math


class TestVector:
    def test_vector_eq(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(1, 2, 3)
        assert v1 == v2

        v3 = Vector(1, 2, 3)
        v4 = Vector(1, 2, 4)
        assert v3 != v4

    def test_vector_add(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(2, 3, 4)
        assert v1 + v2 == Vector(3, 5, 7)

        v3 = Vector(1, 2, 3)
        v4 = Vector(-2, -3, -4)
        assert v3 + v4 == Vector(-1, -1, -1)

    def test_vector_sub(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(2, 3, 4)
        assert v1 - v2 == Vector(-1, -1, -1)

        v3 = Vector(1, 2, 3)
        v4 = Vector(-2, -3, -4)
        assert v3 - v4 == Vector(3, 5, 7)

    def test_vector_mul(self):
        v1 = Vector(1, 2, 3)
        assert v1 * 2 == Vector(2, 4, 6)
        assert 2 * v1 == Vector(2, 4, 6)

        v2 = Vector(1, 2, 3)
        assert v1 * v2 == Vector(1, 4, 9)

    def test_vector_div(self):
        v1 = Vector(1, 2, 3)
        assert v1 / 2 == Vector(0.5, 1, 1.5)

    def test_vector_neg(self):
        v1 = Vector(1, 2, 3)
        assert -v1 == Vector(-1, -2, -3)

    def test_vector_norm(self):
        v1 = Vector(1, 2, 3)
        assert v1.norm() == math.sqrt(14)

    def test_vector_normalize(self):
        v1 = Vector(1, 2, 3)
        assert v1.normalized() == Vector(
            1 / math.sqrt(14), 2 / math.sqrt(14), 3 / math.sqrt(14)
        )


class TestVectorOperations:
    def test_dot_product(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(2, 3, 4)
        assert dot_product(v1, v2) == 20

    def test_cross_product(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(2, 3, 4)
        assert cross_product(v1, v2) == Vector(-1, 2, -1)
