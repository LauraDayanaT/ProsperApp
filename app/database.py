import psycopg2
def get_connection():
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database="prosperapp_db",
        user="admin",
        password="admin"
    )
    return connection