import re

database_url_template = "DATABASE_URL=postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{SQL_HOST}:{SQL_PORT}/{POSTGRES_DB}"

# Placeholder values
values = {
    'POSTGRES_USER': 'your_user',
    'POSTGRES_PASSWORD': 'your_password',
    'SQL_HOST': 'your_host',
    'SQL_PORT': 'your_port',
    'POSTGRES_DB': 'your_database',
}

# Define a function to replace placeholders
def replace_placeholder(match):
    placeholder = match.group(1)
    return values.get(placeholder, placeholder)

# Use re.sub() to replace placeholders with actual values
database_url = re.sub(r'\{([^}]+)\}', replace_placeholder, database_url_template)

print(database_url)
