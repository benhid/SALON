from pydantic import BaseSettings


class _BaseSettings(BaseSettings):
    ONTOLOGY_IRI: str = "https://w3id.org/salon#"
    ONTOLOGY_NAMESPACE: str = "salon"

    STARDOG_ENDPOINT: str = "http://localhost:5820"
    STARDOG_USERNAME: str = "admin"
    STARDOG_PASSWORD: str = "admin"
    STARDOG_DATABASE: str = "SALON"

    class Config:
        env_file = ".env"


settings = _BaseSettings()
