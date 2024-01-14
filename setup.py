from setuptools import setup, find_packages

requirements = [
    "bravado[fido]==11.0.3,<12.0.0",
    "bravado-core>=6.1.1,<7.0.0",
    "numpy>=1.26,<2.0",
    "dill>=0.3.7,<1.0.0",
]

setup(
    name="nevekit",
    version="0.1.0-alpha.1",
    packages=find_packages(),
    install_requires=requirements,
    author="Jorge Haddad",
    author_email="jorgejch@gmail.com",
    description="A Python library for EVE Online.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jorgejch/nevekit",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: Tested on GitHub's ubuntu-latest.",
    ],
    python_requires='>=3.11',
)