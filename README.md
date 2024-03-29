# SALON - [Sequence ALignment ONtology](https://github.com/benhid/SALON)

[![DOI](https://zenodo.org/badge/317975049.svg)](https://zenodo.org/badge/latestdoi/317975049)
[![Explore ontology](https://img.shields.io/badge/docs-Documentation-orange.svg)](https://w3id.org/salon/)

### ✨ Ontology 

[SALON.owl](SALON.owl) was developed using Protégé 5.5.0 (beta 5 SNAPSHOT).

You can directly load the ontology in Protégé using the provided URI:

> https://w3id.org/salon/

### 🧰 Client

**Note**: Unlike Virtuoso, [Stardog](https://www.stardog.com/) supports SWRL rules (which this ontology makes use of). Therefore, this tool requires a running Stardog server instance to unlock all features, albeit Virtuoso or any other triple store can be used. You can deploy Stardog on Docker with:

```shell
$ docker run -it -v ~/your/license/folder/:/var/opt/stardog -p 5820:5820 stardog/stardog
```

#### Installation

To download and install the SALON companion client just clone the Git repository hosted in GitHub:

```shell
$ git clone git@github.com:benhid/SALON.git
$ cd salon
$ python setup.py install
```

Then, run

```shell
$ saloncli --help
```

#### Settings

Setup environmental variables as follows (using your own connection settings):

```shell
$ export STARDOG_ENDPOINT=http://localhost:5820
$ export STARDOG_USERNAME=admin 
$ export STARDOG_PASSWORD=admin 
$ export STARDOG_DATABASE=salon
```

Alternatively, create a dotenv file in the current directory and append the former variables.

#### Usage

Creates database in RDF repository
```shell
$ saloncli init -i SALON.owl
```

Transform sequence alignment from MACSIM/XML to Turtle
```shell
$ saloncli parse -i examples/BB11001.xml -o examples/BB11001.ttl
```

Populates RDF repository
```shell
$ saloncli load -i examples/BB11001.ttl
```

Enriches protein sequence given its URI
```shell
$ saloncli enrich -x https://w3id.org/salon#BB11001_1aab_
```

Generates UniprotKB FASTA header/description line for protein sequence given its URI
```shell
$ saloncli header -x https://w3id.org/salon#BB11001_1aab_
```

### 📖 Documentation

Documentation was generated with pyLODE 2.8.3:

```shell
$ make docs
```

<p align="center">&mdash; ⭐️ &mdash;</p>
<p align="center"><i>Designed & built by Khaos Research (University of Málaga).</i></p>
