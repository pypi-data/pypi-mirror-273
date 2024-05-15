from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name='echostar_public_cloud_hello',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'zipp>=3.13.0',
    ],
    entry_points={
        "console_scripts": [
            "paas-hello = simple_hello:hello",
        ],
    },
    long_description=description,
    long_description_content_type="text/markdown",
)
