FROM python:3.8-slim

RUN apt-get update && apt-get install

RUN apt-get install -y \
    && apt-get clean

RUN python -m pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt

COPY . .
