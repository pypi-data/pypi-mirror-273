from setuptools import setup, find_packages


setup(
    name="aka-data-prep",
    version="0.0.4",
    packages=find_packages(),
    install_requires=[ 
        "pandas>=1.3.5",
        "matplotlib"
    ],
    author="Kader Geraldo",
    description = "Tools for data preparation, cleaning, and preprocessing",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown"
)