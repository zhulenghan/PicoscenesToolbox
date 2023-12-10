#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os

import numpy
from Cython.Build import cythonize
from setuptools import find_packages, setup
from setuptools.command.build_ext import build_ext
from setuptools.extension import Extension


def find_files(root, ext):
    ret = list()
    if os.path.exists(root):
        for file in os.listdir(root):
            if file.endswith(ext):
                ret.append(os.path.join(root, file))
    return ret


EXTENSIONS = []


class Build(build_ext):
    def build_extensions(self):
        if self.compiler.compiler_type in ["msvc"]:
            for e in self.extensions:
                if e.name == "picoscenes":
                    e.extra_compile_args = ['/std:c++latest']
        else:
            for e in self.extensions:
                if e.name == "parsing_core_Float32" or "parsing_core" or "picoscenes":
                    e.extra_compile_args = ['-std=c++2a', '-Wno-attributes',
                                            '-O3']
        super(Build, self).build_extensions()


pico_root = "./rxs_parsing_core"
pico_generated = os.path.join(pico_root, 'preprocess/generated')
pico_include = os.path.join(pico_root, 'preprocess')
pico_source = find_files(pico_root, '.cxx') + find_files(pico_generated, '.cpp')
pico_extension_core = Extension(
    "parsing_core", ["./parsing_core.pyx"] + pico_source,
    include_dirs=[numpy.get_include(), pico_include],
    define_macros=[('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION')],
)
pico_extension_core_Float32 = Extension(
    "parsing_core_Float32", ["./parsing_core_Float32.pyx"] + pico_source,
    include_dirs=[numpy.get_include(), pico_include],
    define_macros=[('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION')],
)
pico_extension = Extension("picoscenes", ["./picoscenes.pyx"])
if os.path.exists(pico_root):
    EXTENSIONS.append(pico_extension_core)
    EXTENSIONS.append(pico_extension_core_Float32)
    EXTENSIONS.append(pico_extension)
setup(
    packages=find_packages(),
    install_requires=['numpy'],
    python_requires='>=3',
    ext_modules=cythonize(
        EXTENSIONS,
        compiler_directives={'language_level': 3, 'binding': False}
    ),
    cmdclass={'build_ext': Build},
    zip_safe=False
)

