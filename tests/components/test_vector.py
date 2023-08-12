from src.components.vector import *
import math
import pytest


class TestVector:
    def test_vector_eq(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(1, 2, 3)
        assert v1 == v2

        v3 = Vector(1, 2, 3)
        v4 = Vector(1, 2, 4)
        assert v3 != v4
        assert v3 != 1

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

        v2 = Vector(1, 2, 3)
        assert v2 / v1 == Vector(1, 1, 1)

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

    def test_vector_pow(self):
        v1 = Vector(1, 2, 3)
        assert v1**2 == Vector(1, 4, 9)

    def test_vector_transform(self):
        v1 = Vector(1, 2, 3)
        m1 = [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
        ]
        m2 = [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 0],
        ]

        assert v1.transform(m1) == Vector(1, 2, 3)
        assert v1.transform(m2) == Vector(1, 2, 0)

        m3 = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        m4 = [[1, 0, 0, 1], [0, 1, 0, 2], [0, 0, 1, 3], [0, 0, 0, 1]]

        assert v1.transform(m3) == Vector(1, 2, 3)
        assert v1.transform(m4) == Vector(2, 4, 6)

        m5 = [[1, 0, 0, 1], [0, 1, 0, 2], [0, 0, 1]]

        with pytest.raises(ValueError):
            v1.transform(m5)


class TestVectorOperations:
    def test_dot_product(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(2, 3, 4)
        assert dot_product(v1, v2) == 20

    def test_cross_product(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(2, 3, 4)
        assert cross_product(v1, v2) == Vector(-1, 2, -1)
