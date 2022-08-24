from typing import Tuple

from raytracer.vec3 import Vec3


class Object:
    def __init__(self, albedo: Vec3, *args, **kwargs):
        self.albedo = albedo
        raise NotImplementedError()

    def normal(self, ray_d: Vec3, intersect: Vec3) -> Vec3:
        raise NotImplementedError()

    def intersect(self, ray_o: Vec3, ray_d: Vec3) -> Tuple[bool, float]:
        raise NotImplementedError()
