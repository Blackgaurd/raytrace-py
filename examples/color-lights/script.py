import time

from raytracer import render
from raytracer.lights import PointLight
from raytracer.linalg import Vec3
from raytracer.materials import Diffuse
from raytracer.objects import Sphere, Triangle
from raytracer.options import Resolution, Settings
from raytracer.visualize import save_png

settings = Settings(Vec3.from_rgb(66, 66, 66), Resolution(w=1920, h=1080), 1, 70, 0.01)
objects = [
    Triangle(
        Vec3(-10, -2, -10),
        Vec3(10, -2, -10),
        Vec3(-10, -2, 10),
        Diffuse(Vec3.from_rgb(255, 255, 255)),
    ),
    Triangle(
        Vec3(10, -2, -10),
        Vec3(10, -2, 10),
        Vec3(-10, -2, 10),
        Diffuse(Vec3.from_rgb(255, 255, 255)),
    ),
    Sphere(Vec3(0, 0, 0), 2, Diffuse(Vec3.from_rgb(255, 255, 255))),
]
lights = [
    PointLight(Vec3(-5, 0, -5), Vec3.from_rgb(255, 0, 0), 1),
    PointLight(Vec3(-5, 0, 3), Vec3.from_rgb(0, 255, 0), 1),
    PointLight(Vec3(-4, 3, 0), Vec3.from_rgb(0, 0, 255), 0.5),
]

look_from = Vec3(-10, 0, 0)
look_at = Vec3(-9, 0, 0)

start = time.time()
image = render(
    look_from, look_at, objects, lights, settings, anti_aliasing=2, recursion_depth=10
)
print(f"Rendered in {time.time() - start:.2f} seconds")

save_png(image, "examples/color-lights/image.png")
print("Image saved to examples/color-lights/image.png")
