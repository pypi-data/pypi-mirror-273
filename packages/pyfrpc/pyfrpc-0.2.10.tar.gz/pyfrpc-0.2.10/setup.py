import os

from Cython.Build import cythonize
from setuptools import setup

PYFRPC_NOEXT = bool(int(os.environ.get('PYFRPC_NOEXT', '0')))


setup_args = dict()

if not PYFRPC_NOEXT:
    setup_args['ext_modules'] = cythonize(['src/pyfrpc/_coding_base_c.pyx'])


if __name__ == "__main__":
    setup(**setup_args)
