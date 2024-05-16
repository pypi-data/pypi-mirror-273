from setuptools import setup, find_packages

# Read the contents of the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pedil",
    version="0.1.1",  # Increment the version number
    author="Ire Gaddr",
    author_email="iregaddr@gmail.com",
    description="A Python package for generating unique and secure IDs using Prime Extended Decimal Index Listing (PEDIL).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pedil",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "sympy",
    ],
)
