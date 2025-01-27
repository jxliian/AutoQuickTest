import random

class Quiz:
    def __init__(self, preguntas):
        self.preguntas = preguntas
        self.por_preguntar = preguntas.copy()
        self.ya_preguntadas = []
        self.falladas = {}

    def siguiente_pregunta(self):
        if not self.por_preguntar:
            return None  # No quedan preguntas.
        # Elegir aleatoriamente una pregunta
        pregunta = random.choice(self.por_preguntar)
        return pregunta

    def registrar_respuesta(self, pregunta_id, correcta):
        if correcta:
            self.por_preguntar.remove(pregunta_id)
            self.ya_preguntadas.append(pregunta_id)
        else:
            self.falladas[pregunta_id] = self.falladas.get(pregunta_id, 0) + 1
