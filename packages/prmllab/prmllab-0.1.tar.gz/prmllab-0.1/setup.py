from setuptools import setup, find_packages

setup(
    name='prmllab',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    package_data={'prmllab ': ['*.py', '*.ipynb','*.zip']},
)
