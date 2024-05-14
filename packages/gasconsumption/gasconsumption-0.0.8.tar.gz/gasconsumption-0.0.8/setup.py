from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.8'
DESCRIPTION = 'Wrap an api that can fitch Deftable and timeseries table to make it more convenient. '
LONG_DESCRIPTION = 'contain an api wrapper that helps to fetch gas cconsumption data.'

# Setting up
setup(
    name="gasconsumption",
    version=VERSION,
    author="Ahmad Riad",
    author_email="meuralengine@outlook.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description= LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas','requests'],
    keywords=['python', 'Deftable', 'timeseries'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)