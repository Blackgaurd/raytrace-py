import math
from typing import Tuple
from raytracer.materials import Material

from raytracer.objects.object_t import Object
from raytracer.vec3 import Vec3


class Sphere(Object):
    __slots__ = ("origin", "radius", "amterial")

    def __init__(self, origin: Vec3, radius: float, material: Material):
        self.origin = origin
        self.radius = radius
        self.material = material

    def normal(self, ray_d: Vec3, intersect: Vec3) -> Vec3:
        return (intersect - self.origin).normalize()

    def intersect(self, ray_o: Vec3, ray_d: Vec3) -> Tuple[bool, float]:
        a = ray_d.x**2 + ray_d.y**2 + ray_d.z**2
        b = 2 * (
            ray_d.x * (ray_o.x - self.origin.x)
            + ray_d.y * (ray_o.y - self.origin.y)
            + ray_d.z * (ray_o.z - self.origin.z)
        )
        c = (
            self.origin.x**2
            + self.origin.y**2
            + self.origin.z**2
            + ray_o.x**2
            + ray_o.y**2
            + ray_o.z**2
            - 2 * (Vec3.dot(self.origin, ray_o))
            - self.radius**2
        )

        D = b**2 - 4 * a * c
        if D < 0:
            return False, 0

        t = (-b - math.sqrt(D)) / (2 * a)
        if t < 0:
            return False, 0
        return True, t
