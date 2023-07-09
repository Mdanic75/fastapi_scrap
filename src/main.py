import json

from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from .settings import Settings
from .schemas import DataExtractionSchema, LinkDocumentSchema
import time

app = FastAPI()


@app.post("/scrap_data/")
async def scrap_data(data: DataExtractionSchema):
    from .utils import map_input_data
    from .celery import process_web_page
    links = map_input_data(data)
    for link in links:
        process_web_page.delay(link.model_dump_json())
    return {"links": links}


@app.get("/merge_data")
def merge_data():
    from .elastic_search import es_connection
    import csv
    import os
    csv_file_path = os.path.abspath('/code/src/sample-websites-company-names.csv')
    with open(csv_file_path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            payload = {
                "company_commercial_name": row[1],
                "company_legal_name": row[2],
                "company_all_available_names": row[3]
            }
            try:
                es_connection.update(index="domains", id=row[0], doc=payload)
            except:
                print(row[0])


@app.get("/get_company_profile")
async def get_company_profile(size: int, domain: str | None = None, phone_number: str | None = None) -> JSONResponse:
    from .elastic_search import es_connection
    query = {
        "bool": {
            "should": [
            ]
        }
    }
    if domain:
        query["bool"]["should"].append({"match": {"domain": domain}})
    if phone_number:
        query["bool"]["should"].append({"match": {"phone_numbers": phone_number}})
    response = es_connection.search(index="domains", body={"query": query, "size": size})
    return response.body

