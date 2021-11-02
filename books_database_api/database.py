import os
import time

from elasticsearch import Elasticsearch

time.sleep(20)
es = Elasticsearch(
    [os.getenv("ELASTIC_SEARCH_URL") or "books-elastics-db"],
    sniff_on_start=True,
    sniff_on_connection_fail=True,
    sniffer_timeout=60,
    port=os.getenv("ELASTIC_SEARCH_PORT") or 9200,
)

