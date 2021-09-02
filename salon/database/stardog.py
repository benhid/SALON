import json

import requests
from SPARQLWrapper import JSON, SPARQLWrapper

from salon.database.repository import RDFRepository


class Stardog(RDFRepository):
    """
    SPARQLWrapper for Stardog graph store.
    """

    def init(self, filename: str):
        """
        Initialize the database by creating the required schema.
        """
        session = requests.Session()
        session.auth = (self.username, self.password)

        meta = {
            "dbname": self.database,
            "options": {"search.enabled": "true"},
            "files": [{"filename": filename}],
        }

        params = [
            ("root", (None, json.dumps(meta), "application/json")),
            (
                filename,
                (
                    filename,
                    open(filename),
                    "application/rdf+xml",
                    {"Content-Encoding": None},
                ),
            ),
        ]

        r = session.post(f"{self.endpoint}/admin/databases", files=params)
        return r.status_code, r.reason

    def update(self, query: str) -> dict:
        sparql = SPARQLWrapper(f"{self.endpoint}/{self.database}/update")
        sparql.setReturnFormat(JSON)
        sparql.setMethod("POST")
        sparql.setQuery(query)

        if self.username:
            sparql.setCredentials(self.username, self.password)

        print(f"Running update query:\n{query}")

        return sparql.query().convert()

    def query(self, query: str) -> dict:
        sparql = SPARQLWrapper(f"{self.endpoint}/{self.database}/query")
        sparql.setReturnFormat(JSON)
        sparql.setQuery(query)

        if self.username:
            sparql.setCredentials(self.username, self.password)

        print(f"Running query:\n{query}")

        return sparql.query().convert()
