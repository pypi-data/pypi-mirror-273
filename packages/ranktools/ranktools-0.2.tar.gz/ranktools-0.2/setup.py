from setuptools import setup, find_packages

with open("README.md", 'r') as handle:
    description = handle.read()

setup(
    name='ranktools',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.15.0'
    ],
    long_description=description,
    long_description_content_type="text/markdown",
)
