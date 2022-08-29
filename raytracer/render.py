import itertools
import math
import sys
from typing import List

from raytracer.lights import Light
from raytracer.linalg import Vec3
from raytracer.materials import Diffuse, Reflect, ReflectRefract
from raytracer.objects import Object
from raytracer.objects.mesh import Mesh
from raytracer.options import Resolution, Settings


def check_interference(
    ray_o: Vec3, ray_d: Vec3, objects: List[Object], source_ind: int
) -> bool:
    # check if ray intersects with any object
    # assuming that all objects are opaque
    for i, obj in enumerate(objects):
        if i == source_ind or not isinstance(obj.material, Diffuse):
            continue
        intersect, t = obj.intersect(ray_o, ray_d)
        if intersect:
            return True
    return False


def cast_ray(
    ray_o: Vec3,
    ray_d: Vec3,
    objects: List[Object],
    lights: List[Light],
    settings: Settings,
    max_depth: int,
) -> Vec3:
    if max_depth == 0:
        return settings.background_color

    closest_t = float("inf")
    obj_ind = -1
    for i, obj in enumerate(objects):
        intersect, t = obj.intersect(ray_o, ray_d)
        if intersect and t < closest_t:
            closest_t = t
            obj_ind = i

    if obj_ind == -1:
        return settings.background_color

    obj = objects[obj_ind]
    intersect_p: Vec3 = ray_o + ray_d * closest_t
    normal = obj.normal(ray_d, intersect_p)
    bias = normal * settings.bias

    hit_color = Vec3(0, 0, 0)

    if isinstance(obj.material, Diffuse):
        # diffuse lighting
        for light in lights:
            light_dir = light.direction_at(intersect_p)

            # shadows
            if check_interference(intersect_p + bias, light_dir, objects, obj_ind):
                continue

            # shading
            hit_color += (
                obj.material.albedo
                / math.pi
                * light.intensity
                * light.color
                * max(0, normal.dot(light_dir))
            )

    elif isinstance(obj.material, Reflect):
        # perfect mirror reflection
        reflect_d = obj.material.reflect(ray_d, normal)
        hit_color += (
            cast_ray(
                intersect_p + bias,
                reflect_d,
                objects,
                lights,
                settings,
                max_depth - 1,
            )
            * 0.8  # rough fresnel effect approximation
        )

    elif isinstance(obj.material, ReflectRefract):
        refract_k = obj.material.fresnel(ray_d, normal)
        outside = ray_d.dot(normal) < 0
        ray_o = intersect_p + bias if outside else intersect_p - bias

        refract_color = Vec3(0, 0, 0)
        if refract_k < 1:
            # refraction occurs
            refract_d = obj.material.refract(ray_d, normal)
            refract_color = cast_ray(
                ray_o, refract_d, objects, lights, settings, max_depth - 1
            )

        reflect_d = obj.material.reflect(ray_d, normal)
        reflect_color = cast_ray(
            ray_o, reflect_d, objects, lights, settings, max_depth - 1
        )

        hit_color += refract_color * refract_k + reflect_color * (1 - refract_k)

    return hit_color


def render(
    camera: Vec3,
    objects: List[Object],
    lights: List[Light],
    settings: Settings,
    *,
    anti_aliasing: int = 1,
    recursion_depth: int = 5,
) -> List[List[Vec3]]:
    # todo: add asserts

    fov = math.radians(settings.fov)
    img_res = settings.resolution
    world_res_w = 2 * settings.distance_to_image * math.tan(fov / 2)
    world_res = Resolution(world_res_w, world_res_w * img_res.h / img_res.w)
    cell_size = world_res.w / img_res.w

    if not (isinstance(img_res.w, int) and isinstance(img_res.h, int)):
        sys.stderr.write("Image resolution must be integer, casting to int\n")
        img_res.w, img_res.h = int(img_res.w), int(img_res.h)
    image = [[Vec3(0, 0, 0) for _ in range(img_res.w)] for _ in range(img_res.h)]

    AA = anti_aliasing

    new_objects: List[Object] = []
    for obj in objects:
        if isinstance(obj, Mesh):
            new_objects.extend(obj.triangles)
        else:
            new_objects.append(obj)
    objects = new_objects

    for i, j in itertools.product(range(img_res.h), range(img_res.w)):
        for a_i, a_j in itertools.product(range(AA), range(AA)):
            p2 = Vec3(
                camera.x + settings.distance_to_image,
                (img_res.h - i) * cell_size
                + (cell_size / AA) * (a_i + 0.5)
                - world_res.h / 2,
                j * cell_size + (cell_size / AA) * (a_j + 0.5) - world_res.w / 2,
            )
            ray_d = p2 - camera

            image[i][j] += cast_ray(
                camera, ray_d, objects, lights, settings, recursion_depth
            )
        image[i][j] /= AA**2

    return image
