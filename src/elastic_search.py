from elasticsearch import Elasticsearch
from .settings import Settings

elastic_settings = Settings().elastic_search

es_connection = Elasticsearch([f"elastic://{elastic_settings.user}:{elastic_settings.password}@elasticsearch:{elastic_settings.port}"])
