from typing import Tuple

from raytracer.linalg import Vec3
from raytracer.materials import Material


class Object:
    def __init__(self, material: Material, *args, **kwargs):
        self.material = material
        raise NotImplementedError()

    def normal(self, ray_d: Vec3, intersect: Vec3) -> Vec3:
        raise NotImplementedError()

    def intersect(self, ray_o: Vec3, ray_d: Vec3) -> Tuple[bool, float]:
        raise NotImplementedError()
