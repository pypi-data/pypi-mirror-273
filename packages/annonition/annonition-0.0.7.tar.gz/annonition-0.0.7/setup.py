from setuptools import setup, find_packages
from os import path
working_dir = path.abspath(path.dirname(__file__))

with open(path.join(working_dir, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="annonition",
    version="0.0.7",
    author="Abtin Turing",
    author_email="abtinturing@gmail.com",
    description="Beginning of a new era in annotation tools.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/abtinturing/anno",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "coloredlogs",
        "verboselogs"
    ]
)