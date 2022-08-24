from raytracer.light.light_t import Light
from raytracer.vec3 import Vec3


class PointLight(Light):
    __slots__ = ("position", "color", "intensity")

    def __init__(self, position: Vec3, color: Vec3, intensity: float):
        assert 0 <= intensity <= 1, "intensity must be between 0 and 1"

        self.position = position
        self.color = color
        self.intensity = intensity

    def direction_at(self, point: Vec3) -> Vec3:
        return (self.position - point).normalize()
