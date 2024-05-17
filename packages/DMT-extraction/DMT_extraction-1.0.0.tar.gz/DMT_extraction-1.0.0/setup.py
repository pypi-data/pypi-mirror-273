import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DMT_extraction",
    version="1.0.0",
    author="SemiMod",
    author_email="mario.krattenmacher@semimod.de",
    description="Device Modeling Toolkit extraction submodule",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/dmt-development/dmt_extraction",
    packages=setuptools.find_namespace_packages(include=["DMT.*"]),
    license="DMT License",
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
    ],
    package_data={"": ["*.tex", "*.bib", "doc"]},
    install_requires=[
        "DMT-core[pyqtgraph,latex]",
        "qtpy",
        "matplotlib",
    ],
    extras_require={
        "batch_mode": ["coloredlogs", "click"],
        "pyside2": ["PySide2"],
        "pyside6": ["PySide6"],
    },
)
