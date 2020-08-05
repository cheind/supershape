'''Python code to compute 3D parametric SuperShapes 
Additional Blender mesh generation support.
https://github.com/cheind/supershape

For an explanation of Supershapes, see
http://paulbourke.net/geometry/supershape/
https://en.wikipedia.org/wiki/Superformula
'''

import numpy as np

'''Predefined params of a sphere'''
SPHERE = [0.01, 1., 1., 0.1, 0.01, 10.0]
'''Predefined params of round cube'''
ROUNDCUBE = [4, 1., 1., 10., 10., 10.]
'''Predefined params of a flower-like object'''
FLOWER = [7, 1, 1, 0.2, 1.7, 1.7]
'''Predefined params of a cone-like object'''
CONE = [[4, 1, 1, 100, 1, 1],[4, 1, 1, 1, 1, 1]]

def create3d(params, shape=(50,50)):
    '''Returns coordinates of a parametrized 3D supershape.
    
    See
    http://paulbourke.net/geometry/supershape/
    https://en.wikipedia.org/wiki/Superformula

    Params
    ------
    params: 1x6 or 2x6 array
        Parameters of the two supershapes. If 1x6 the same
        parameters will be used for the second supershape.
        The order of the parameters is as follows:
        m: float
            long/lat frequency.
            Defaults to 0.01
        a: float
            long/lat inverse amplitude of first term.
            Defaults to 1.
        b: float
            long/lat inverse amplitude of second term
            Defaults to 1.
        n1: float
            First exponent. Defaults to 0.1
        n2: float
            Second exponent. Defaults to 0.01
        n3: float
            Third exponent. Actually (-1/n3). Defaults to 10.0
    shape : tuple
        longitude/latitude resolution (U,V)

    Returns
    -------
    x: UxV array
        x coordinates for each long/lat point
    y: UxV array
        y coordinates for each long/lat point
    z: UxV array
        z coordinates for each long/lat point
    '''

    params = np.atleast_2d(params)
    if params.shape[0] == 1:
        params = np.tile(params, (2,1))

    sf = lambda alpha, sp: (
        np.abs(np.cos(sp[0]*alpha/4.)/sp[1])**sp[4] + 
        np.abs(np.sin(sp[0]*alpha/4.)/sp[2])**sp[5]
    )**(-1/sp[3])

    u = np.linspace(-np.pi, np.pi, shape[0])     # long, theta
    v = np.linspace(-np.pi/2, np.pi/2, shape[1]) # lat, phi
        
    g = np.meshgrid(v, u)
    uv = np.stack((g[1],g[0]),-1)
    r1 = sf(uv[...,0], params[0])
    r2 = sf(uv[...,1], params[1])    

    x = r1 * np.cos(u)[:,None] * r2 * np.cos(v)[None, :]
    y = r1 * np.sin(u)[:,None] * r2 * np.cos(v)[None, :]
    z = r2 * np.sin(v)[None, :]

    return x,y,z

def bpy_mesh(x,y,z, obj=None):
    '''Create or update a Blender (>2.8) mesh from supershape coordinates.

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
    
    Returns
    -------
    obj: bpy.types.Object
        Mesh object build from quads.
    '''
    import bpy 
    import bmesh
    # create quads
    U,V = x.shape
    if obj is None:
        faces = []
        for u in range(U-1):
            for v in range(V-1):
                A = u*V + v
                B = u*V + (v+1)
                C = (u+1)*V + (v+1)
                D = (u+1)*V + v
                faces.append((A,B,C,D))
        verts = np.stack((x,y,z), -1).reshape(-1, 3)
        mesh = bpy.data.meshes.new('supershape')
        mesh.from_pydata(verts.tolist(), [], faces)
        mesh.update(calc_edges=True)
        obj = bpy.data.objects.new('supershape', mesh)
        bpy.context.collection.objects.link(obj)
        for p in mesh.polygons:
            p.use_smooth = True
        return obj
    else:             
        x = x.reshape(-1)
        y = y.reshape(-1)
        z = z.reshape(-1)   
        for idx, v in enumerate(obj.data.vertices):
            v.co = (x[idx], y[idx], z[idx])
        
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(obj.data)
        bm.clear()
        obj.data.update()
        bm.free()
        
def plain_main():
    '''Entry point for visualization without Blender'''
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    # Create shape
    shape=(50,50)
    x,y,z = create3d(FLOWER, shape=shape)

    # Plot it
    fig = plt.figure(figsize=(6,6), frameon=False)
    ax = fig.add_axes([0,0,1,1],projection='3d')
    ax.plot_surface(
        x,y,z, 
        cmap='viridis', 
        edgecolors='k',
        linewidth=0.5,
        rcount=shape[0], ccount=shape[1])
    plt.axis('off')
    plt.grid(b=None)    
    plt.show()

def main_bpy():
    '''Entry point for visualization in Blender'''

    # Create shape
    shape=(100, 100)
    x,y,z = create3d(FLOWER, shape=shape)

    # Create mesh and show
    obj = bpy_mesh(x,y,z)

if __name__ == '__main__':
    try:
        import bpy
        main_bpy()
    except ModuleNotFoundError:
        plain_main()