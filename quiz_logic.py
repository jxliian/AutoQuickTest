import random
import pandas as pd


class Quiz: # Clase Quiz
    def __init__(self, preguntas): # Constructor
        self.respuestas = []  # Lista de respuestas
        self.pregunta_actual = None  # Pregunta actual
        self.preguntas = preguntas  # Lista de preguntas
        self.por_preguntar = preguntas.copy()  # Preguntas pendientes
        self.ya_preguntadas = []  # Preguntas respondidas correctamente
        self.falladas = {}  # Conteo de preguntas falladas
        
        
    def siguiente_pregunta(self): # Método para obtener la siguiente pregunta
            """
            Selecciona una pregunta, ponderada por los fallos. 
            """ 
            if not self.por_preguntar: # Si no quedan preguntas por preguntar
                return None  # No quedan preguntas por preguntar 
            
            # Ponderar preguntas falladas
            preguntas_ponderadas = sorted(self.por_preguntar, key=lambda p: self.falladas.get(p['ID'], 0), reverse=True)
            return preguntas_ponderadas[0]


    def registrar_respuesta(self, pregunta_id, correcta):
        """
        Actualiza las listas según si la respuesta es correcta o no.
        """
        if correcta: # Si la respuesta es correcta
            # Mover a ya preguntadas
            self.por_preguntar = [p for p in self.por_preguntar if p['ID'] != pregunta_id]
            self.ya_preguntadas.append(pregunta_id)
        else:
            # Incrementar contador de fallos
            self.falladas[pregunta_id] = self.falladas.get(pregunta_id, 0) + 1
