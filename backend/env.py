import os
from dotenv import load_dotenv

load_dotenv()

secret_key = os.getenv("SECRET_KEY")
database_url = os.getenv("DATABASE_URL")

