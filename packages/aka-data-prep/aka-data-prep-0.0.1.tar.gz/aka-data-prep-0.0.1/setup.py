from setuptools import setup, find_packages


setup(
    name="aka-data-prep",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[ 
        "pandas>=1.3.5",
        "matplotlib", 
        "shap"
        ],
    author="Kader Geraldo",
    description = "Tools for data preparation, cleaning, and preprocessing",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown"
)