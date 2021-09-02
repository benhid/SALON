from collections import defaultdict
from pathlib import Path

import click
from Bio import AlignIO
from rdflib import RDF, Graph, Literal, Namespace, URIRef

from salon.config import settings

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def _etree_to_dict(t):
    """Transform an XML to a Python dictionary."""
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(_etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k: v[0] if len(v) == 1 else v for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update(("@" + k, v) for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
                d[t.tag]["#text"] = text
        else:
            d[t.tag] = text
    return d


def from_macsim_xml_instance(filepath: str) -> Graph:
    """
    Creates an RDF graph for given input alignment in MACSIM/XML format.

    :param filepath: Input file in MACSIM/XML format.
    :return: RDF graph.
    """
    root = ET.parse(filepath).getroot()
    instance = Path(filepath).stem

    # rdf graph
    graph = Graph()

    # bind namespace
    namespace = Namespace(settings.ONTOLOGY_IRI)
    graph.bind(settings.ONTOLOGY_NAMESPACE, namespace)

    for alignment in root:
        alignment_uri = URIRef(f"{namespace}{instance}")
        graph.add((alignment_uri, RDF.type, namespace.Alignment))
        graph.add((alignment_uri, namespace.gapCharacter, Literal("-")))

        for item in alignment.iterfind("aln-name"):
            subalignment_name = item.text.replace("/", "-")
            subalignment_uri = URIRef(f"{namespace}{instance}_{subalignment_name}")
            graph.add((alignment_uri, namespace.hasSubAlignment, subalignment_uri))
            graph.add((subalignment_uri, RDF.type, namespace.SubAlignment))
            graph.add((subalignment_uri, namespace.subAlignmentName, Literal(subalignment_name)))

            for item in alignment.iterfind("aln-score"):
                alignment_score_uri = URIRef(f"{namespace}{instance}_{subalignment_name}_score")
                graph.add((alignment_uri, namespace.hasAlignmentScore, alignment_score_uri))
                graph.add((alignment_score_uri, namespace.score, Literal(item.text)))

            for sequence in alignment.iter("sequence"):
                seq_name, seq_uri = "", ""
                for item in sequence.iterfind("seq-name"):
                    seq_name = item.text
                    seq_uri = URIRef(f"{namespace}{instance}_{seq_name}")

                graph.add((subalignment_uri, namespace.hasSequence, seq_uri))
                graph.add((seq_uri, namespace.identifier, Literal(seq_name)))

                if sequence.attrib["seq-type"] == "Protein":
                    graph.add((seq_uri, RDF.type, namespace.ProteinAlignmentSequence))
                else:
                    graph.add((seq_uri, RDF.type, namespace.DNAAlignmentSequence))

                for item in sequence.iterfind("seq-data"):
                    graph.add((seq_uri, namespace.sequence, Literal(item.text.strip())))
                    graph.add((seq_uri, namespace.length, Literal(len(item.text.strip()))))

                for i, item in enumerate(sequence.iter("fitem")):
                    blocks = _etree_to_dict(item)["fitem"]
                    feature_uri = URIRef(f"{namespace}{instance}_{seq_name}_f{i}")
                    graph.add((seq_uri, namespace.hasFeature, feature_uri))
                    graph.add((feature_uri, namespace.FType, Literal(blocks["ftype"])))
                    graph.add((feature_uri, namespace.FNote, Literal(blocks["fnote"])))
                    graph.add((feature_uri, namespace.FStop, Literal(blocks["fstop"])))
                    graph.add((feature_uri, namespace.FStart, Literal(blocks["fstart"])))
                    graph.add((feature_uri, namespace.FScore, Literal(blocks["fscore"])))

                for info in sequence.iter("seq-info"):
                    for item in info.iterfind("accession"):
                        # item_alpha = re.sub(r'[\W_]+', '', item.text)  # keep only alphanumeric
                        graph.add(
                            (
                                seq_uri,
                                namespace.accessionNumber,
                                Literal(item.text),
                            )
                        )

                    for item in info.iterfind("definition"):
                        graph.add((seq_uri, namespace.description, Literal(item.text.strip())))

                    for item in info.iterfind("organism"):
                        graph.add((seq_uri, namespace.organism, Literal(item.text.strip())))

    return graph


def from_fasta(filepath: str) -> Graph:
    """
    Transform input alignment into RDF graph.

    :param filepath: Input file in FASTA-like format.
    :return: RDF graph.
    """
    instance = Path(filepath).stem

    # rdf graph
    graph = Graph()

    # creates and bind namespace
    namespace = Namespace(settings.ONTOLOGY_IRI)
    graph.bind(settings.ONTOLOGY_NAMESPACE, namespace)

    # alignment data
    alignment_uri = URIRef(f"{namespace}{instance}")
    graph.add((alignment_uri, RDF.type, namespace.Alignment))
    graph.add((alignment_uri, namespace.gapCharacter, Literal("-")))

    # sub alignment data
    subalignment_uri = URIRef(f"{namespace}{instance}_subalignment")
    graph.add((alignment_uri, namespace.hasSubAlignment, subalignment_uri))
    graph.add((subalignment_uri, RDF.type, namespace.Sub_Alignment))
    graph.add((subalignment_uri, namespace.subAlignmentName, Literal(instance)))

    for record in AlignIO.read(filepath, "fasta"):
        seq_uri = URIRef(f"{namespace}{instance}_{record.name}")
        graph.add((subalignment_uri, namespace.hasSequence, seq_uri))
        graph.add((seq_uri, namespace.identifier, Literal(record.name)))

        if True:  # TODO: check if protein or dna
            graph.add((seq_uri, RDF.type, namespace.ProteinAlignmentSequence))

        graph.add((seq_uri, namespace.sequence, Literal(record.seq.upper())))
        graph.add((seq_uri, namespace.length, Literal(len(record))))
        graph.add((seq_uri, namespace.accessionNumber, Literal(record.id.upper())))

    return graph


@click.command()
@click.option(
    "--input-path",
    "-i",
    help="Input file path (FASTA, MACSIM/XML)",
)
@click.option("--output-path", "-o", default="output.ttl", help="Output file path.")
def parse(input_path: str, output_path: str):
    """
    Supported formats: MACSIM/XML, FASTA.
    """
    in_extension = Path(input_path).suffix.lower()
    out_extension = Path(output_path).suffix[1:].lower()

    if in_extension == ".xml":
        graph = from_macsim_xml_instance(input_path)
    elif in_extension == ".fa" or in_extension == ".fasta":
        graph = from_fasta(input_path)
    else:
        raise ValueError("Input file not supported, try one of these extensions instead: .xml, .fasta, .fa")

    graph.serialize(destination=output_path, format=out_extension)


if __name__ == "__main__":
    parse()
