import os
from ast import parse
import setuptools

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open(os.path.join('pyfortracc', '_version.py')) as f:
    version_line = next(filter(lambda line: line.startswith('__version__'), f))
    parsed_version = parse(version_line)
    __version__ = parsed_version.body[0].value.s

setuptools.setup(
    name="pyfortracc",
    version=__version__,
    author="Helvecio B. L. Neto, Alan J. P. Calheiros",
    author_email="fortraccproject@gmail.com",
    description="A Python package for track and forecasting.",
    long_description=open("README.md").read(),
    # long_description_content_type="text/x-rst", # For RST
    long_description_content_type="text/markdown", # For MD
    url="https://github.com/fortracc-project/pyfortracc",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    license="LICENSE",
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Hydrology",
    ]
)
