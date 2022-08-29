from __future__ import annotations

from typing import List

from raytracer.materials import Diffuse
from raytracer.materials.material_t import Material
from raytracer.objects.object_t import Object
from raytracer.objects.triangle import Triangle
from raytracer.linalg import Vec3


class Mesh(Object):
    # .normal() and .intersect() are not implemented
    # because the Mesh class will be handled differently
    # by the render function

    __slots__ = ("objects",)

    def __init__(self, objects: List[Object]):
        self.triangles = objects

    @classmethod
    def from_obj(
        cls,
        obj_file: str,
        material: Material,
        scale: float = 1.0,
        translate: Vec3 = Vec3(0, 0, 0),
    ) -> Mesh:
        # ignores textures and materials for now

        with open(obj_file, "r") as f:
            vertices = []
            triangles = []
            for line in f:
                args = line.split()
                if args[0] == "v":
                    x, y, z = map(float, args[1:4])
                    vertices.append(Vec3(x, y, z) * scale + translate)
                elif args[0] == "f":
                    a, b, c = map(lambda x: int(x.split("/")[0]), args[1:4])
                    triangles.append(
                        Triangle(
                            vertices[a - 1],
                            vertices[b - 1],
                            vertices[c - 1],
                            material,
                        )
                    )

        return cls(triangles)
