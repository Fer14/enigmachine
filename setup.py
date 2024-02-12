from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="enigmachine",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "tabulate",
    ],
    description="Engima chiper machine",
    author="Fernando Cortés",
    author_email="fcsancho14@gmail.com",
    license="MIT",
    url="https://github.com/Fer14/enigmachine",
    project_urls={
        "Bug Tracker": "https://github.com/Fer14/enigmachine/issues",
        "Documentation": "https://github.com/Fer14/enigmachine/",
        "Source Code": "https://github.com/Fer14/enigmachine/",
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="enigma machine cryptography cipher",
)
