from setuptools import find_packages, setup


def read_requirements():
    with open('requirements.txt') as req:
        return req.read().splitlines()

setup(
    packages=find_packages(exclude=['*test']),
    install_requires=read_requirements(),    
    py_modules=['vayu', 'vayu_consts'],
)

