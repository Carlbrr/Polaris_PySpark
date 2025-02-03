from setuptools import setup, find_packages
#Used to package the code to be installed by pip

setup(
    name="polarisx",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["pyspark", "requests"],
    author="Carl Bruun & Andreas Kongstad",
    description="PolarisX function catalog integration for PySpark",
    url="https://github.com/Carlbrr/Polaris_PySpark",
)
