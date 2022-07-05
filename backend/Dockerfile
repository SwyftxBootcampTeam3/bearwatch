FROM python:3.8-slim-buster
WORKDIR /backend
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
# install system dependencies
RUN apt-get update \
    && apt-get -y install netcat gcc postgresql \
    && apt-get clean
# install python dependencies
RUN pip3 install --upgrade pip
COPY ./requirements.txt /backend/requirements.txt
RUN pip3 install -r requirements.txt
COPY . /backend