import os

from src.data.db_connection import DBConnection


def initialize_database():
    db = DBConnection()
    cursor = db.connection.cursor()

    with open('src/data/create_tables.sql', 'r') as file:
        sql = file.read()
        cursor.execute(sql)
        db.connection.commit()

    cursor.close()
