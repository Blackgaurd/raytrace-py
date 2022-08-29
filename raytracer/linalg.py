from __future__ import annotations

import math
from typing import List


class Vec3:
    __slots__ = ("x", "y", "z")

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def from_rgb(cls, red: float, green: float, blue: float) -> Vec3:
        return cls(red, green, blue) / 255

    def normalize(self) -> Vec3:
        return self / self.norm()

    def dot(self, other: Vec3) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: Vec3) -> Vec3:
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def norm(self) -> float:
        # Frobenius norm
        # same as magnitude
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def distance(self, other: Vec3) -> float:
        return math.sqrt(
            (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2
        )

    def tt_angle(self, other: Vec3) -> float:
        # tail-tail angle
        return math.acos(self.dot(other) / (self.norm() * other.norm()))

    def transform(self, matrix: Mat44) -> Vec3:
        ret = Vec3(
            self.x * matrix[0][0]
            + self.y * matrix[1][0]
            + self.z * matrix[2][0]
            + matrix[3][0],
            self.x * matrix[0][1]
            + self.y * matrix[1][1]
            + self.z * matrix[2][1]
            + matrix[3][1],
            self.x * matrix[0][2]
            + self.y * matrix[1][2]
            + self.z * matrix[2][2]
            + matrix[3][2],
        )

        w = (
            self.x * matrix[0][3]
            + self.y * matrix[1][3]
            + self.z * matrix[2][3]
            + matrix[3][3]
        )
        if w != 1 and w != 0:
            ret /= w

        return ret

    def __repr__(self) -> str:
        return f"Vec3({self.x}, {self.y}, {self.z})"

    def __str__(self) -> str:
        return f"({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"

    def __add__(self, other: Vec3 | float | int) -> Vec3:
        if isinstance(other, Vec3):
            return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
        elif isinstance(other, (float, int)):
            return Vec3(self.x + other, self.y + other, self.z + other)
        else:
            raise TypeError(
                f"unsupported operand type(s) for +: {type(self)} and {type(other)}"
            )

    def __sub__(self, other: Vec3 | float | int) -> Vec3:
        if isinstance(other, Vec3):
            return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
        elif isinstance(other, (float, int)):
            return Vec3(self.x - other, self.y - other, self.z - other)
        else:
            raise TypeError(
                f"unsupported operand type(s) for -: {type(self)} and {type(other)}"
            )

    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def __mul__(self, other: Vec3 | float | int) -> Vec3:
        if isinstance(other, Vec3):
            return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)
        elif isinstance(other, (float, int)):
            return Vec3(self.x * other, self.y * other, self.z * other)
        else:
            raise TypeError(
                f"unsupported operand type(s) for *: {type(self)} and {type(other)}"
            )

    def __rmul__(self, other: Vec3 | float | int) -> Vec3:
        return self * other

    def __truediv__(self, other: Vec3 | float | int) -> Vec3:
        if isinstance(other, Vec3):
            return Vec3(self.x / other.x, self.y / other.y, self.z / other.z)
        elif isinstance(other, (float, int)):
            return Vec3(self.x / other, self.y / other, self.z / other)
        else:
            raise TypeError(
                f"unsupported operand type(s) for /: {type(self)} and {type(other)}"
            )

    def __abs__(self) -> Vec3:
        return Vec3(abs(self.x), abs(self.y), abs(self.z))


class Mat44:
    __slots__ = "arr"

    def __init__(self):
        # identity matrix
        self.arr = [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ]

    @classmethod
    def from_list(cls, arr: List[List[float]]) -> Mat44:
        assert len(arr) == 4 and len(arr[0]) == 4

        ret = cls()
        for i in range(4):
            for j in range(4):
                ret.arr[i][j] = arr[i][j]
        return ret

    def __repr__(self) -> str:
        return f"Mat44({self.arr})"

    def transpose(self) -> Mat44:
        ret = Mat44()
        for i in range(4):
            for j in range(4):
                ret.arr[i][j] = self.arr[j][i]
        return ret

    def __mul__(self, other: Mat44) -> Mat44:
        ret = Mat44()
        for i in range(4):
            for j in range(4):
                ret.arr[i][j] = sum(self.arr[i][k] * other.arr[k][j] for k in range(4))

    def __getitem__(self, index: int) -> List[float]:
        return self.arr[index]
