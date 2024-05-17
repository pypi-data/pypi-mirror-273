
from setuptools import setup, find_packages

setup(
    name='bhalaho',
    version='0.3',
    packages=find_packages(),
    include_package_data=True,
    package_data={'bhalaho': ['data/*.c']},
)

