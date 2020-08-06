import bpy
import supershape as sshape

# Remove default cube
bpy.data.objects.remove(bpy.data.objects['Cube'], do_unlink=True)

# Generate mesh
shape=(100,100)
x,y,z = sshape.supercoords(sshape.FLOWER, shape=shape)
obj = sshape.make_bpy_mesh(x,y,z)