from setuptools import setup, find_packages
import os

def get_requirements(file_name: str) -> list:
    with open(file_name, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('-e')]

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="mongodb_connect",
    version="0.0.4",
    author="akinolanath5519",
    author_email="akinolanathaniel3026@gmail.com",
    description="A python package for connecting with MongoDB database.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/akinolanath5519/MlopsMangoDBpackage",
    project_urls={
        "Bug Tracker": "https://github.com/akinolanath5519/MlopsMangoDBpackage/issues",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=get_requirements("requirements.txt"),
    extras_require={
        'dev': get_requirements('requirements_dev.txt')
    }
)
