import time
from random import seed, uniform

from raytracer import render
from raytracer.lights import DirectionalLight
from raytracer.linalg import Vec3
from raytracer.materials import Diffuse, ReflectRefract
from raytracer.materials.reflect import Reflect
from raytracer.objects import Sphere
from raytracer.options import Resolution, Settings
from raytracer.visualize import save_png

seed(123)

settings = Settings(
    background_color=Vec3.from_rgb(255, 252, 222),
    resolution=Resolution(w=1600, h=900),
    distance_to_image=1,
    fov=70,
    bias=1e-4,
)

objects = [Sphere(Vec3(0, -1000, 0), 1000, Diffuse(Vec3.from_rgb(123, 201, 255)))]
num_objects = 10
for i in range(num_objects):
    radius = uniform(1, 5)
    origin = Vec3(
        uniform(-10, 10),
        radius,
        uniform(-10, 10),
    )

    # make sure new sphere is not inside any other ones
    for prev in objects:
        distance = origin.distance(prev.origin)
        if distance < radius + prev.radius:
            break
    else:
        if uniform(0, 1) < 0.5:
            color = Vec3.from_rgb(*[uniform(0, 255) for _ in range(3)])
            material = Diffuse(color)
        else:
            material = ReflectRefract(1.52)
            # material = Reflect()
        objects.append(Sphere(origin, radius, material))

lights = [
    DirectionalLight(Vec3(0.5, -0.5, 0.5), Vec3.from_rgb(255, 255, 255), 1),
    DirectionalLight(Vec3(-0.5, -0.5, -0.5), Vec3.from_rgb(255, 255, 255), 1),
]

look_from = Vec3(20, 7, -5)
look_at = Vec3(0, 1, 0)

start = time.time()
image = render(
    look_from, look_at, objects, lights, settings, anti_aliasing=2, recursion_depth=10
)
print(f"Rendered in {time.time() - start:.2f} seconds")

save_png(image, "examples/many-balls/image.png")
print("Image saved to examples/many-balls/image.png")
