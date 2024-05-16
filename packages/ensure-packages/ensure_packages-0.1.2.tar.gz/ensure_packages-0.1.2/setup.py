from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ensure_packages",  # Replace with your own package name
    version="0.1.2",
    author="vinothjs",
    author_email="jeyashreenarayan@gmail.com",
    description="A package to ensure other packages are installed its created by vinoth cse-B. a laternate for using pip",
    long_description=long_description,
    long_description_content_type="text/markdown",
 # Replace with your own URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
