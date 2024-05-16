from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='windows_booknlp',
    version='0.0.1', 
    packages=find_packages(),
    py_modules=['booknlp'],
    url="https://github.com/DrewThomasson/booknlp",
    author="David Bamman and Andrew Phillip Thomasson",
    author_email="dbamman@berkeley.edu",
    include_package_data=True, 
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Adjust content type if necessary
    install_requires=[
        'torch>=1.7.1',
        #'tensorflow>=1.15',
        'spacy>=3',
        'transformers>=4.11.3,<=4.30.0'         
    ],
)
