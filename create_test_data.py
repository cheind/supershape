import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import supershape as sshape
import numpy as np
from pathlib import Path

# Create shape
SHAPE = (50, 50)
BASEDIR = Path(__file__).parent


def render_shape(x, y, z, name):
    # Plot it
    fig = plt.figure(figsize=(6, 6), frameon=False)
    ax = fig.add_axes([0, 0, 1, 1], projection='3d')
    ax.set_title(name)
    ax.plot_surface(
        x, y, z,
        cmap='viridis',
        edgecolors='k',
        linewidth=0.5,
        rcount=SHAPE[0], ccount=SHAPE[1])
    plt.axis('off')
    plt.grid(b=None)
    plt.show()


def create_shape(params, name, visualize=True):
    with np.errstate(divide='raise'):
        x, y, z = sshape.supercoords(params, shape=SHAPE)
    if visualize:
        render_shape(x, y, z, name)
    np.save(BASEDIR / 'data' / f'{name}.npy', np.stack((x, y, z), 0))


def main(visualize=True):
    create_shape(sshape.CONE, 'cone', visualize=visualize)
    create_shape(sshape.FLOWER, 'flower', visualize=visualize)
    create_shape(sshape.ROUNDCUBE, 'roundcube', visualize=visualize)
    create_shape(sshape.SPHERE, 'sphere', visualize=visualize)


if __name__ == '__main__':
    main()
