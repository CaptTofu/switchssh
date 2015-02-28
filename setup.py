from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

# chardet's setup.py
setup(
    name = "switchssh",
    version = "0.2.0",
    description = "Python Switch SSH Library",
    long_description="Simple Paramiko-based library making interacting with Switches simple",

    author = "Patrick Galbraith",
    author_email = "patg@hp.com",

    # Choose your license
    license='Apache',

    url = "http://patg.net/",
    download_url = "http://tbd.tgz",
    keywords = ["Comware", "Pro Vision", "hp switches", "ansible"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Development Status :: 3 - Alpha",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Network :: Switches",
        ],

    packages=find_packages(exclude=['bin']),

    install_requires=['paramiko'],

    entry_points={
        'console_scripts': [
            'switchssh=switchssh:main',
        ],
        },
)
