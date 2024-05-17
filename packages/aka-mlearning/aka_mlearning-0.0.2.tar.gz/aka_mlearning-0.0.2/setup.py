from setuptools import setup, find_packages


setup(
    name="aka_mlearning",
    version="0.0.2",
    packages=find_packages(),
    install_requires=[
        "xgboost",
        "catboost",
        "pandas>=1.3.5",
        "matplotlib"
    ],
    author="Kader Geraldo",
    description="Regression and classification analysis tools",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown"
)