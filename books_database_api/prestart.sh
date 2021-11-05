#!/bin/bash
wait-for-it ${ELASTIC_SEARCH_URL}:${ELASTIC_SEARCH_PORT} -t 120
. /app/install-nltk-packages.sh