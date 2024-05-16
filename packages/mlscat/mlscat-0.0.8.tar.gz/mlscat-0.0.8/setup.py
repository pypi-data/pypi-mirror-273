from setuptools import setup, find_packages

with open('./README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

PACKAGE = "mlscat"
NAME = PACKAGE
VERSION = __import__(PACKAGE).__version__

setup(
    name=NAME,
    version=VERSION,
    packages=find_packages(),
    install_requires=[
        'numpy',
    ],
    author="i4mhmh",
    author_email='i4mhmh@outlook.com',
    description='A small cat help you enjoy your side channel attack journal!',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires = ">=3.8"
)