FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
COPY . /app

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    python3-pip  \
    libpq-dev \
    python-dev

RUN echo "alias python=python3" >> ~/.bashrc ; \
    echo "alias pip=pip3" >> ~/.bashrc

RUN pip install psycopg2 \
    sqlalchemy==1.4.26 \
    pytest==6.2.5 \
    requests==2.26.0

env PYTHONPATH=`pwd`
CMD [ "/start-reload.sh" ]