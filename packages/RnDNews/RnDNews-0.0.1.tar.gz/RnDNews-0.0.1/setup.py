from setuptools import find_packages, setup

setup(
    version='0.0.1',
    name='RnDNews',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(include=['RnDNews']),
    description='Crawling RnDNews',
    install_requires=[],
    author='Leyton'
)

