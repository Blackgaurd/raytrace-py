from enum import Enum


class Material:
    def __init__(self, *args, **kwargs):
        self.type: MaterialBehavior


class MaterialBehavior(Enum):
    diffuse = 1
    reflect = 2
    reflect_refract = 3
