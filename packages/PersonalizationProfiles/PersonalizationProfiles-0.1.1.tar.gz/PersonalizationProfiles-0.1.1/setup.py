from setuptools import setup, find_packages

setup(
    name='PersonalizationProfiles',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy>= 1.20"
    ],
)