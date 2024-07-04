FROM node:18-alpine
WORKDIR /app
COPY ../app .

# Change working directory to /app/src
WORKDIR /app/src

RUN npm install

EXPOSE 8001

# Run your application
CMD ["npm", "run", "dev"]
