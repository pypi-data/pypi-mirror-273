from setuptools import setup
import urllib.request
from zipfile import ZipFile
from pathlib import Path
DOC = ""

Path("wgse/third_party").mkdir(parents=True, exist_ok=True)
Path("wgse/third_party/__init__.py").touch(exist_ok=True)

urllib.request.urlretrieve("https://github.com/WGSE-NG/External/releases/download/v0.0.1/third_party-1.0.0.zip", "third_party.zip")
with ZipFile("third_party.zip", "r") as f:
    f.extractall(Path("wgse/third_party"))

setup(
    name="WGSE-NG-3rd-party",
    packages=["wgse.third_party"],
    author="Multiple",
    author_email="",
    include_package_data=True,
    description="Whole Genome Sequencing data manipulation tool",
    long_description="Whole Genome Sequencing data manipulation tool",
    install_requires=[],
    url="https://github.com/chaplin89/WGSE-NG",
    version="0.0.1",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    keywords="bioinformatics",
)
