from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="quantumvista",
    version="1.0.0",
    author="Hemorra",
    author_email="blestduck24@proton.me",
    description="A Python package for quantum computing concepts and algorithms.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/nebula",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)