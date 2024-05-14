# -*- coding: utf-8 -*-

from setuptools import setup
from codecs import open
from os import path
import configparser

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read version from hystfit/data/system.ini

inifile = configparser.ConfigParser()
inifile.read(path.join(here, 'hystfit/data/system.ini'))
version = inifile.get('system', 'version')

setup(
    name='hystfit',
    version=version,
    description='Fit soil water retention curve with hysteresis',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://sekika.github.io/hystfit/',
    author='Katsutoshi Seki',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Environment :: Console',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: Microsoft :: Windows :: Windows 11',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: BSD',
        'Operating System :: POSIX :: Linux',
        'Topic :: Scientific/Engineering :: Hydrology',
        'Natural Language :: English',
    ],
    keywords='soil',
    packages=['hystfit'],
    package_data={'hystfit': ['data/*']},
    install_requires=['unsatfit'],
    python_requires=">=3.10",
)
