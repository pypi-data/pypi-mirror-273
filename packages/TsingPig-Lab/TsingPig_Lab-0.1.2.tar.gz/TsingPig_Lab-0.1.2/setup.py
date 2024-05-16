import tsingpig_lab

__version__ = tsingpig_lab.__version__
__author__ = tsingpig_lab.__author__
__package_name__ = tsingpig_lab.__package_name__


import setuptools

with open("README.md",'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name = __package_name__,
    version = __version__,
    author = __author__,
    author_email = "1114196607@qq.com",
    description = "TsingPig_Lab is a package for algorithm.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url="https://gitlab.com/tsingpig-code/tsingpig_lab",
    packages=setuptools.find_packages(),
    install_requires = [],
    # add any additional packages that needs to be installed along with SSAP package.

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)