from setuptools import setup, find_packages
import os

setup(
    name="wsppchem",
    version="0.1",
    author="Cossard Lucas and Enzo Venancio",
    author_email="lucas.cossard@epfl.ch and enzo.venancio@epfl.ch",
    description="Water Solubility Prediction Project",
    long_description=open('README.md').read() if os.path.exists('README.md') else '',
    long_description_content_type="text/markdown",
    url="https://github.com/Nohalyan/WSPP_Projectppchem",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        "pandas",
        "numpy",
        "rdkit",
        "tqdm",
        "lightgbm",
        "requests"
    ],
)
