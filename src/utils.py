import requests
import asyncio
from typing import List
import ssl
import json
from .schemas import DataExtractionSchema, LinkDocumentSchema, BaseDocumentSchema
from .elastic_search import es_connection


def map_input_data(initial_data: DataExtractionSchema) -> List[LinkDocumentSchema]:
    links = []
    for domain in initial_data.domains:
        link = LinkDocumentSchema(link=f"https://{domain}", node_rank=1, max_rank=initial_data.node_max_rank,
                                  domain=domain)
        es_connection.create(index="links", id=link.link, document=link.model_dump_json())
        links.append(link)
        es_connection.create(index="domains", id=domain,
                             document={"domain": domain, "phone_numbers": [], "social_media_links": []})
    return links


def add_scrapped_data(domain: str, phone_numbers: List[str], social_media_links: List[str]):
    script_source = '''
            if(ctx._source.phone_numbers == null) {
                ctx._source.phone_numbers = new ArrayList(params.phone_numbers);
            } else {
                for (item in params.phone_numbers) { 
                    if (!ctx._source.phone_numbers.contains(item)) {
                        ctx._source.phone_numbers.add(item) 
                    }
                }
            }

            if(ctx._source.social_media_links == null) {
                ctx._source.social_media_links = new ArrayList(params.social_media_links);
            } else {
                for (item in params.social_media_links) { 
                    if (!ctx._source.social_media_links.contains(item)) {
                        ctx._source.social_media_links.add(item) 
                    }
                }
            }
        '''

    es_connection.update(
        index="domains",
        id=domain,
        body={
            "script": {
                "lang": "painless",
                "source": script_source,
                "params": {
                    "phone_numbers": phone_numbers,
                    "social_media_links": social_media_links
                }
            }
        }
    )
