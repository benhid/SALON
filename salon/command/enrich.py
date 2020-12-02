import click

from salon.database.stardog import Stardog

from salon.config import settings

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


@click.command()
@click.option(
    "--uri",
    "-x",
    help="Source URI to enhance (i.e., sequence).",
)
def enrich(uri: str):
    """
    Adds information to sequences in the database following the ontology specification.
    This function ONLY WORKS for *protein sequences*.
    """
    query = (
        """
        PREFIX salon:<"""+settings.ONTOLOGY_IRI+"""">
        SELECT ?ac
        WHERE {
            <"""
        + uri
        + """> a salon:ProteinAlignmentSequence .
            OPTIONAL{<"""
        + uri
        + """> salon:accessionNumber ?ac} .
        }
    """
    )

    management = Stardog(
        endpoint=settings.STARDOG_ENDPOINT,
        database=settings.STARDOG_DATABASE,
        username=settings.STARDOG_USERNAME,
        password=settings.STARDOG_PASSWORD,
    )
    res = management.query(query)

    try:
        bindings = res['results']['bindings'][0]
    except IndexError:
        print(f"Accession number not found for sequence {uri}")
        bindings = {}

    # We _assume_ that the ac number is linked to the PDB identifier of the sequence's protein
    pdb = bindings.get("ac", None)
    pdb_value = pdb["value"]

    if pdb_value:
        query = (
            """
            PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
            PREFIX up:<http://purl.uniprot.org/core/>
            PREFIX pdb:<http://rdf.wwpdb.org/pdb/>
            PREFIX salon:<"""+settings.ONTOLOGY_IRI+"""">
            INSERT {
                <"""
            + uri
            + """> salon:organism ?ncbi . 
                <"""
            + uri
            + """> salon:associatedTo ?protein_uri .
                ?protein_uri a salon:Protein .
                ?protein_uri salon:description ?protfullname .
                ?protein_uri salon:keyword ?protmnemonic .
                ?protein_uri salon:proteinName ?protfullname .
                ?protein_uri rdfs:seeAlso ?organism .
                ?protein_uri rdfs:seeAlso ?protein .
                ?protein_uri rdfs:seeAlso ?pdb .
            }
            WHERE {
                <"""
            + uri
            + """> rdf:type salon:ProteinAlignmentSequence .
                SERVICE <http://sparql.uniprot.org/sparql> {
                    BIND(pdb:"""
            + pdb_value.upper()
            + """ AS ?pdb) .
                    ?protein a up:Protein;
                             rdfs:seeAlso ?pdb ;
                             up:recommendedName ?protname ;
                             up:mnemonic ?protmnemonic ;
                             up:organism ?organism .
                    ?protname up:fullName ?protfullname .
                    ?organism up:mnemonic ?orgmnemonic ;
                              up:scientificName ?orgscientific .
                    BIND(STRAFTER(STR(?protein), "http://purl.uniprot.org/uniprot/") AS ?ac) .
                    BIND(STRAFTER(STR(?organism), "http://purl.uniprot.org/taxonomy/") AS ?ncbi)
                    BIND(URI(CONCAT("salon:", STR(?ac))) AS ?protein_uri)
                }
            }
        """
        )
        management.update(query)


if __name__ == "__main__":
    enrich()
