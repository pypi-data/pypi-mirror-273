from setuptools import setup, find_packages

setup(
    name='pedil',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'sympy',  # Specify dependencies here
    ],
    author='Your Name',
    author_email='your.email@example.com',
    description='A Python package for generating unique IDs using the Prime Extended Decimal Index Listing (PEDIL) method.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/IreGaddr/pedil',  # Replace with your GitHub repository URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
