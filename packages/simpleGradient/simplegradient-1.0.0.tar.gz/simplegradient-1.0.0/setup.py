from setuptools import setup, find_packages
import codecs
import os
VERSION = '1.0.0'
DESCRIPTION = 'A simple package to create Gradients'
LONG_DESCRIPTION = 'A package that allows to build simple or complex gradients'

# Setting up
setup(
    name="simpleGradient",
    version=VERSION,
    author="Kaiser Fechner",
    author_email="<coolpotatorocks@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'gradients', 'colors'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
