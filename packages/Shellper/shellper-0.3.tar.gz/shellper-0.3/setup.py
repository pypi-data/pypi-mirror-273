from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Shellper",
    version="0.3",
    author="ShawnMerry",
    author_email="merrybili@163.com",
    description="A Python Library for create shell apps.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/ShawnMerry/Shellper",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Internet"
    ],
    python_requires=">=3"
)
