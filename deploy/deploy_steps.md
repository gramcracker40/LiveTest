# Development build/run commands for LiveTest
docker-compose --file deploy/docker-compose.yml build
docker-compose --file deploy/docker-compose.yml up


### Docker development for frontend/backend
  docker build -f backend/deploy/Dockerfile -t livetest_api .
  docker run -p 8000:8000 livetest_api

  docker build -f frontend/deploy/Dockerfile -t livetest .
  docker run -p 8001:8001 livetest
