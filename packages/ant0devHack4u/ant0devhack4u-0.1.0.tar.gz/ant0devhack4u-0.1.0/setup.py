from setuptools import setup, find_packages

# Leer el contenido del archivo README.md
with open('README.md', "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ant0devHack4u",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Antonio Infantes",
    description="Una biblioteca del curso Python Ofensivo de Hack4u",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://hack4u.io"
)
