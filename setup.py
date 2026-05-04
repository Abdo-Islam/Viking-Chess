from setuptools import setup, find_packages

def read_requirements():
    with open('requirements.txt') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="viking",
    version="0.2.0",
    packages=find_packages(),
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "viking=src.gui:main",
        ],
    },
    description="A Python implementation of the Viking Chess game, also known as Hnefatafl.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AbdoIslam/Viking-Chess",
    python_requires=">=3.6",
) 

