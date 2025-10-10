"""
handles loading and abstraction of the .env file for the given instance.
"""

import os
import re
from dotenv import load_dotenv

load_dotenv()  # load .env into process env

def expand_db_template(url_template: str, env: dict | None = None) -> str:
    """
    Expands placeholders like postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{SQL_HOST}:{SQL_PORT}/{POSTGRES_DB}
    using environment variables. Leaves unknown placeholders as-is.
    """
    env = env or os.environ

    def repl(m: re.Match):
        key = m.group(1)
        return env.get(key, m.group(0))

    return re.sub(r"\{([^}]+)\}", repl, url_template or "")

template = os.getenv("DATABASE_URL", "")
database_url = expand_db_template(template)

docker_flag = os.getenv("DOCKER", "0")
if docker_flag.strip() in ("", "0", "false", "False", "FALSE", "no", "No"):
    # local dev DB (relative file)
    database_url = "sqlite:///./scantron-hacker.db"

secret_key = os.getenv("SECRET_KEY")
admin_user = os.getenv("ADMIN_USER", "").strip()
admin_pass = os.getenv("ADMIN_PASS", "").strip()
