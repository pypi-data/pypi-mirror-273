from distutils.core import setup
from setuptools import find_packages

setup(
    name="pandasql-lts",
    version="0.7.3",
    author="Greg Lamp",
    author_email="greg@yhathq.com",
    maintainer="Bui Hoang Tu",
    maintainer_email="bhtu.work@gmail.com",
    url="https://github.com/BuiHoangTu/pandasql/tree/release",
    license="MIT",
    packages=find_packages(),
    package_dir={"pandasql": "pandasql"},
    package_data={"pandasql": ["data/*.csv"]},
    description="sqldf for pandas",
    long_description=open("README.rst").read(),
    install_requires=["numpy", "pandas", "sqlalchemy"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
)
