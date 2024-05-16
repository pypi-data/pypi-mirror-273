from setuptools import setup, find_packages

setup(
    name="AbeewayConfig",
    version='0.11',
    packages=find_packages(),
    install_requires=[
        "pyserial",
    ],
    entry_points={
        "console-scripts": [
            "abeewayconfig = AbeewayConfig:main",
        ],
    },
)
