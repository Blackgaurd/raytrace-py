from raytracer.linalg import Vec3
from raytracer.materials.material_t import Material


class Reflect(Material):
    __slots__ = ("type",)

    def __init__(self) -> None:
        pass

    def reflect(self, ray_d: Vec3, normal: Vec3) -> Vec3:
        return (ray_d - normal * 2 * ray_d.dot(normal)).normalize()

    def __repr__(self) -> str:
        return "Reflect()"
