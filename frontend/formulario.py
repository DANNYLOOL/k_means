import streamlit as st
import numpy as np
import time
from database import obtener_respuestas, obtener_emociones
from backend.guardar_formulario import guardar_formulario

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

def mostrar_formulario():
    st.title('Test: ¿Qué emoción te representa?')

    st.write("Por favor, completa las siguientes preguntas con honestidad:")

    nombre = st.text_input('Nombre completo', placeholder='Escribe tu nombre completo')
    if nombre == '':
        st.warning('Por favor ingresa tu nombre completo')
    else:
        nombre = nombre.upper()
    
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

    respuestas_seleccionadas = []

    for i, pregunta in enumerate(preguntas):
        pregunta_numero = i + 1
        opciones = obtener_respuestas(pregunta_numero)
        respuesta_dict = {f"{opcion[1]}": opcion[0] for opcion in opciones}
        respuesta_options = [''] + list(respuesta_dict.keys())
        seleccion = st.selectbox(pregunta, respuesta_options, key=pregunta_numero, help='Selecciona tu respuesta')
        respuesta_id = respuesta_dict.get(seleccion, '')
        respuestas_seleccionadas.append(respuesta_id)
        if seleccion == '':
            st.warning(f'Por favor selecciona tu respuesta')
    
    form_valido = nombre != '' and all(respuesta != '' for respuesta in respuestas_seleccionadas)

    if st.button('Enviar', disabled=not form_valido):
        if form_valido:
            # Convertir respuestas seleccionadas a valores numéricos de tipo int
            respuestas_numericas = [int(respuesta) for respuesta in respuestas_seleccionadas]
            respuestas_array = np.array(respuestas_numericas).reshape(1, -1)
            
            # Verificar que no haya NaNs en las respuestas
            if not np.isnan(respuestas_array).any():
                # Obtener emociones desde la base de datos
                emociones = obtener_emociones()
                emociones_dict = {id: nombre for id, nombre in emociones}

                # Asignar emoción predominante basado en la respuesta más frecuente
                emocion_id = np.bincount(respuestas_array.flatten()).argmax()
                emocion_predominante = emocion_id  # Guardar el ID de la emoción

                # Guardar formulario en la base de datos
                form_data = (nombre,) + tuple(respuestas_numericas) + (int(emocion_predominante),) 
                guardar_formulario(form_data)

                emocion_nombre = emociones_dict[emocion_id]
                st.session_state.emocion_nombre = emocion_nombre

                st.session_state.pantalla = 'formulario_enviado'
                st.experimental_rerun()
            else:
                st.warning('Hay respuestas incompletas o no válidas. Por favor revisa tus respuestas.')
        else:
            st.warning('Por favor completa todos los campos antes de enviar el formulario')