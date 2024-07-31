# database.py
import psycopg2
from psycopg2 import Error, sql

# Función para establecer la conexión a PostgreSQL
def connect():
    try:
        conn = psycopg2.connect(
            dbname="aplicacion_python",
            user="postgres",
            password="password",
            host="localhost",
            port="5432"
        )
        return conn
    except Error as e:
        print(f"Error al conectar a PostgreSQL: {e}")
        return None

# Función para obtener respuestas desde la base de datos
def obtener_respuestas(pregunta_numero):
    conn = connect()
    respuestas = []
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = sql.SQL("SELECT id, respuesta FROM {}").format(sql.Identifier(f'pregunta{pregunta_numero}'))
            cursor.execute(query)
            respuestas = cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener las respuestas de la pregunta {pregunta_numero}: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        print(f"No se pudo establecer conexión con la base de datos para la pregunta {pregunta_numero}")
    return respuestas

# Función para obtener emociones desde la base de datos
def obtener_emociones():
    conn = connect()
    emociones = []
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre FROM emociones")
            emociones = cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener las emociones: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("No se pudo establecer conexión con la base de datos para obtener las emociones")
    return emociones