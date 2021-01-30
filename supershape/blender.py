import numpy as np
from . import SUPERSHAPE_BLENDER

if SUPERSHAPE_BLENDER:
    import bpy
    import bmesh
    from mathutils import Vector

    def make_bpy_mesh(shape, name='supershape', coll=None, smooth=True, weld=False):
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
        name: str
            Name of object.
        coll: bpy collection
            Collection to link object to. If None,
            default collection is used. If False, object is not
            added to any collection.
        smooth: bool
            Smooth or flat rendering.
        weld: bool, optional
            Whether to add a weld-modifier to the mesh. The weld modifier
            closes geometry seams by merging duplicate vertices. Defaults to
            false.
        '''
        U, V = shape
        xy = np.stack(np.meshgrid(np.linspace(0, 1, V),
                                  np.linspace(0, 1, U)), -1).astype(np.float32)
        vertices = np.concatenate(
            (xy, np.zeros((U, V, 1), dtype=np.float32)), -1).reshape(-1, 3)

        # Vertices
        bm = bmesh.new()
        for v in vertices:
            bm.verts.new(Vector(v))
        # Required after adding / removing vertices and before accessing them by index.
        bm.verts.ensure_lookup_table()
        # Required to actually retrieve the indices later on (or they stay -1).
        bm.verts.index_update()
        # Faces
        for u in range(U-1):
            for v in range(V-1):
                A = u*V + v
                B = u*V + (v+1)
                C = (u+1)*V + (v+1)
                D = (u+1)*V + v
                bm.faces.new((bm.verts[D], bm.verts[C],
                              bm.verts[B], bm.verts[A]))
        # UV
        uv_layer = bm.loops.layers.uv.new()
        for face in bm.faces:
            for loop in face.loops:
                v, u = vertices[loop.vert.index][:2]
                loop[uv_layer].uv = (u, 1.-v)

        bm.normal_update()
        mesh = bpy.data.meshes.new(name)
        bm.to_mesh(mesh)
        bm.free()

        if smooth:
            for f in mesh.polygons:
                f.use_smooth = True

        obj = bpy.data.objects.new(name, mesh)
        del mesh

        if weld:
            mod = obj.modifiers.new("CloseSeams", 'WELD')
            mod.merge_threshold = 1e-3
        if coll is None:
            coll = bpy.context.collection
        if coll is not False:
            coll.objects.link(obj)

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
            Object to update. Note that the long./lat. resolution must match.
        '''
        import bmesh
        x = x.reshape(-1, 1)
        y = y.reshape(-1, 1)
        z = z.reshape(-1, 1)
        flat = np.concatenate((x, y, z), -1)
        obj.data.vertices.foreach_set("co", flat.reshape(-1))

        # Update normals
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        # Instead of closing seams at data level through
        # bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-3)
        # use a weld mesh modifier.
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(obj.data)
        bm.clear()
        obj.data.update()
        bm.free()
        del bm
else:
    def make_bpy_mesh(x, y, z):
        raise ValueError('Not called from within Blender.')

    def update_bpy_mesh(x, y, z, obj):
        raise ValueError('Not called from within Blender.')
