from setuptools import setup, find_packages

setup(
    name="edudat",
    version="0.001",
    packages=["edudat"],
    install_requires=[
        "pandas",
        "requests",
    ],
    author="Oliver Dürr",
    description="A package for educational datasets",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/tensorchiefs/data",
)
