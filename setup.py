"""
OCTO-AGI-DEMO: Unified Artificial Consciousness System
Integrating UMG, Tetrahedral Spatial Reasoning, and Deschooling Philosophy
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="octo-agi",
    version="1.0.0",
    author="OCTO-AGI Team",
    description="Breakthrough in unified artificial consciousness",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GitMonsters/OCTO-AGI-DEMO",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "networkx>=2.6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ],
    },
)
