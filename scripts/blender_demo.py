import bpy
import supershape as sshape

# Remove default cube
bpy.data.objects.remove(bpy.data.objects['Cube'], do_unlink=True)

# Generate mesh
shape=(100,100)
obj = sshape.make_bpy_mesh(shape)
x,y,z = sshape.supercoords(sshape.SPHERE, shape=shape)
sshape.update_bpy_mesh(x, y, z, obj)
