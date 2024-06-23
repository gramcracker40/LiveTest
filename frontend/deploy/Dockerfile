FROM node:18-alpine
EXPOSE 8001
WORKDIR /app
COPY ./frontend/app .
RUN npm install
CMD ["npm", "run", "dev"]
