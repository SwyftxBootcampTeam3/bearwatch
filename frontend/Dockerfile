FROM node:alpine3.11
ADD . /var/app
WORKDIR /var/app
ENV PATH="/var/app/node/modules/.bin/:${PATH}"
RUN npm install
RUN npm run build
CMD npm start
EXPOSE 3000