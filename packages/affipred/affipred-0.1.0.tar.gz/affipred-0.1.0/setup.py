import setuptools

with open("README.md", "r", encoding="utf-8") as fhand:
    long_description = fhand.read()

setuptools.setup(
    name="affipred",
    version="0.1.0",
    author="Mustafa S. Pir",
    author_email="mustafapir29@gmail.com",
    description=("AlphaFold based Functional Impact Prediction of Missense Variations"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mustafapir/affipred",
    project_urls={
        "Bug Tracker": "https://github.com/mustafapir/affipred/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["pysam>=0.22.0","requests>=2.31.0","pandas>=2.0.0","biopython>=1.81","numpy>=1.24.0"],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "affipred_pred = AFFIPred_cli.cli:main",
        ]
    }
)