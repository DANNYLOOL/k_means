import streamlit as st

def formulario_enviado():
    st.title('Test: ¿Qué emoción te representa?')

    emocion_nombre = st.session_state.emocion_nombre
    st.write(f'El formulario se ha enviado correctamente. Tu emoción predominante es: **"{emocion_nombre}"**.')

    if st.button('Ir al formulario'):
        st.session_state.pantalla = 'formulario'
        st.rerun()