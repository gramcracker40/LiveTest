FROM node:18-buster-slim
WORKDIR /usr/src/app
COPY /app .
RUN npm install
EXPOSE 8001
CMD ["npm", "run", "dev"]