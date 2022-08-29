# Ray tracing in python

Very few optimizations were made other than algorithm specific. This is because if I wanted something faster I wouldn't have used python. This is more of a learning resource than anything else.

The source code is 100% type hinted, so the module can be compiled with mypy using the following command:

```bash
mypyc raytracer/
```

This yields about ~2x speed boost.

## Demonstrations

![rainbow](examples/rainbow/image.png)
