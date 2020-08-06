# supershape
Python code to efficiently generate  [3D SuperShapes](https://en.wikipedia.org/wiki/Superformula). Comes with additional support for Blender mesh generation.

3D SuperShapes are a family of parametric surfaces that can take on a variety of shapes depending on the parametrization. The following snippet creates 3D coordinates of a flower-like object
```python
import supershape as sshape

x,y,z = sshape.supercoords(
    # m, a, b, n1, n2, n3
    [7, 1, 1, 0.2, 1.7, 1.7], 
    # u,v resolution
    shape=(50,50)
)
```

<p align="center">
  <img  src="etc/flower.png">
</p>

To reproduce the above result, run
```
python -m supershape
```

### Blender support
Launch Blender (>=v2.8) as follows
```
blender --python-use-system-env --python scripts\blender_demo.py
```
to get 
<p align="center">
  <img  src="etc/flower_blender.png">
</p>