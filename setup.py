from os.path import abspath, dirname, join

from setuptools import find_packages, setup

basedir = abspath(dirname(__file__))

with open(join(basedir, "README.md"), encoding="utf-8") as f:
    README = f.read()

install_requires = [
    "Biopython",
    "rdflib==5.0.0",  # Warn: this version is required for pylode (see: https://github.com/RDFLib/pyLODE/issues/145)
    "rdflib-jsonld==0.5.0" "SPARQLWrapper",  # Required for rdflib<=5.0.0
    "requests",
    "click",
]
extras_require = {
    "docs": install_requires + ["pylode==2.12.0"],
    "black": install_requires + ["isort", "black"],
}

setup(
    name="saloncli",
    version="0.1.1",
    description="SALON client",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Antonio Benítez-Hidalgo",
    author_email="antoniobenitez@lcc.uma.es",
    license="MIT",
    url="https://github.com/benhid/SALON",
    packages=find_packages(exclude=["test_"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3.6",
    ],
    install_requires=install_requires,
    extras_require=extras_require,
    entry_points={
        "console_scripts": [
            "saloncli=salon.cli:entry_point",
        ],
    },
)
