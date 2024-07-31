import streamlit as st
import pandas as pd
import psycopg2
from psycopg2 import sql

# Diccionario actualizado para mapear valores a emociones
respuesta_emociones = {
    'Alegría': 1,
    'Enojo': 2,
    'Tristeza': 3,
    'Miedo': 4,
    'Desagrado': 5
}

# Diccionario para convertir valores de respuesta numéricos a texto
respuesta_valores = {
    'Me motiva y me esfuerzo más': 1,
    'Me irrito y pierdo la paciencia': 2,
    'Me pongo pensativo y reflexiono': 3,
    'Me preocupa el resultado': 4,
    'Prefiero evitarlo': 5,
    'Busco distracciones agradables': 1,
    'Hablo con alguien sobre mi problema': 2,
    'Pienso en posibles soluciones': 3,
    'Me aíslo hasta calmarme': 4,
    'Intento no pensar en ello': 5,
    'Soy el alma de la fiesta': 1,
    'Participo activamente': 2,
    'Prefiero observar': 3,
    'Me siento nervioso': 4,
    'Voy porque debo ir': 5,
    'Lo tomo como una oportunidad de mejorar': 1,
    'Me molesta un poco': 2,
    'Me afecta y me entristece': 3,
    'Me pone ansioso': 4,
    'No le doy importancia': 5,
    'Aprendo de la experiencia': 1,
    'Me enfado al recordarlo': 2,
    'Me pongo nostálgico': 3,
    'Siento un nudo en el estómago': 4,
    'Me desagrada pensarlo': 5,
    'Disfruto de mi tiempo a solas': 1,
    'Busco algo para hacer': 2,
    'Me relajo y reflexiono': 3,
    'Me siento inquieto': 4,
    'Me aburro fácilmente': 5,
    'Lo veo como una aventura': 1,
    'Me molesta adaptarme': 2,
    'Me siento incómodo': 3,
    'Me pone nervioso': 4,
    'Quiero regresar a lo familiar': 5,
    'Busco la manera de solucionarlo': 1,
    'Expreso mi frustración': 2,
    'Me afecta emocionalmente': 3,
    'Me preocupo y dudo': 4,
    'Intento ignorarlo': 5,
    'Acepto el cambio positivamente': 1,
    'Me resisto un poco': 2,
    'Lo acepto con tristeza': 3,
    'Me da miedo': 4,
    'No me gusta el cambio': 5,
    'Me siento orgulloso y feliz': 1,
    'Me enfado por lo que no logré': 2,
    'Me da nostalgia': 3,
    'Me preocupa el futuro': 4,
    'Prefiero no pensar en ello': 5
}

# Preguntas para renombrar las columnas
preguntas = [
    "¿Cómo describes tu reacción al enfrentar un desafío?",
    "¿Qué sueles hacer cuando te sientes abrumado?",
    "¿Cómo te comportas en una reunión social?",
    "¿Qué piensas cuando alguien te hace una crítica constructiva?",
    "¿Cómo te sientes al recordar una experiencia negativa?",
    "¿Qué haces cuando estás solo en casa?",
    "¿Cómo reaccionas cuando te encuentras en una situación desconocida?",
    "¿Qué haces si te enfrentas a un problema inesperado?",
    "¿Cómo describes tu actitud hacia los cambios?",
    "¿Qué piensas cuando reflexionas sobre tus logros pasados?"
]

# Función para conectar a la base de datos
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
    except psycopg2.Error as e:
        print(f"Error al conectar a PostgreSQL: {e}")
        return None

# Función para obtener los datos del formulario
def obtener_datos_formulario():
    conn = connect()
    if conn is not None:
        query = """
            SELECT nombre, pregunta1, pregunta2, pregunta3, pregunta4, pregunta5,
                   pregunta6, pregunta7, pregunta8, pregunta9, pregunta10, resultado, fecha
            FROM formulario
        """
        try:
            df = pd.read_sql_query(query, conn)
        except Exception as e:
            print(f"Error al obtener datos del formulario: {e}")
            df = pd.DataFrame()
        finally:
            conn.close()
        return df
    else:
        return pd.DataFrame()

# Función para exportar datos a CSV
def exportar():
    st.title('Exportar Formulario a CSV')
    st.write("Por favor, seleccione el botón 'Exportar', para exportar los datos recopilados del formulario a un archivo CSV.")
    # Obtener datos del formulario
    df = obtener_datos_formulario()
    
    if df.empty:
        st.write("No se pudieron obtener datos del formulario.")
        return
    
    # Renombrar las columnas
    df.columns = ['Nombre'] + preguntas + ['Resultado', 'Fecha']
    
    # Convertir valores de respuesta a texto
    for pregunta in preguntas:
        df[pregunta] = df[pregunta].map({v: k for k, v in respuesta_valores.items()})
    
    # Convertir resultado a texto si es necesario (similar a respuestas)
    df['Resultado'] = df['Resultado'].map({v: k for k, v in respuesta_emociones.items()})
    
    # Exportar a CSV
    csv = df.to_csv(index=False)
    st.download_button(
        label="Exportar",
        data=csv,
        file_name='test_emociones.csv',
        mime='text/csv'
    )