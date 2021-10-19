import os
from elasticsearch import Elasticsearch

es = Elasticsearch(
    [os.getenv("ELASTIC_SEARCH_URL")],
    sniff_on_start=True,
    sniff_on_connection_fail=True,
    sniffer_timeout=60,
    port=os.getenv("ELASTIC_SEARCH_PORT"),
)

