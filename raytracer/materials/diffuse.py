from raytracer.linalg import Vec3
from raytracer.materials.material_t import Material


class Diffuse(Material):
    __slots__ = ("type", "albedo")

    def __init__(self, albedo: Vec3):
        # albedo is the amount of light (red, green, blue)
        # that gets reflected
        self.albedo = albedo

    def __repr__(self) -> str:
        return f"Diffuse(albedo={self.albedo})"
