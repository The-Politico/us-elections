from setuptools import find_packages, setup

setup(
    name="us-elections",
    version="0.0.3",
    description="US elections metadata",
    url="https://github.com/The-Politico/us-elections",
    author="Jon McClure",
    author_email="interactives@politico.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet :: WWW/HTTP",
    ],
    package_data={"elections": ["data/**/*.pkl", "data/*.pkl"]},
    keywords="",
    packages=find_packages(exclude=["docs", "tests"]),
    install_requires=["us"],
    zip_safe=False,
    extras_require={"test": ["pytest"]},
)
