import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import supershape as sshape
import numpy as np

# Create shape
shape=(50,50)

with np.errstate(divide='raise'):
    for i in range(500000):
        params = np.random.uniform(
            low =[0.00,1,1,0.0,0.0, 0.0],
            high=[20.00,1,1,40,10.0,10.0],
            size=(2,6)
        ).astype(np.float32)
        print(params)
        x,y,z = sshape.supercoords(params, shape=shape)


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