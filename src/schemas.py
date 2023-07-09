from pydantic import BaseModel, HttpUrl
from typing import List, Optional


class DataExtractionSchema(BaseModel):
    node_max_rank: int
    domains: List[str]


class BaseDocumentSchema(BaseModel):
    domain: str
    phone_numbers: List[str] | None = []
    social_media_links: List[str] | None = []


class LinkDocumentSchema(BaseModel):
    link: str
    parent_link: str | None = ""
    domain: str
    phone_numbers: List[str] | None = []
    social_media_links: List[str] | None = []
    node_rank: int
    max_rank: int
