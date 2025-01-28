import pandas as pd

def cargar_preguntas(ruta_archivo):
    try:
        df = pd.read_excel(ruta_archivo) # Cargar archivo Excel
        df = df.dropna(subset=['Pregunta', 'Opcion_A', 'Opcion_B', 'Opcion_C', 'Opcion_D', 'Opcion_E']) # Quitar filas con valores nulos
        df = df.drop_duplicates() # Eliminar filas duplicadas

        # Verifica que las columnas necesarias estén presentes
        required_columns = ['ID', 'Pregunta', 'Opcion_A', 'Opcion_B', 'Opcion_C', 'Opcion_D', 'Opcion_E', 'Respuesta_Correcta']
        # Si falta alguna columna, lanza un error
        for column in required_columns:
            if column not in df.columns:
                raise ValueError(f"Falta la columna requerida: {column}")
        preguntas = [] # Lista de preguntas

        # Ahora que sabemos que no hay valores nan en las preguntas o opciones
        for _, row in df.iterrows(): # Iterar sobre las filas del DataFrame
            pregunta = { # Crear un diccionario con la información de la pregunta
                'ID': row['ID'], # ID de la pregunta
                'Pregunta': row['Pregunta'], # Texto de la pregunta
                'Opciones': {   # Opciones de la pregunta
                    'A': row['Opcion_A'], # Opción A
                    'B': row['Opcion_B'], # Opción B
                    'C': row['Opcion_C'], # Opción C
                    'D': row['Opcion_D'], # Opción D
                    'E': row['Opcion_E'] # Opción E
                },
                'Respuesta Correcta': row['Respuesta_Correcta'] # Respuesta correcta
            }
            preguntas.append(pregunta) # Agregar la pregunta a la lista de preguntas

        print("Preguntas cargadas:", preguntas) # Imprimir las preguntas cargadas
        return preguntas # Devolver la lista de preguntas
    except FileNotFoundError:
        print(f"El archivo {ruta_archivo} no fue encontrado.")
        return []
    except pd.errors.EmptyDataError:
        print("El archivo está vacío.")
        return []
    except pd.errors.ParserError:
        print("Error al analizar el archivo.")
        return []
    except Exception as e: # Capturar cualquier otra excepción
        print(f"Error cargando preguntas: {e}") # Imprimir el error
        return []
 

