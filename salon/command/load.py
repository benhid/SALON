from pathlib import Path

import click
from rdflib import Graph

from salon.config import settings
from salon.database.stardog import Stardog


@click.command()
@click.option(
    "--filename",
    "-i",
    help="Create database.",
)
def create(filename: str):
    """
    Creates the database.
    """
    management = Stardog(
        endpoint=settings.STARDOG_ENDPOINT,
        database=settings.STARDOG_DATABASE,
        username=settings.STARDOG_USERNAME,
        password=settings.STARDOG_PASSWORD,
    )
    management.setup_database(filename=filename)


@click.command()
@click.option(
    "--filename",
    "-i",
    help="Input file name.",
)
def load(filename: str):
    """
    Inserts data to RDF repository.
    """
    file_extension = Path(filename).suffix[1:].lower()

    management = Stardog(
        endpoint=settings.STARDOG_ENDPOINT,
        database=settings.STARDOG_DATABASE,
        username=settings.STARDOG_USERNAME,
        password=settings.STARDOG_PASSWORD,
    )

    graph = Graph()
    graph.parse(location=filename, format=file_extension)
    graph_as_ttl = graph.serialize(format="nt").decode("UTF-8")

    # management.update("DROP SILENT GRAPH <salon>")

    if isinstance(management, Stardog):
        query_string = "INSERT DATA { " + graph_as_ttl + " }"
    else:
        query_string = "INSERT DATA { GRAPH { " + management.database + " } " + graph_as_ttl + " }"

    management.update(query_string)


if __name__ == "__main__":
    load()
