import setuptools
from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("c_is_alone.pyx"),
)

setup(
    ext_modules=cythonize("c_possible_moves.pyx"),
)

setup(
    ext_modules=cythonize("c_win_tower.pyx"),
)