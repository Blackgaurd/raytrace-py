from __future__ import annotations

import math
from typing import List

EPSILON = 1e-4
ROW_MAJOR = True


def float_eq(a: float, b: float) -> bool:
    return abs(a - b) < EPSILON


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

    def to_rgba(self) -> int:
        # converts to hex color (0xRRGGBBAA)
        r, g, b = map(lambda x: round(x * 255), (self.x, self.y, self.z))
        return (r << 16 | g << 8 | b) << 8 | 255

    def to_abgr(self) -> int:
        # converts to reversed hex color (0xAABBGGRR)
        r, g, b = map(lambda x: round(x * 255), (self.x, self.y, self.z))
        return 255 << 24 | b << 16 | g << 8 | r

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

    def __neg__(self) -> Vec3:
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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vec3):
            raise TypeError(
                f"unsupported operand type(s) for ==: {type(self)} and {type(other)}"
            )

        return (
            float_eq(self.x, other.x)
            and float_eq(self.y, other.y)
            and float_eq(self.z, other.z)
        )

    def __abs__(self) -> Vec3:
        return Vec3(abs(self.x), abs(self.y), abs(self.z))


class Mat44:
    __slots__ = "arr"

    def __init__(self) -> None:
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
        ret.arr = arr
        return ret

    @classmethod
    def camera(cls, look_from: Vec3, look_at: Vec3, up: Vec3 = Vec3(0, 1, 0)) -> Mat44:
        forward = (look_from - look_at).normalize()

        if forward == Vec3(0, 1, 0) or forward == Vec3(0, -1, 0):
            raise ValueError("forward vector is parallel to up vector")

        right = up.cross(forward).normalize()
        newup = forward.cross(right).normalize()

        ret = cls()

        ret[0][0] = right.x
        ret[0][1] = right.y
        ret[0][2] = right.z

        ret[1][0] = newup.x
        ret[1][1] = newup.y
        ret[1][2] = newup.z

        ret[2][0] = forward.x
        ret[2][1] = forward.y
        ret[2][2] = forward.z

        ret[3][0] = look_from.x
        ret[3][1] = look_from.y
        ret[3][2] = look_from.z

        return ret

    def transpose(self) -> Mat44:
        ret = Mat44()
        for i in range(4):
            for j in range(4):
                ret.arr[i][j] = self.arr[j][i]
        return ret

    def transform_point(self, vec: Vec3) -> Vec3:
        if ROW_MAJOR:
            ret = Vec3(
                vec.x * self.arr[0][0]
                + vec.y * self.arr[1][0]
                + vec.z * self.arr[2][0],
                vec.x * self.arr[0][1]
                + vec.y * self.arr[1][1]
                + vec.z * self.arr[2][1],
                vec.x * self.arr[0][2]
                + vec.y * self.arr[1][2]
                + vec.z * self.arr[2][2],
            )
            w = vec.x * self.arr[0][3] + vec.y * self.arr[1][3] + vec.z * self.arr[2][3]

            if w != 0:
                ret /= w
            return ret

        else:
            ret = Vec3(
                vec.x * self.arr[0][0]
                + vec.y * self.arr[0][1]
                + vec.z * self.arr[0][2],
                vec.x * self.arr[1][0]
                + vec.y * self.arr[1][1]
                + vec.z * self.arr[1][2],
                vec.x * self.arr[2][0]
                + vec.y * self.arr[2][1]
                + vec.z * self.arr[2][2],
            )
            w = vec.x * self.arr[3][0] + vec.y * self.arr[3][1] + vec.z * self.arr[3][2]

            if w != 0:
                ret /= w
            return ret

    def transform_dir(self, vec: Vec3) -> Vec3:
        if ROW_MAJOR:
            return Vec3(
                vec.x * self.arr[0][0]
                + vec.y * self.arr[1][0]
                + vec.z * self.arr[2][0],
                vec.x * self.arr[0][1]
                + vec.y * self.arr[1][1]
                + vec.z * self.arr[2][1],
                vec.x * self.arr[0][2]
                + vec.y * self.arr[1][2]
                + vec.z * self.arr[2][2],
            )
        else:
            return Vec3(
                vec.x * self.arr[0][0]
                + vec.y * self.arr[0][1]
                + vec.z * self.arr[0][2],
                vec.x * self.arr[1][0]
                + vec.y * self.arr[1][1]
                + vec.z * self.arr[1][2],
                vec.x * self.arr[2][0]
                + vec.y * self.arr[2][1]
                + vec.z * self.arr[2][2],
            )

    def __repr__(self) -> str:
        return f"Mat44({self.arr})"

    def __mul__(self, other: Mat44) -> Mat44:
        ret = Mat44()
        for i in range(4):
            for j in range(4):
                ret.arr[i][j] = sum(self.arr[i][k] * other.arr[k][j] for k in range(4))
        return ret

    def __getitem__(self, index: int) -> List[float]:
        return self.arr[index]
