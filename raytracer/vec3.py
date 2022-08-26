from __future__ import annotations

import math


class Vec3:
    __slots__ = ("x", "y", "z")

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def from_rgb(cls, red: float, green: float, blue: float) -> Vec3:
        return Vec3(red, green, blue) / 255

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
