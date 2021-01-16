from __future__ import absolute_import
from __future__ import print_function

import io
from os import path
import os
import re
import sys
import platform
import subprocess

from setuptools import setup, Extension
from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools.command.build_ext import build_ext
from distutils.version import LooseVersion

here = path.abspath(path.dirname(__file__))


def read(*names, **kwargs):
    return io.open(path.join(here, *names), encoding=kwargs.get('encoding', 'utf8')).read()


class CMakeExtension(Extension):

    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):

    def run(self):
        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError("CMake must be installed to build the following extensions: " + ", ".join(e.name for e in self.extensions))

        if platform.system() == "Windows":
            cmake_version = LooseVersion(re.search(r'version\s*([\d.]+)', out.decode()).group(1))
            if cmake_version < '3.1.0':
                raise RuntimeError("CMake >= 3.1.0 is required on Windows")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        cmake_args = [
            '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,
            '-DPYTHON_EXECUTABLE=' + sys.executable]

        cfg = 'Debug' if self.debug else 'Release'
        build_args = ['--config', cfg]

        if platform.system() == "Windows":
            cmake_args += ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(cfg.upper(), extdir)]
            if sys.maxsize > 2**32:
                cmake_args += ['-A', 'x64']
            # build_args += ['--', '/m']
        else:
            # # For MacOS.
            # # During compiling stage, the python module always links to a temporary generated library which is going to be destroyed.
            # # Then importing the final installed module will return a link error
            # # The following commands will force the module to look up the its dynmaic linked library in the same folder
            # cmake_args += [
            #     '-DCMAKE_INSTALL_RPATH=@loader_path',
            #     '-DCMAKE_BUILD_WITH_INSTALL_RPATH:BOOL=ON',
            #     '-DCMAKE_INSTALL_RPATH_USE_LINK_PATH:BOOL=OFF']

            cmake_args += ['-DCMAKE_BUILD_TYPE=' + cfg]
            cmake_args += ['-DLIBIGL_INCLUDE_DIR=../../ext/libigl/include'] 
            build_args += ['--', '-j2']


        env = os.environ.copy()
        env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(env.get('CXXFLAGS', ''), self.distribution.get_version())
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        subprocess.check_call(['cmake', ext.sourcedir] + cmake_args, cwd=self.build_temp, env=env)
        subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd=self.build_temp)


long_description = read('README.md')
requirements = read('requirements.txt').split('\n')
optional_requirements = {}


setup(
    name='compas_libigl',
    version='0.1.0',
    description='Opinionated COMPAS compatible bindings for top-level algorithms of libigl.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/BlockResearchGroup/compas_libigl',
    author='Tom Van Mele',
    author_email='van.mele@arch.ethz.ch',
    license='MIT license',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    keywords=[],
    packages=['compas_libigl', ],
    package_dir={'': 'src'},
    project_urls={},
    package_data={},
    data_files=[],
    include_package_data=True,
    zip_safe=False,
    install_requires=requirements,
    python_requires='>=3.6',
    extras_require=optional_requirements,
    ext_modules=[CMakeExtension('compas_libigl')],
    cmdclass=dict(build_ext=CMakeBuild),
)
