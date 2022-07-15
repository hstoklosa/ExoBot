from exobot.__init__ import env
import mysql.connector


db = mysql.connector.connect(
    host = env['DB_HOST'],
    user = env['DB_USER'],
    password = env['DB_PASS'],
    database = env['DB_SCHEMA']
)


cursor = db.cursor(dictionary=True)