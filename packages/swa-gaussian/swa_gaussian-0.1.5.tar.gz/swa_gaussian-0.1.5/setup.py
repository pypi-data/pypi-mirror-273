from setuptools import find_packages, setup
import os
import sys

_here = os.path.abspath(os.path.dirname(__file__))

if sys.version_info[0] < 3:
    with open(os.path.join(_here, "README.rst")) as f:
        long_description = f.read()
else:
    with open(os.path.join(_here, "README.rst"), encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="swa_gaussian",
    description=("SWA-Gaussian repo"),
    long_description=long_description,
    author="Wesley Maddox, Timur Garipov, Pavel Izmailov, Dmitry Vetrov, Andrew Gordon Wilson",
    author_email="wm326@cornell.edu",
    url="https://github.com/Helsinki-NLP/swa_gaussian",
    maintainer="Sami Virpioja",
    maintainer_email="sami.virpioja@helsinki.fi",
    license="BSD",
    packages=find_packages(include=["swag", "swag.*"]),
    install_requires=[
        "tqdm>=4.26.0",
        "numpy>=1.14.3",
        "torchvision>=0.2.1",
        "gpytorch>=0.1.0rc4",
        "tabulate>=0.8.2",
        "scipy>=1.1.0",
        "setuptools>=39.1.0",
        "matplotlib>=2.2.2",
        "torch>=1.0.0",
        "Pillow>=5.4.1",
        "scikit_learn>=0.20.2",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.6",
    ],
    python_requires=">=3.6",
    use_scm_version=True
)
