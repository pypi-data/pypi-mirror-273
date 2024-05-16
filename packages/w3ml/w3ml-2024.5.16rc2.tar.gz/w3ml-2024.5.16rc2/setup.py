import setuptools


def load_long_description():
    with open("README.md", "r") as f:
        long_description = f.read()
    return long_description


def get_version():
    with open("w3ml/__init__.py", "r") as f:
        for line in f.readlines():
            if line.startswith("__version__"):
                return line.split('"')[1]
        else:
            raise TypeError("NO W3ML_VERSION")


setuptools.setup(
    name="w3ml",
    version=get_version(),
    author="kyunam",
    author_email="rbska56455@gmail.com",
    description="Personal library using W3",
    long_description=load_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/kyu90/web3_ml",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "autogluon.tabular==0.5.0",
        "numpy>=1.19.2,<1.20",
        "pandas>=1.1.1,<1.2.0",
    ],
)
