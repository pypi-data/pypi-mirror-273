from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='apple_silicon_booknlp',
    version='1.0.7.1',
    packages=find_packages(),
    py_modules=['booknlp'],
    url="https://github.com/dbamman/book-nlp",
    author="David Bamman (Creator) and Drew Thomasson (For this apple silicon pip)",
    author_email="dbamman@berkeley.edu",
    license="MIT",
    include_package_data=True,
    install_requires=[
        'torch>=1.7.1',
        'tensorflow-macos',
        'spacy>=3',
        'transformers>=4.11.3,<=4.30.0'
    ],
    long_description=long_description,
    long_description_content_type="text/markdown"  # Markdown format for the README
)
