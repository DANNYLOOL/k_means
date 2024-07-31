import streamlit as st
from frontend import formulario
from frontend import formulario_enviado
from frontend import login
from frontend import exportar
from frontend import k_means

def main():
    st.markdown("""
    <style>
        [data-testid=stSidebar] {
            background-color: #555;
        }
        .sidebar-footer {
            position: absolute;
            top: 350px;
            color: white;
            font-size: 8px;
        }
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        # Título de la barra de navegación
        st.sidebar.markdown('<h1 style="color:white; font-size: 36px; text-align: center;">Test: Emociones</h1>', unsafe_allow_html=True)
        
        st.sidebar.markdown("---")  # Línea de separación
        
        if st.sidebar.button('Formulario', key='formulario_btn', on_click=lambda: st.session_state.update(pantalla='formulario'), use_container_width=True):
            st.session_state.pantalla = 'formulario'

        if st.sidebar.button('Exportar Formulario', key='exportar_btn', on_click=lambda: st.session_state.update(pantalla='exportar'), use_container_width=True):
            st.session_state.pantalla = 'exportar'

        if st.sidebar.button('K-means', key='k_means_btn', on_click=lambda: st.session_state.update(pantalla='k_means'), use_container_width=True):
            st.session_state.pantalla = 'k_means'

        st.sidebar.markdown("""
        <div class="sidebar-footer">
            <p style="font-size: 14px;"><strong>Autores:</strong></p>
            <p style="font-size: 14px;">Daniel Rangel Paredón</p>
            <p style="font-size: 14px;">Yolanda Valeria Chávez Zarate</p>
            <p style="font-size: 14px;">José Carlos Duarte Vázquez</p>
        </div>
        """, unsafe_allow_html=True)

    if 'pantalla' not in st.session_state:
        st.session_state.pantalla = 'formulario'

    # Renderizar las pantallas según el estado
    if st.session_state.pantalla == 'formulario':
        formulario.mostrar_formulario()
    elif st.session_state.pantalla == 'formulario_enviado':
        formulario_enviado.formulario_enviado()
    elif st.session_state.pantalla == 'login':
        login.login()
    elif st.session_state.pantalla == 'exportar':
        exportar.exportar()
    elif st.session_state.pantalla == 'k_means':
        k_means.k_means()
    
if __name__ == "__main__":
    main()
