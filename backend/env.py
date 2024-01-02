'''
handles loading and abstraction of the .env file for the given instance. 
'''

import os, re
from dotenv import load_dotenv

def build_db_string(env_file) -> str:
    '''
    parse the beginning variables and identify remaining delimiters to fill
    builds database connection string according to 
        SQL_PORT
        SQL_HOST
        POSTGRES_USER
        POSTGRES_PASSWORD
        POSTGRES_DB
    '''
    env_file = open(env_file, "r").read()

    env_vars = {}
    for var in env_file.split('\n')[:-2]:
        key, value = var.split('=')
        env_vars[key] = value

    def replace_placeholder(match):
        placeholder = match.group(1)
        return env_vars.get(placeholder, placeholder)

    database_url = re.sub(r'\{([^}]+)\}', replace_placeholder, env_vars['DATABASE_URL'])
    return database_url

load_dotenv()
db_string = build_db_string(".env")
os.environ["DATABASE_URL"] = db_string

secret_key = os.getenv("SECRET_KEY")
database_url = os.getenv("DATABASE_URL")

print(f"DATABASE_URL: {database_url}")

test = build_db_string(".env")

