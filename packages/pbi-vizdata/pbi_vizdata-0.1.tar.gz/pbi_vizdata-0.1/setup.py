# setup.py

from setuptools import setup, find_packages

setup(
    name='pbi_vizdata',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'os',
        'time',
        'pandas',
        'shutil',
        're',
        'powerbiclient'
    ],  # Add any dependencies here
    author = "Nitin Satish",
    zip_safe=False
)
