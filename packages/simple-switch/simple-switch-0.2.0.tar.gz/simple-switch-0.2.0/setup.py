import setuptools

VERSION = '0.2.0'

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simple-switch",
    version=VERSION,
    author='David Flanders',
    author_email='thedatadave@gmail.com',
    url='https://github.com/TheDataDave/switch',
    description="A simple and flexible switch statement implementation for Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['python', 'conditional', 'logic', 'switch', 'case', 'if-else', 'if', 'else'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: OS Independent",
    ],
)
