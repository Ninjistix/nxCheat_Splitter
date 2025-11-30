from setuptools import setup, find_packages

setup(
    name="nxCheat_Splitter",
    version="1.0.0",
    author="Ninjistix",
    description="A simple Windows tool to split Nintendo Switch cheat files into per-build-ID folders.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Ninjistix/nxCheat_Splitter",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "tkinterdnd2"
    ],
    entry_points={
        "console_scripts": [
            "nxcheat=cheat_converter_gui:main"
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
    ],
    python_requires=">=3.10",
)
