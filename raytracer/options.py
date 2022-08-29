from dataclasses import dataclass
from typing import Union

from raytracer.linalg import Vec3

EPSILON = 1e-4


@dataclass
class Resolution:
    w: Union[int, float]
    h: Union[int, float]


@dataclass
class Settings:
    background_color: Vec3
    resolution: Resolution
    distance_to_image: float
    fov: float
    bias: float
