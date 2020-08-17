from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="crun-py",
    version="0.0.2",
    author="Snehashis Sarkar",
    author_email="snehashis.2000@gmail.com",
    description="C Programming Simplified",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/snehashis365/cRun",
    packages=["src"],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "cRun-py=src.cRun:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
    ],
    python_requires='>=3.6',
)
