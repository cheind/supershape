from setuptools import setup
from pathlib import Path

THISDIR = Path(__file__).parent

with open(THISDIR/'README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='supershape',
    author='Christoph Heindl',
    description='Python code to efficiently generate 3D supershapes with optional Blender support.',
    url='https://github.com/cheind/supershape',
    packages=['supershape'],
    version=open(THISDIR/'supershape' /
                 '__init__.py').readlines()[-1].split()[-1].strip('\''),
    install_requires=['numpy'],
    long_description=long_description,
    long_description_content_type='text/markdown',
)
