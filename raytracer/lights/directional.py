from raytracer.lights.light_t import Light
from raytracer.vec3 import Vec3


class DirectionalLight(Light):
    __slots__ = ("direction", "color", "intensity")

    def __init__(self, direction: Vec3, color: Vec3, intensity: float):
        assert 0 <= intensity <= 1, "intensity must be between 0 and 1"

        # multiply direction by -1
        # to have ray go from camera to light
        # rather than the other way around
        self.direction = -direction
        self.color = color
        self.intensity = intensity

    def direction_at(self, point: Vec3) -> Vec3:
        return self.direction
