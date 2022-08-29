from mypyc.build import mypycify
from setuptools import setup

setup(
    name="mypyc_output",
    ext_modules=mypycify(["raytracer"], opt_level="3", debug_level="0"),
)
