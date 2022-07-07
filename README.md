# BearWatch: a crypto price alert notification tool

## Backend Requirements
  * [Docker](https://www.docker.com/).
  * [Docker Compose](https://docs.docker.com/compose/install/).

## Frontend Requirements ##

Node v14.17.4 (best to use NVM to manage node version)  
Yarn  

If you havent used react before. I highly reccomend going through these docs: https://beta.reactjs.org/
Once you have the correct version of node running, run ```yarn install``` to install the package dependanices.

## Backend Development ##
  
Start the backend by running command in root folder: 
```bash
docker-compose up -d --build
```
You can now open the browser and interact with the api documentation at: http://localhost:8000/docs

Flower - Celery monitoring tool dashboard can be accessed at: http://localhost:5556 

## Frontend Development ##

  Enter the `frontend` directory, install the NPM packages and start the live server using the `yarn` scripts:

```bash
cd frontend
yarn run start
```

  This will launch the app in your default web browser at http://localhost:3000