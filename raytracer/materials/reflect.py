from raytracer.materials.material_t import Material, MaterialBehavior
from raytracer.vec3 import Vec3


class Reflect(Material):
    __slots__ = ("type",)

    def __init__(self):
        self.type = MaterialBehavior.reflect

    def reflect(self, ray_d: Vec3, normal: Vec3) -> Vec3:
        return (ray_d - normal * 2 * ray_d.dot(normal)).normalize()
