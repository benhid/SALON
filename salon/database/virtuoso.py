import re
from typing import Dict

import httpx
from httpx import Response

from salon.database.repository import RDFRepository


class Virtuoso(RDFRepository):
    """
    SPARQLWrapper for Virtuoso graph store.
    """

    COMMENTS_PATTERN = re.compile(r"(^|\n)\s*#.*?\n")

    def __init__(self, endpoint: str, database: str, username: str = None, password: str = None):
        super().__init__(endpoint, database, username, password)

        self.parameters: Dict[str, str] = {}
        self.headers: Dict[str, str] = {}

        self._setup_request()

    def _setup_request(self) -> None:
        self._add_parameter("default-graph-uri", self.database)
        self._add_parameter("User-Agent", "salon")

        self._add_header(
            "Accept",
            "application/sparql-results+json,application/json,text/javascript,application/javascript",
        )

    def query(self, query: str) -> dict:
        """
        Run 'SELECT' query with http Auth DIGEST and return results in JSON format.
        Protocol details at http://www.w3.org/TR/sparql11-protocol/#query-operation
        """
        self._add_parameter("query", query)
        req = self._get()

        # convert to json and return bindings
        result = {}
        if not req.is_error:
            result = req.json()
            result = result["results"]["bindings"]

        self._remove_parameter("query")

        return result

    def update(self, query: str) -> None:
        """
        Run 'INSERT' update query with http Auth DIGEST.
        Protocol details at http://www.w3.org/TR/sparql11-protocol/#update-operation
        """
        self._add_header("Content-Type", "application/sparql-update")

        req = self._post_directly(query)

        # convert to json and return bindings
        result = {}
        if not req.is_error:
            result = req.json()
            result = result["results"]["bindings"]

        self._remove_header("Content-Type")

        return result

    def _post_directly(self, query: str) -> Response:
        auth = httpx.DigestAuth(self.username, self.password)
        with httpx.Client(timeout=12000) as client:
            req = client.post(
                self.endpoint,
                data=query,
                params=self.parameters,
                headers=self.headers,
                auth=auth,
            )
        if req.is_error:
            print(req.text, req.status_code)
        return req

    def _get(self) -> Response:
        auth = httpx.DigestAuth(self.username, self.password)
        with httpx.Client() as client:
            req = client.post(
                self.endpoint,
                params=self.parameters,
                headers=self.headers,
                auth=auth,
            )
        if req.is_error:
            print(req.text, req.status_code)
        return req

    def _add_header(self, param: str, value: str) -> None:
        """
        Adds new custom header to request.
        """
        self.headers[param] = value

    def _remove_header(self, param: str) -> None:
        """
        Deletes header from request.
        """
        try:
            del self.headers[param]
        except KeyError:
            pass

    def _add_parameter(self, param: str, value: str) -> None:
        """
        Adds new parameter to request.
        """
        self.parameters[param] = value

    def _remove_parameter(self, param: str) -> None:
        """
        Deletes parameter from request.
        """
        try:
            del self.parameters[param]
        except KeyError:
            pass
