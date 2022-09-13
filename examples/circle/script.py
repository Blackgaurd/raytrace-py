import math
import time

from raytracer import render
from raytracer.lights import PointLight
from raytracer.linalg import Vec3
from raytracer.materials import Diffuse
from raytracer.objects import Sphere, Mesh
from raytracer.options import Resolution, Settings
from raytracer.visualize import save_png

settings = Settings(
    background_color=Vec3.from_rgb(30, 198, 167),
    resolution=Resolution(w=1600, h=900),
    distance_to_image=1,
    fov=70,
    bias=1e-4,
)

sphere_color = Diffuse(Vec3.from_rgb(255, 255, 255))
objects = [
    Sphere(Vec3(0, -10000, 0), 10000, Diffuse(Vec3.from_rgb(200, 200, 200))),  # floor
    Sphere(Vec3(-5, 1, 0), 1, sphere_color),
    Sphere(Vec3(5, 1, 0), 1, sphere_color),
    Mesh.from_obj("models/cube.obj", sphere_color, translate=Vec3(-2.5, 1, 2.5 * math.sqrt(3))),
    Sphere(Vec3(2.5, 1, -2.5 * math.sqrt(3)), 1, sphere_color),
    Sphere(Vec3(-2.5, 1, -2.5 * math.sqrt(3)), 1, sphere_color),
    Sphere(Vec3(2.5, 1, 2.5 * math.sqrt(3)), 1, sphere_color),
]

lights = [PointLight(Vec3(0, 3, 0), Vec3.from_rgb(125, 80, 255), 1)]

look_from = Vec3(-12, 5, 3)
look_at = Vec3(0, 1, 0)

start = time.time()
image = render(
    look_from, look_at, objects, lights, settings, anti_aliasing=2, recursion_depth=10
)
print(f"Rendered in {time.time() - start:.2f} seconds")

save_png(image, "examples/circle/image.png")
print("Image saved to examples/circle/image.png")
