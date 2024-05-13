from setuptools import find_packages
from setuptools import setup

setup(
    name='pandisplay',
    version='1.0.0',
    packages=find_packages(),
    description='Pandas display methods for DataFrame visualization in Jupyter Notebooks.',
    author='bkitej',
    install_requires=[
        'pandas',
        'ipython'
    ],
)
