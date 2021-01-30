import bpy
import supershape as sshape

# Remove default cube
bpy.data.objects.remove(bpy.data.objects['Cube'], do_unlink=True)

# Generate supershape
shape = (100, 100)
obj = sshape.make_bpy_mesh(shape, weld=True)
x, y, z = sshape.supercoords(sshape.FLOWER, shape=shape)
sshape.update_bpy_mesh(x, y, z, obj)
