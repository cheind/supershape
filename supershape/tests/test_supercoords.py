from pathlib import Path
import numpy as np
import supershape as sshape

SHAPE = (50, 50)
MODELS = [
    (sshape.FLOWER, 'flower.npy'),
    (sshape.SPHERE, 'sphere.npy'),
    (sshape.CONE, 'cone.npy'),
    (sshape.ROUNDCUBE, 'roundcube.npy'),
]
DATADIR = Path(__file__).parent.parent.parent/'data'
assert DATADIR.exists(), 'Data directory not found.'


def compare(model):
    reference = np.load(DATADIR/model[1])
    actual = np.stack(sshape.supercoords(model[0], shape=SHAPE), 0)
    if not np.allclose(actual, reference, atol=1e-3):
        assert False, f'Coordinate comparison for model {model[1]} failed.'


def test_reference_models():
    [compare(m) for m in MODELS]
