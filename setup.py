from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="enigmachine",
    version="0.4",
    packages=find_packages(),
    install_requires=[
        "tabulate",
    ],
    description="Engima chiper machine",
    author="Fernando Cortés",
    author_email="fcsancho14@gmail.com",
    license="MIT",
    home_page="https://github.com/Fer14/enigmachine",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
