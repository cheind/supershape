import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import supershape as sshape

# Create shape
shape=(50,50)
x,y,z = sshape.supercoords(sshape.FLOWER, shape=shape)

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