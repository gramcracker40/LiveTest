import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="../")

secret_key = os.getenv("SECRET_KEY")
database_url = os.getenv("DATABASE_URL")

