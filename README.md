# [Sequence ALignment ONtology](https://github.com/benhid/SALON)

[![Explore ontology](https://img.shields.io/badge/docs-Documentation-orange.svg?style=flat-square)](https://benhid.github.io/SALON/index.html)

### ✨ Ontology 

[SALON.owl](SALON.owl) was developed using Protégé 5.5.0 (beta 5 SNAPSHOT).

### 🧰 Client

**Note**: This tool requires a running [Stardog](https://www.stardog.com/) server instance.

#### Installation

To download and install the client just clone the Git repository hosted in GitHub:

```bash
git clone https://github.com/benhid/SALON.git
cd salon
python setup.py install
```

Then, run

```bash
saloncli --help
```

#### Settings

Setup environmental variables as follows (using your own connection settings):

```bash
export STARDOG_ENDPOINT=http://0.0.0.0:5820
export STARDOG_USERNAME=admin 
export STARDOG_PASSWORD=admin 
export STARDOG_DATABASE=salon
```

Alternatively, create a dotenv file in the current directory and append the former variables.

#### Usage

Creates database in RDF repository
```bash
saloncli create -i SALON.owl
```

Transform sequence alignment to RDF/XML 
```bash
saloncli parse -i examples/sample.fasta -o sample.ttl
```

Populates RDF repository  
```bash
saloncli load -i sample.ttl
```

Enriches protein sequence given its URI
```bash
saloncli enrich -x http://www.ontologies.khaos.uma.es/salon/sample_1A00
saloncli enrich -x http://www.ontologies.khaos.uma.es/salon/sample_1e32
saloncli enrich -x http://www.ontologies.khaos.uma.es/salon/sample_1e94
saloncli enrich -x http://www.ontologies.khaos.uma.es/salon/sample_1d2n
```

Generates UniprotKB FASTA description line for protein sequence given its URI
```bash
saloncli export -x http://www.ontologies.khaos.uma.es/salon/sample_1A00
```

### 📖 Documentation

Documentation was generated with pyLODE 2.8.3:

```bash
pylode -i SALON.owl -o ./docs/index.html
```

<p align="center">&mdash; ⭐️ &mdash;</p>
<p align="center"><i>Designed & built by Khaos Research (University of Málaga).</i></p>
