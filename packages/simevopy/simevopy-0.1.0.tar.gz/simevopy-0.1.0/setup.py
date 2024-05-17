from skbuild import setup
from setuptools import find_packages

setup(
    name="simevopy",
    version="0.1.0",
    description="SimEvo Python bindings",
    packages=find_packages(),
    cmake_source_dir=".",
    url='https://github.com/YJack0000/SimEvo',
    author='YJack0000',
    author_email='yjack0000.cs12@nycu.edu.tw',
    license='MIT',
)
