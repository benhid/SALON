import click

from salon.database.stardog import Stardog

from salon.config import settings


@click.command()
@click.option(
    "--uri",
    "-x",
    help="Protein alignment sequence URI.",
)
def export(uri: str):
    """
    Returns FASTA description line for a protein sequence in the ontology.
    """
    query = """
        PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
        PREFIX skos:<http://www.w3.org/2004/02/skos/core#> 
        PREFIX up:<http://purl.uniprot.org/core/>
        PREFIX salon:<"""+settings.ONTOLOGY_IRI+"""">
        SELECT DISTINCT ?db ?UniqueIdentifier ?EntryName 
               ?OrganismName ?OrganismIdentifier ?ProteinName 
               ?GeneName ?ProteinExistence
        WHERE{
            <""" + uri + """> a salon:ProteinAlignmentSequence ;
                              salon:identifier ?UniqueIdentifier ;
                              salon:organism ?OrganismIdentifier ;
                              salon:associatedTo ?protein .
            ?protein a salon:Protein ;
                     salon:proteinName ?ProteinName ;
                     rdfs:seeAlso ?pdb .
            SERVICE <http://sparql.uniprot.org/sparql> {
                ?pdb a up:Protein ;
                         up:reviewed ?db ;
                         up:encodedBy ?gene ;
                         up:mnemonic ?EntryName ;
                         up:existence ?ProteinExistence ;
                         up:organism ?organism .
                ?gene skos:prefLabel ?GeneName .
                ?organism a up:Taxon;
                          up:scientificName ?OrganismName .
            }
        }
    """
    management = Stardog(
        endpoint=settings.STARDOG_ENDPOINT,
        database=settings.STARDOG_DATABASE,
        username=settings.STARDOG_USERNAME,
        password=settings.STARDOG_PASSWORD,
    )
    res = management.query(query)

    try:
        bindings = res['results']['bindings']
    except IndexError:
        bindings = {}

    for seq in bindings:
        db = "sp" if seq["db"]["value"] else "tl"
        unique_identifier = seq["UniqueIdentifier"]["value"]
        entry_name = seq["EntryName"]["value"]
        protein_name = seq["ProteinName"]["value"]
        organism_name = seq["OrganismName"]["value"]
        organism_identifier = seq["OrganismIdentifier"]["value"]
        gene_name = seq["GeneName"]["value"]

        mapping = {
            "http://purl.uniprot.org/core/Evidence_at_Protein_Level_Existence": 1,
            "http://purl.uniprot.org/core/Evidence_at_Transcript_Level_Existence": 2,
            "http://purl.uniprot.org/core/Inferred_from_Homology_Existence": 3,
            "http://purl.uniprot.org/core/Predicted_Existence": 4,
            "http://purl.uniprot.org/core/Uncertain_Existence": 5,
        }
        protein_existence = seq["ProteinExistence"]["value"]
        protein_existence = mapping[protein_existence]

        # UniprotKb FASTA header specification
        template = (
            f">{db}|{unique_identifier}|{entry_name} {protein_name} "
            f"OS={organism_name} OX={organism_identifier} GN={gene_name} PE={protein_existence}"
        )

        print(f"Potential description line(s) found for sequence {uri}:")
        print(f"\t{template}")


if __name__ == "__main__":
    export()
