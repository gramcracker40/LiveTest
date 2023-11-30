# backend

### to test the backend
  simply run 'python API.py', this will launch the fastapi application and then you can try out various HTTP routes. Make sure you have the virtual environment sourced and active when you run it, as well as all the necessary dependencies in the requirements.txt

### documentation
  go to 'http://127.0.0.1:8000/docs'
  for more info on the various routes that the API implements. Such as the required parameters for the route, what the routes does, etc. There will also be info about JWT key passing. Acquire your access token through the 'login' route.


## models/
  pydantic models that handle data verification through the fastapi routers

## routers/
  fastapi routers that implement the various HTTP