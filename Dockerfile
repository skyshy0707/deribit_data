FROM python:3.14.2-alpine3.23

WORKDIR /code
COPY ./src/ ./src
COPY ./requirements.txt ./requirements.txt

RUN set -eux \
    && apk add --no-cache --virtual .build-deps python3 py3-pip \
    && pip install --upgrade pip setuptools wheel \
    && pip install fastapi uvicorn

RUN pip install -r requirements.txt

WORKDIR /code/src

CMD python -m db.init_db; uvicorn main:app --host 0.0.0.0 --workers 4