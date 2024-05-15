from setuptools import setup, find_packages

# Read the long description from README.md file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="common_hms_library",
    version="1.1",
    author="Aditya Sharma",
    author_email="aditya@softprimeconsulting.com",
    description="Library for calculating age as float based on date of birth",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
