from setuptools import setup, find_packages
import os 
with open("README.md", "r") as fh:
    long_description = fh.read()
VERSION=os.getenv("PACKAGE_VERSION")
setup(
    name="helm-hawk",
    version=VERSION,
    packages=find_packages(include=['cli', 'cli.*'], exclude=["dist","build","*.egg-info","tests", "cli/diff", "cli/get", "cli/history", "cli/rollback", "cli/status", "cli/uninstall", "cli/upgrade", "cli/utils"]),
    package_dir={'cli': 'cli'},
    install_requires=[
        'click',
        'colorama'
    ],
    author="Ankit Singh",
    author_email="as8356047@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.8',
    entry_points='''
    [console_scripts]
    helm-hawk=cli.main:cli
    ''',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

)