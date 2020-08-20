from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="crun-py",
    version="0.0.5",
    author="Snehashis Sarkar",
    author_email="snehashis.2000@gmail.com",
    description="C Programming Simplified",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://get-crun.github.io/",
    project_urls={
        "GitHub repository": "https://github.com/snehashis365/cRun-py",
    },
    packages=["cRun_py"],
    install_requires=[
          "windows-curses >= 2.0;platform_system=='Windows'", "tqdm"
      ],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "cRun-py=cRun_py.cRun:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: Android",
    ],
    python_requires='>=3.6',
)
