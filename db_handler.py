import pandas as pd

def cargar_preguntas(ruta_excel):
    try:
        # Leer el Excel en un DataFrame
        df = pd.read_excel(ruta_excel)
        # Validar columnas necesarias
        columnas_esperadas = ['ID', 'Pregunta', 'Opción A', 'Opción B', 'Opción C', 'Opción D', 'Correcta']
        if not all(col in df.columns for col in columnas_esperadas):
            raise ValueError("El archivo no tiene el formato correcto.")
        return df
    except Exception as e:
        print(f"Error cargando preguntas: {e}")
        return None

