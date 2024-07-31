import os
from dotenv import load_dotenv

load_dotenv()

MARIADB_HOST = os.getenv("MARIADB_HOST")
MARIADB_PORT = os.getenv("MARIADB_PORT", 3306)
MARIADB_DATABASE = os.getenv("MARIADB_DATABASE")
MARIADB_USER = os.getenv("MARIADB_USER", "root")
MARIADB_ROOT_PASSWORD = os.getenv("MARIADB_ROOT_PASSWORD")
