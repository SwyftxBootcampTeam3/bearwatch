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
CMD uvicorn app.api.server:app --reload --workers 1 --host 0.0.0.0 --port 8080
EXPOSE 8080
