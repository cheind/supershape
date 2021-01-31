from .supershape import supercoords

try:
    import bpy
    SUPERSHAPE_BLENDER = True
except ModuleNotFoundError as e:
    SUPERSHAPE_BLENDER = False

from .blender import make_bpy_mesh, update_bpy_mesh

'''Predefined params of a sphere'''
SPHERE = [0.01, 1., 1., 0.1, 0.01, 10.0]
'''Predefined params of round cube'''
ROUNDCUBE = [4, 1., 1., 10., 10., 10.]
'''Predefined params of a flower-like object'''
FLOWER = [7, 1, 1, 0.2, 1.7, 1.7]
'''Predefined params of a cone-like object'''
CONE = [[4, 1, 1, 100, 1, 1], [4, 1, 1, 1, 1, 1]]

__VERSION__ = '1.1.1'
