import math

from raytracer.materials.material_t import MaterialBehavior
from raytracer.materials.reflect import Reflect
from raytracer.vec3 import Vec3


def clamp(x: float, _min: float, _max: float) -> float:
    return max(_min, min(x, _max))


class ReflectRefract(Reflect):
    __slots__ = ("type", "ior")
    AIR_IOR = 1

    def __init__(self, refractive_index: float):
        # ior stands for index of refraction
        self.ior = refractive_index
        self.type = MaterialBehavior.reflect_refract

    def refract(self, ray_d: Vec3, normal: Vec3) -> Vec3:
        n_dot_i = normal.dot(ray_d)
        ior = self.ior
        air_ior = self.AIR_IOR

        if n_dot_i < 0:
            n_dot_i = -n_dot_i
        else:
            normal = -normal
            ior, air_ior = air_ior, ior

        ior_ratio = air_ior / ior

        # handling total internal reflection
        k = 1 - ior_ratio * ior_ratio * (1 - n_dot_i * n_dot_i)
        if k < 0:
            # this case will never be used as the
            # function calling this one will make sure
            # to not get a refraction component if
            # total internal reflection happens

            # this value is insignificant
            return Vec3(0, 0, 0)

        return (
            ior_ratio * ray_d + (ior_ratio * n_dot_i - math.sqrt(k)) * normal
        ).normalize()

    def fresnel(self, ray_d: Vec3, normal: Vec3) -> float:
        # returns the amount of light refracted

        cosi = clamp(-1, 1, ray_d.dot(normal))
        ior = self.ior
        air_ior = self.AIR_IOR

        if cosi > 0:
            air_ior, ior = ior, air_ior

        ior_ratio = air_ior / ior

        sint = ior_ratio * math.sqrt(max(0, 1 - cosi * cosi))
        if sint >= 1:
            # total internal reflection
            return 1

        cost = math.sqrt(max(0, 1 - sint * sint))
        cosi = abs(cosi)
        Rs = ((air_ior * cosi) - (ior * cost)) / ((air_ior * cosi) + (ior * cost))
        Rp = ((ior * cosi) - (air_ior * cost)) / ((ior * cosi) + (air_ior * cost))
        return (Rs**2 + Rp**2) / 2
