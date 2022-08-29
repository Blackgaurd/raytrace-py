from raytracer.lights import DirectionalLight
from raytracer.materials import Diffuse, Reflect
from raytracer.objects import Sphere, Triangle
from raytracer.options import Resolution, Settings
from raytracer.render import render
from raytracer.linalg import Vec3
from raytracer.visualize import save_png

settings = Settings(
    Vec3.from_rgb(184, 255, 217), Resolution(w=1920, h=1080), 1, 70, 0.01
)
camera = Vec3(-10, 0, 0)
objects = [
    Triangle(Vec3(-10, -2, -10), Vec3(10, -2, -10), Vec3(-10, -2, 10), Reflect()),
    Triangle(Vec3(10, -2, -10), Vec3(-10, -2, 10), Vec3(10, -2, 10), Reflect()),
    Sphere(Vec3(2, 0, -7.5), 1, Diffuse(Vec3.from_rgb(255, 0, 0))),  # red
    Sphere(Vec3(3, 0, -5), 1, Diffuse(Vec3.from_rgb(255, 127, 0))),  # orange
    Sphere(Vec3(4, 0, -2.5), 1, Diffuse(Vec3.from_rgb(255, 255, 0))),  # yellow
    Sphere(Vec3(5, 0, 0), 1, Diffuse(Vec3.from_rgb(0, 255, 0))),  # green
    Sphere(Vec3(4, 0, 2.5), 1, Diffuse(Vec3.from_rgb(0, 0, 255))),  # blue
    Sphere(Vec3(3, 0, 5), 1, Diffuse(Vec3.from_rgb(75, 0, 130))),  # violet
    Sphere(Vec3(2, 0, 7.5), 1, Diffuse(Vec3.from_rgb(148, 0, 211))),  # indigo
    Sphere(Vec3(8, 4, 0), 2, Reflect()),  # mirror
]
lights = [
    DirectionalLight(Vec3(-1, -1, -0.9), Vec3(1, 1, 1), 1),
    DirectionalLight(Vec3(1, -0.3, 1), Vec3(1, 1, 1), 1),
]
image = render(camera, objects, lights, settings, anti_aliasing=2, recursion_depth=10)
save_png(image, "examples/rainbow/image.png")
print("Image saved to examples/rainbow/image.png")
