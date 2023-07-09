from celery import Celery
from .settings import Settings
from .scrap_utils import Scraper
from .schemas import LinkDocumentSchema
from .utils import add_scrapped_data
from typing import List
import json


redis_settings = Settings().redis
redis_url = f"redis://{redis_settings.host}:{redis_settings.port}"

celery_app = Celery(
    "fastapi_scrap",
    broker=redis_url,
    backend=redis_url
)


def map_links(links: List[str], parent_link_doc: LinkDocumentSchema) -> List[LinkDocumentSchema]:
    links_docs = []
    for link in links:
        links_docs.append(LinkDocumentSchema(link=link, parent_link=parent_link_doc.link, domain=parent_link_doc.domain,
                                             node_rank=parent_link_doc.node_rank+1, max_rank=parent_link_doc.max_rank))
    return links_docs


@celery_app.task(max_retires=0)
def process_web_page(link: json):
    from .elastic_search import es_connection
    import requests
    link = LinkDocumentSchema.model_validate_json(link)
    web_html = requests.get(link.link).text
    scrapper = Scraper(web_html)
    if len(scrapper.social_media_links) != 0 or len(scrapper.phone_numbers) != 0:
        link.social_media_links = scrapper.social_media_links
        link.phone_numbers = scrapper.phone_numbers
        try:
            add_scrapped_data(link.domain, link.phone_numbers, link.social_media_links)
        except:
            pass
    if link.node_rank < link.max_rank:
        new_links = map_links(scrapper.links, link)
        for new_link in new_links:
            try:
                es_connection.create(index="links", id=new_link.link, document=new_link.model_dump_json())
                process_web_page.delay(new_link.model_dump_json())
            except:
                pass