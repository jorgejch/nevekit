from setuptools import setup, find_packages

# Read requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='nevekit',
    version='0.1.0',
    packages=find_packages(),
    install_requires=requirements,
)
