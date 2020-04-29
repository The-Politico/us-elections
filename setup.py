# Imports from python.
import os
from setuptools import find_packages
from setuptools import setup


# Imports from us-elections.
from elections import __appname__, __version__


REPO_URL = "https://github.com/The-Politico/us-elections/"

PYPI_VERSION = ".".join(str(v) for v in __version__)

with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

setup(
    name=__appname__,
    version=PYPI_VERSION,
    packages=find_packages(exclude=["db", "docs", "tests"]),
    license="MIT",
    description="U.S. election and government metadata",
    long_description=README,
    long_description_content_type="text/markdown",
    url=REPO_URL,
    download_url="{repo_url}archive/{version}.tar.gz".format(
        **{"repo_url": REPO_URL, "version": PYPI_VERSION}
    ),
    author="POLITICO Interactive News",
    author_email="interactives@politico.com",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet :: WWW/HTTP",
    ],
    keywords="",
    platforms=["any"],
    package_data={"elections": ["data/**/*.pkl", "data/*.pkl"]},
    include_package_data=True,
    install_requires=["us>=1,<2"],
    zip_safe=False,
    extras_require={"test": ["pytest"]},
)
