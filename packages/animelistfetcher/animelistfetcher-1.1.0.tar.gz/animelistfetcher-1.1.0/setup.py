from setuptools import setup, find_packages
setup(
    name='animelistfetcher',
    version='1.1.0',
    description='A Python wrapper for my anime libraries',
    author='Dominik Procházka',
    packages=find_packages(),
    install_requires=['alfetcher', 'malfetcher']
)