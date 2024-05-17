#!/usr/bin/env python

from setuptools import setup, find_packages

# Read the contents of the README file
with open('README.rst', 'r') as f:
    long_description = f.read()


# Open the requirements.txt file
with open('requirements.txt') as f:
    # Read the file and split it into lines
    # Each line should be a separate requirement
    requirements = f.read().splitlines()

setup(
    name='strainchoosr',
    version='0.1.6',
    packages=find_packages(),
    description='This package was originally created by Andrew Low. Now maintained by Adam Koziol.',
    long_description=long_description,
    # The content type of the long description. Necessary for PyPI
    entry_points={
        'console_scripts': [
            'strainchoosr = strainchoosr.strainchoosr:main',
            'strainchoosr_gui = strainchoosr.strainchoosr_gui:main',
            'strainchoosr_drawimage = strainchoosr.strainchoosr_gui:draw_image_wrapper'
        ],
    },
    author='Adam Koziol',
    author_email='adam.koziol@inspection.gc.ca',
    url='https://github.com/OLC-Bioinformatics/StrainChoosr',
    tests_require=['pytest'],
    install_requires=requirements
)
