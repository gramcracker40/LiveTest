FROM node:18-alpine
EXPOSE 8001
WORKDIR /app
COPY ./app .
RUN npm install
CMD ["npm", "run", "dev"]