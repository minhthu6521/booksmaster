FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
COPY . /app

ENV ELASTIC_SEARCH_URL=${ELASTIC_SEARCH_URL:-books-elastics-db}
ENV ELASTIC_SEARCH_PORT=${ELASTIC_SEARCH_PORT:-9200}

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    python3-pip  \
    libpq-dev \
    python-dev \
    wait-for-it

RUN echo "alias python=python3" >> ~/.bashrc ; \
    echo "alias pip=pip3" >> ~/.bashrc

RUN pip install psycopg2 \
    sqlalchemy==1.4.26 \
    cleantext-tn==0.0.6 \
    elasticsearch==7.15.1 \
    nltk

CMD [ "wait-for-it", '${ELASTIC_SEARCH_URL}:${ELASTIC_SEARCH_PORT}', '-t', '120' ]


CMD [ "/start-reload.sh" ]

