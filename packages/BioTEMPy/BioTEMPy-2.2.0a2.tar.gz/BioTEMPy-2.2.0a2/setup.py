
import os
import setuptools
import shutil
import sys
from distutils.core import setup

if os.path.exists('build') is True:
    print('build exists')
    shutil.rmtree('./build')

setup(
    name='BioTEMPy',
    version='2.2.0a2',
    author='Maya Topf, Daven Vasishtan, Arun Prasad Pandurangan, Irene Farabella, Agnel-Praveen Joseph, Harpal Sahota',
    author_email='tempy-help@cryst.bbk.ac.uk',
    packages=setuptools.find_packages(),
    url='http://tempy.ismb.lon.ac.uk/',
    description='TEMPy: a Python Library for Assessment of 3D Electron Microscopy Density Fits',
    package_dir={'TEMPy': 'TEMPy'},
    python_requires='>=3.7',
    install_requires=[
        'numpy>=1.16.1',
        'scipy>=1.7.0',
        'matplotlib',
        'gemmi>=0.5.6',
        'voxcov>=0.2.7',
        'mrcfile',
        'pyfftw',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_data={'TEMPy': ['tempy_data/*.pk']},
    entry_points = {
        'console_scripts': ['TEMPy.smoc=TEMPy.script.smoc:main',
                            'TEMPy.gamma=TEMPy.script.gamma:main',
                            'TEMPy.loqfit=TEMPy.script.loqfit:main',
                            'TEMPy.sccc=TEMPy.script.sccc:main',
                            'TEMPy.scores=TEMPy.script.scores:main']
    }
)
