from dotenv import load_dotenv
import os

load_dotenv()
# Read .env file

DB_NAME = os.getenv('CONFIG_COBRA_DB_NAME')
DB_HOST = os.getenv('CONFIG_COBRA_DB_USER')
DB_PORT = os.getenv('CONFIG_COBRA_DB_PORT')
DB_USER = os.getenv('CONFIG_COBRA_DB_HOST')
DB_PASSWORD = os.getenv('CONFIG_COBRA_DB_PASSWORD')