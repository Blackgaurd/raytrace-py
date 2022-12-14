from typing import Tuple

from raytracer.linalg import EPSILON, Vec3
from raytracer.materials import Material
from raytracer.objects.object_t import Object


class Triangle(Object):
    __slots__ = ("a", "b", "c", "material", "N")

    def __init__(self, a: Vec3, b: Vec3, c: Vec3, material: Material):
        self.a = a
        self.b = b
        self.c = c
        self.material = material

        self.N = (b - a).cross(c - a).normalize()

    def normal(self, ray_d: Vec3, intersect: Vec3) -> Vec3:
        # return self.N or -self.N depending on which normal has a
        # smaller theta angle with the ray origin

        # if (-ray_d).tt_angle(self.N) < (-ray_d).tt_angle(-self.N)
        # simplifies to:
        # if ray_d.tt_angle(self.N) > ray_d.tt_angle(-self.N)
        if ray_d.tt_angle(self.N) > ray_d.tt_angle(-self.N):
            return self.N
        return -self.N

    def intersect(self, ray_o: Vec3, ray_d: Vec3) -> Tuple[bool, float]:
        # there exist faster triangle-ray intersection algorithms
        # but this is good enough for now

        N_ray_dir = ray_d.dot(self.N)
        if abs(N_ray_dir) < EPSILON:
            return False, 0

        d = -self.N.dot(self.a)
        t = -(self.N.dot(ray_o) + d) / N_ray_dir

        if t < 0:
            return False, 0

        P = ray_o + ray_d * t

        edge_ab = self.b - self.a
        vpa = P - self.a
        C = edge_ab.cross(vpa)
        if self.N.dot(C) < 0:
            return False, 0

        edge_bc = self.c - self.b
        vpb = P - self.b
        C = edge_bc.cross(vpb)
        if self.N.dot(C) < 0:
            return False, 0

        edge_ca = self.a - self.c
        vpc = P - self.c
        C = edge_ca.cross(vpc)
        if self.N.dot(C) < 0:
            return False, 0

        return True, t

    def __repr__(self) -> str:
        return f"Triangle(a={self.a}, b={self.b}, c={self.c}, material={self.material})"

    def __str__(self) -> str:
        return f"Triangle(a={self.a}, b={self.b}, c={self.c}, m={self.material})"
