from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.10'
DESCRIPTION = 'Data Preprocessing library that makes EDA easy for all'


# Setting up
setup(
    name="lprocess",
    version=VERSION,
    author="Chirag Patil",
    author_email="chiragnpatil@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy', 'pandas', 'matplotlib'],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
