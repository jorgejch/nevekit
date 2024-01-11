from setuptools import setup, find_packages

requirements = [
    'bravado[fido]==11.0.3',
    'bravado-core==6.1.1'
]

setup(
    name='nevekit',
    version='0.1.0',
    packages=find_packages(),
    install_requires=requirements,
)
