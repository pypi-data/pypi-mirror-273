#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='strainchoosr',
    version='0.1.4',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'strainchoosr = strainchoosr.strainchoosr:main',
            'strainchoosr_gui = strainchoosr.strainchoosr_gui:main',
            'strainchoosr_drawimage = strainchoosr.strainchoosr_gui: \
                draw_image_wrapper'
        ],
    },
    author='Andrew Low',
    author_email='andrew.low@canada.ca',
    url='https://github.com/lowandrew/StrainChoosr',
    tests_require=['pytest'],
    install_requires=['pytest',
                      'ete3',
                      # Required by ete3 for visualisation, but not listed
                      'PyQt5==5.15.10',
                      ]
)
