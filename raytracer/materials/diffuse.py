from raytracer.materials.material_t import Material, MaterialBehavior
from raytracer.vec3 import Vec3


class Diffuse(Material):
    __slots__ = ("type", "albedo")

    def __init__(self, albedo: Vec3):
        # albedo is the amount of light (red, green, blue)
        # that gets reflected
        self.albedo = albedo
        self.type = MaterialBehavior.diffuse

    def __repr__(self) -> str:
        return f"Diffuse(albedo={self.albedo})"
