# coding:utf-8
import sys

from setuptools import setup, find_packages

install_requires = [
    "requests>=2.25.1",
    "retry==0.9.2",
    "pytz==2020.5",
    "pycryptodome==3.9.9",
    "protobuf>=3.18.3",
    "google>=3.0.0",
    "six>=1.0",
]

setup(
    name="test-set-sdk",
    version="1.0.12",
    keywords=("pip", "test", "test-set-sdk"),
    description="The test set SDK for Python",
    license="MIT License",

    url="https://github.com/johlin/test3",
    author="test-set SDK",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=install_requires
)
