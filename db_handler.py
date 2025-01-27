import pandas as pd

def cargar_preguntas(ruta_archivo):
    try:
        df = pd.read_excel(ruta_archivo)
        df = df.dropna(subset=['Pregunta', 'Opcion_A', 'Opcion_B', 'Opcion_C', 'Opcion_D', 'Opcion_E'])
            
        # Verifica que las columnas necesarias estén presentes
        required_columns = ['ID', 'Pregunta', 'Opcion_A', 'Opcion_B', 'Opcion_C', 'Opcion_D', 'Opcion_E', 'Respuesta_Correcta']
        for column in required_columns:
            if column not in df.columns:
                raise ValueError(f"Falta la columna requerida: {column}")
        preguntas = []

        # Filtra las filas que no tienen preguntas o opciones válidas
        df = df.dropna(subset=['Pregunta', 'Opcion_A', 'Opcion_B', 'Opcion_C', 'Opcion_D', 'Opcion_E'])

        # Ahora que sabemos que no hay valores nan en las preguntas o opciones
        for _, row in df.iterrows():
            pregunta = {
                'ID': row['ID'],
                'Pregunta': row['Pregunta'],
                'Opciones': {
                    'A': row['Opcion_A'],
                    'B': row['Opcion_B'],
                    'C': row['Opcion_C'],
                    'D': row['Opcion_D'],
                    'E': row['Opcion_E']
                },
                'Respuesta Correcta': row['Respuesta_Correcta']
            }
            preguntas.append(pregunta)

        print("Preguntas cargadas:", preguntas)
        return preguntas
    except Exception as e:
        print(f"Error cargando preguntas: {e}")
        return []


