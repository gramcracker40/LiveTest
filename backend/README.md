# backend

### to test the backend
  simply run 'python API.py', this will launch the fastapi application and then you can try out various HTTP routes. Make sure you have the virtual environment sourced and active when you run it, as well as all the necessary dependencies in the requirements.txt
  pip installed within the environment and ready to go. 

### documentation
  go to 'http://127.0.0.1:8000/docs'
  for more info on the various routes that the API implements. Such as the required parameters for the route, what the route does, etc. The API aims to be RESTful. 

## API.py
  builds the fastapi application using a factory pattern.

## core/ 
  core functionality of the application, includes the modules that perform
  the grading of answer sheets, creation of analytics, test processing, etc

## models/
  pydantic models that handle data verification through the fastapi routers

## routers/
  fastapi routers that implement the various HTTP

## db.py 
  handles creation of database tables and the db session maker. 

## tables.py 
  SQLAlchemy models defined for database creation and interaction. 

## jwt.py
  implements the security features of the app. 

## env.py
  grabs the instance details from the .env file and builds the db connection string

## .env 
  instance configuration file
