import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
import io
import tempfile
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Diccionario de respuestas y sus valores numéricos
respuesta_valores = {
    'Me motiva y me esfuerzo más': 0,
    'Me irrito y pierdo la paciencia': 1,
    'Me pongo pensativo y reflexiono': 2,
    'Me preocupa el resultado': 3,
    'Prefiero evitarlo': 4,
    'Busco distracciones agradables': 0,
    'Hablo con alguien sobre mi problema': 1,
    'Pienso en posibles soluciones': 2,
    'Me aíslo hasta calmarme': 3,
    'Intento no pensar en ello': 4,
    'Soy el alma de la fiesta': 0,
    'Participo activamente': 1,
    'Prefiero observar': 2,
    'Me siento nervioso': 3,
    'Voy porque debo ir': 4,
    'Lo tomo como una oportunidad de mejorar': 0,
    'Me molesta un poco': 1,
    'Me afecta y me entristece': 2,
    'Me pone ansioso': 3,
    'No le doy importancia': 4,
    'Aprendo de la experiencia': 0,
    'Me enfado al recordarlo': 1,
    'Me pongo nostálgico': 2,
    'Siento un nudo en el estómago': 3,
    'Me desagrada pensarlo': 4,
    'Disfruto de mi tiempo a solas': 0,
    'Busco algo para hacer': 1,
    'Me relajo y reflexiono': 2,
    'Me siento inquieto': 3,
    'Me aburro fácilmente': 4,
    'Lo veo como una aventura': 0,
    'Me molesta adaptarme': 1,
    'Me siento incómodo': 2,
    'Me pone nervioso': 3,
    'Quiero regresar a lo familiar': 4,
    'Busco la manera de solucionarlo': 0,
    'Expreso mi frustración': 1,
    'Me afecta emocionalmente': 2,
    'Me preocupo y dudo': 3,
    'Intento ignorarlo': 4,
    'Acepto el cambio positivamente': 0,
    'Me resisto un poco': 1,
    'Lo acepto con tristeza': 2,
    'Me da miedo': 3,
    'No me gusta el cambio': 4,
    'Me siento orgulloso y feliz': 0,
    'Me enfado por lo que no logré': 1,
    'Me da nostalgia': 2,
    'Me preocupa el futuro': 3,
    'Prefiero no pensar en ello': 4
}

def k_means():
    st.title('Análisis K-means')
    st.write("Por favor, sube un archivo CSV para importar datos y realizar un análisis con el algoritmo K-means.")

    uploaded_file = st.file_uploader("Subir archivo CSV", type="csv")

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write("Datos del archivo CSV:")
        st.dataframe(data)

        # Filtrar columnas para eliminar 'fecha', 'resultado', y 'marca temporal'
        columns_to_remove = ['fecha', 'resultado', 'marca temporal']
        columns = [col for col in data.columns if col.lower() not in [x.lower() for x in columns_to_remove]]

        # Selección de columnas
        selected_columns = st.multiselect("Selecciona las variables a utilizar", options=columns)
        
        if not selected_columns:
            selected_columns = columns  # Selecciona todas las columnas por defecto

        # Mostrar datos con columnas seleccionadas
        selected_data = data[selected_columns].copy()  # Crear una copia para evitar SettingWithCopyWarning
        
        st.write("Datos de las variables seleccionadas:")
        st.dataframe(selected_data)

        # Identificar y almacenar columnas no numéricas (como nombre o nombre completo)
        non_numeric_columns = [col for col in selected_columns if col.lower() in ['nombre', 'nombre completo']]
        numeric_columns = [col for col in selected_columns if col.lower() not in ['nombre', 'nombre completo']]
        
        # Convertir textos a números usando el diccionario en columnas numéricas
        for col in numeric_columns:
            if selected_data[col].dtype == 'object':
                selected_data[col] = selected_data[col].map(respuesta_valores)
        
        # Eliminar columnas no numéricas para el análisis K-means
        numeric_data = selected_data[numeric_columns].select_dtypes(include=[np.number])

        # Mantener las columnas no numéricas para mostrar
        display_data = selected_data.copy()
        
        st.write("Datos transformados:")
        st.dataframe(display_data)

        # Verificar si hay datos numéricos para continuar
        if numeric_data.empty:
            st.error("No hay datos numéricos disponibles para el análisis.")
            return

        # Normalización de datos
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(numeric_data)
        
        # Determinar el número óptimo de clusters usando el método del codo
        st.write("Determinación del número óptimo de clusters (Método del Codo):")

        inertia = []
        K = range(1, 11)
        for k in K:
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(scaled_data)
            inertia.append(kmeans.inertia_)

        # Graficar el método del codo
        fig_codo, ax_codo = plt.subplots(figsize=(6, 4))  # Ajustar tamaño de la figura
        ax_codo.plot(K, inertia, 'bx-')
        ax_codo.set_xlabel('Número de clusters')
        ax_codo.set_ylabel('Inercia')
        ax_codo.set_title('Método del Codo para Determinar el Número Óptimo de Clusters')
        st.pyplot(fig_codo)
        
        # Guardar la gráfica del codo en un archivo temporal
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file_codo:
            fig_codo.savefig(temp_file_codo.name, bbox_inches='tight', dpi=300)
            temp_file_codo.seek(0)
            temp_image_path_codo = temp_file_codo.name
        
        # Graficar los clusters
        fig_clusters, ax_clusters = plt.subplots(figsize=(6, 4))  # Ajustar tamaño de la figura
        
        # Determinar el número óptimo de clusters
        num_clusters = st.slider("Selecciona el número de clusters", min_value=2, max_value=10, value=3)
        st.write(f"Número de clusters seleccionado: {num_clusters}")

        # Entrenamiento del modelo K-means
        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        kmeans.fit(scaled_data)
        clusters = kmeans.labels_

        # Añadir las etiquetas de clusters al DataFrame original
        final_data = selected_data.copy()
        final_data['Cluster'] = clusters

        st.write("")
        st.write("Datos con etiquetas de clusters:")
        st.dataframe(final_data)

        # Reducir dimensiones para visualización 2D
        pca = PCA(n_components=2)
        reduced_data = pca.fit_transform(scaled_data)

        # Graficar los clusters
        scatter = ax_clusters.scatter(reduced_data[:, 0], reduced_data[:, 1], c=clusters, cmap='viridis')
        legend1 = ax_clusters.legend(*scatter.legend_elements(), title="Clusters")
        ax_clusters.add_artist(legend1)
        ax_clusters.set_xlabel('Componente 1')
        ax_clusters.set_ylabel('Componente 2')
        ax_clusters.set_title('Visualización de Clusters en 2D')
        st.pyplot(fig_clusters)
        
        # Guardar la gráfica de clusters en un archivo temporal
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file_clusters:
            fig_clusters.savefig(temp_file_clusters.name, bbox_inches='tight', dpi=300)
            temp_file_clusters.seek(0)
            temp_image_path_clusters = temp_file_clusters.name

        # Calcular y mostrar el puntaje de silueta
        silhouette_avg = silhouette_score(scaled_data, clusters)
        st.write(f"Puntaje promedio de silueta: {silhouette_avg:.2f}")
        st.write("")
        st.write("")

        # Exportar datos a Excel
        st.write("Exportar datos a Excel:")
        if st.button("Exportar a Excel"):
            # Crear un buffer de BytesIO para almacenar el archivo Excel en memoria
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                final_data.to_excel(writer, index=False, sheet_name='Datos con Clusters')
            output.seek(0)  # Volver al inicio del buffer
            st.success("Datos exportados a Excel exitosamente.")
            st.download_button(
                label="Descargar archivo Excel",
                data=output,
                file_name="datos_kmeans.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        st.write("")
        
        # Exportar gráfico a PDF
        st.write("Exportar gráficos a PDF:")
        if st.button("Exportar gráficos a PDF"):
            pdf_buffer = io.BytesIO()
            c = canvas.Canvas(pdf_buffer, pagesize=letter)

            # Gráfico del codo
            c.drawString(100, 750, "Método del Codo para Determinar el Número Óptimo de Clusters")
            c.drawImage(temp_image_path_codo, 100, 500, width=400, height=200)
            c.showPage()

            # Gráfico de clusters
            c.drawString(100, 750, "Visualización de Clusters en 2D")
            c.drawImage(temp_image_path_clusters, 100, 500, width=400, height=200)
            c.save()
            
            pdf_buffer.seek(0)
            st.success("Gráficos exportados a PDF exitosamente.")
            st.download_button(
                label="Descargar gráficos en PDF",
                data=pdf_buffer,
                file_name="graficos_kmeans.pdf",
                mime="application/pdf"
            )