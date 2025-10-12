FROM node:20-alpine
WORKDIR /app
COPY ../app .

WORKDIR /app/src

RUN npm install

EXPOSE 8001
CMD ["npm", "run", "dev"]
