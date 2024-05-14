from setuptools import setup, find_packages

VERSION = '0.1.0'
DESCRIPTION = 'API Wrapper for Snusbase'
LONG_DESCRIPTION = 'A wrapper for the database lookup website, Snusbase'

setup(
    name="snusbase",
    version=VERSION,
    author="leon",
    author_email="viiiee@femboy.cx",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['httpx']
)
