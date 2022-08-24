from typing import Tuple

from raytracer.vec3 import Vec3


class Light:
    def __init__(self, intensity: float, *args, **kwargs):
        self.intensity = intensity
        raise NotImplementedError()

    def direction_at(self, point: Vec3) -> Vec3:
        raise NotImplementedError()
