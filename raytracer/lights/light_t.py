from raytracer.linalg import Vec3


class Light:
    def __init__(self, color: Vec3, intensity: float, *args, **kwargs):
        self.intensity = intensity
        self.color = color
        raise NotImplementedError()

    def direction_at(self, point: Vec3) -> Vec3:
        raise NotImplementedError()
