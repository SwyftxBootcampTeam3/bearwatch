FROM python:3.8-slim-buster
WORKDIR /backend
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
# install system dependencies
RUN apt-get update \
    && apt-get -y install netcat gcc postgresql \
    && apt-get clean
# install python dependencies
RUN pip install --upgrade pip
ADD ./backend/requirements.txt /backend/
RUN pip install -r requirements.txt
COPY ./backend /backend
CMD celery -A app.services.celery_worker.celery worker --loglevel=info
