import numpy as np
from . import SUPERSHAPE_BLENDER

if SUPERSHAPE_BLENDER:
    import bpy 
    import bmesh

    def make_bpy_mesh(shape):
        '''Create a Blender (>2.8) mesh from supershape coordinates.

        Adapted from
        http://wiki.theprovingground.org/blender-py-supershape
        
        Params
        ------
        shape : tuple
            long./lat. resolution of supershape
        
        Returns
        -------
        obj: bpy.types.Object
            Mesh object build from quads.
        '''
        U,V = shape
        faces = []
        for u in range(U-1):
            for v in range(V-1):
                A = u*V + v
                B = u*V + (v+1)
                C = (u+1)*V + (v+1)
                D = (u+1)*V + v
                faces.append((A,B,C,D))
        verts = np.zeros((U*V,3), dtype=np.float32)
        mesh = bpy.data.meshes.new('supershape')
        mesh.from_pydata(verts.tolist(), [], faces)
        mesh.update(calc_edges=True)
        obj = bpy.data.objects.new('supershape', mesh)
        bpy.context.collection.objects.link(obj)
        for p in mesh.polygons:
            p.use_smooth = True
        return obj

    def update_bpy_mesh(x, y, z, obj):
        '''Update a Blender (>2.8) mesh from supershape coordinates.

        Adapted from
        http://wiki.theprovingground.org/blender-py-supershape
        
        Params
        ------
        x: UxV array
            x coordinates for each long/lat point
        y: UxV array
            y coordinates for each long/lat point
        z: UxV array
            z coordinates for each long/lat point
        obj: bpy.types.Object
            Optional object to update, instead of creating a new one.
            Note that the long./lat. resolution must match.
        '''
        import bmesh
        x = x.reshape(-1)
        y = y.reshape(-1)
        z = z.reshape(-1)   
        for idx, v in enumerate(obj.data.vertices):
            v.co = (x[idx], y[idx], z[idx])
        
        # Update normals
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(obj.data)
        bm.clear()
        obj.data.update()
        bm.free()
else:
    def make_bpy_mesh(x,y,z):
        raise ValueError('Not called from within Blender.')

    def update_bpy_mesh(x,y,z,obj):
        raise ValueError('Not called from within Blender.')