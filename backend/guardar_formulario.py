from database import connect

def guardar_formulario(data):
    query = """
    INSERT INTO formulario (
        nombre, 
        pregunta1, 
        pregunta2, 
        pregunta3, 
        pregunta4, 
        pregunta5, 
        pregunta6, 
        pregunta7, 
        pregunta8, 
        pregunta9, 
        pregunta10,
        resultado
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    conn = connect()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query, data)
            conn.commit()
            print("Datos guardados correctamente")
        except Exception as e:
            print(f"Error al guardar los datos: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("No se pudo establecer conexión con la base de datos")
