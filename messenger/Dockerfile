FROM python:2.7-slim
MAINTAINER Patrick L. Lange <patrick.l.lange@gmail.com>

RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y --no-install-recommends curl

ENV INSTALL_PATH /messenger
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

WORKDIR /
CMD gunicorn --worker-class "eventlet" -b '0.0.0.0:8000' 'messenger:create_app()'
