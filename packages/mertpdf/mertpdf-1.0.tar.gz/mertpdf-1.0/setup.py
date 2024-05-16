import setuptools
from pathlib import Path

setuptools.setup(
    name="mertpdf",
    version=1.0,
    long_description=Path("README.md").read_text(),
    # this method will look at our project
    # and autmatically discover the packages we have defined
    # but it needs to exclude two directories - tests and data
    # because they do not include source code
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
