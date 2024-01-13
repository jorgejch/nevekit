from setuptools import setup, find_packages

requirements = [
    "bravado[fido]==11.0.3,<12.0.0",
    "bravado-core>=6.1.1,<7.0.0",
    "numpy>=1.26,<2.0",
    "dill>=0.3.7,<1.0.0",
]

setup(
    name="nevekit",
    version="0.1.0",
    packages=find_packages(),
    install_requires=requirements,
)
