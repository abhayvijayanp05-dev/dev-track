import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def get_connection():
    connection = psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    return connection

def get_db():
    connection = get_connection()

    try:
        yield connection
    finally:
        connection.close()



        
        
# if __name__ == "__main__":
#     connection = get_connection()

#     cursor = connection.cursor()

#     cursor.execute(
#         """
#         INSERT INTO projects (id, name, status)
#         VALUES (%s, %s, %s)
#         """,
#         (1, "MentorLoop", "completed")
#     )

#     connection.commit()

#     print("Project inserted successfully! 🚀")

#     cursor.close()
#     connection.close()
#     connection = get_connection()

#     cursor = connection.cursor()

#     cursor.execute("SELECT * FROM projects")

#     rows = cursor.fetchall()

#     print(rows)

#     cursor.close()
#     connection.close()

