"""A setuptools based setup module."""

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="python3-cyberfusion-common",
    version="2.10.11.2",
    description="Common utilities.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.9",
    author="William Edwards",
    author_email="wedwards@cyberfusion.nl",
    url="https://vcs.cyberfusion.nl/shared/python3-cyberfusion-common",
    platforms=["linux"],
    packages=["cyberfusion.Common", "cyberfusion.Common.exceptions"],
    package_dir={"": "src"},
    data_files=[],
    install_requires=[
        "cached_property==1.5.2",
        "psutil==5.8.0",
        "requests==2.25.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["cyberfusion", "common"],
    license="MIT",
)
