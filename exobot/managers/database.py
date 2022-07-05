import mysql.connector
from dotenv import dotenv_values

# Loading env config for database credentials
env_config = dotenv_values(".env")


db = mysql.connector.connect(
    host = env_config['DB_HOST'],
    user = env_config['DB_USER'],
    password = env_config['DB_PASS'],
    database = env_config['DB_SCHEMA']
)


cursor = db.cursor(dictionary=True)