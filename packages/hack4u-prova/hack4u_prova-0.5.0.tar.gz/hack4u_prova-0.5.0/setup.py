from setuptools import setup, find_packages

# Leer el contenido del archivo README.md
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="hack4u_prova",
    version="0.5.0",
    packages=find_packages(),
    install_requires=[],
    author="Ramon Santos",
    description="A simple package to test the Python packaging",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://hack4u.io",
)

