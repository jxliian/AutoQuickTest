import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from db_handler import cargar_preguntas
from quiz_logic import Quiz

class App:
    def __init__(self, root):  # Constructor
        self.root = root
        self.root.title("Test de Preguntas")
        self.quiz = None

        # Botón para cargar la base de datos
        self.btn_cargar = tk.Button(root, text="Cargar BBDD", command=self.cargar_bbdd)
        self.btn_cargar.pack(pady=10)

        # Botones de control adicionales
        self.btn_reiniciar = tk.Button(root, text="Reiniciar", command=self.reiniciar)
        self.btn_reiniciar.pack(pady=5)

        self.btn_ir_final = tk.Button(root, text="Ir a la última", command=self.ir_al_final)
        self.btn_ir_final.pack(pady=5)

        self.btn_pasar = tk.Button(root, text="Pasar Pregunta", command=self.pasar_pregunta)
        self.btn_pasar.pack(pady=5)

        # Contenedor para las preguntas
        self.pregunta_label = tk.Label(root, text="", wraplength=400)
        self.pregunta_label.pack(pady=10)

        # Opciones
        self.opciones_var = tk.StringVar()
        self.opciones_frame = tk.Frame(root)
        self.opciones_frame.pack()

        # Botón para responder
        self.btn_responder = tk.Button(root, text="Responder", command=self.validar_respuesta)
        self.btn_responder.pack(pady=10)

        # Indicadores
        self.indicadores_frame = tk.Frame(root)
        self.indicadores_frame.pack(pady=10)

        self.lbl_total_preguntas = tk.Label(self.indicadores_frame, text="Total: 0")
        self.lbl_total_preguntas.grid(row=0, column=0, padx=10)

        self.lbl_restantes = tk.Label(self.indicadores_frame, text="Restantes: 0")
        self.lbl_restantes.grid(row=0, column=1, padx=10)

        self.lbl_acertadas = tk.Label(self.indicadores_frame, text="Acertadas: 0")
        self.lbl_acertadas.grid(row=1, column=0, padx=10)

        self.lbl_falladas = tk.Label(self.indicadores_frame, text="Falladas: 0")
        self.lbl_falladas.grid(row=1, column=1, padx=10)

        self.lbl_nota_media = tk.Label(self.indicadores_frame, text="Nota media: 0.0")
        self.lbl_nota_media.grid(row=2, column=0, columnspan=2, pady=5)

        self.lbl_pregunta_actual = tk.Label(self.indicadores_frame, text="Pregunta actual: 0")
        self.lbl_pregunta_actual.grid(row=3, column=0, columnspan=2, pady=5)

    def cargar_bbdd(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx")])
        preguntas = cargar_preguntas(ruta)
        if preguntas:
            self.quiz = Quiz(preguntas)
            self.mostrar_siguiente_pregunta()
            self.actualizar_indicadores()
        else:
            messagebox.showerror("Error", "No se pudo cargar el archivo.")

    def mostrar_siguiente_pregunta(self):
        if self.quiz:
            pregunta = self.quiz.siguiente_pregunta()
            if pregunta:
                self.pregunta_actual = pregunta
                self.pregunta_label.config(text=pregunta['Pregunta'])
                self.opciones_var.set("")
                for widget in self.opciones_frame.winfo_children():
                    widget.destroy()
                for key in ['A', 'B', 'C', 'D', 'E']:
                    opcion_texto = pregunta['Opciones'].get(key, "Opción no disponible")
                    tk.Radiobutton(
                        self.opciones_frame, text=opcion_texto, variable=self.opciones_var, value=key
                    ).pack(anchor="w")

                # Actualizar indicadores
                self.actualizar_indicadores()

            else:
                messagebox.showinfo("Fin", "Has respondido todas las preguntas.")
                self.actualizar_indicadores()

    def validar_respuesta(self):
        seleccion = self.opciones_var.get()
        if seleccion:
            # Verificar si la respuesta es correcta
            correcta = seleccion == self.pregunta_actual['Respuesta Correcta']
            
            # Registrar la respuesta, correcta o incorrecta
            self.quiz.registrar_respuesta(self.pregunta_actual['ID'], correcta)
            
            # Almacenar la respuesta de la pregunta (correcta o incorrecta)
            if correcta:
                self.quiz.ya_preguntadas.append({'ID': self.pregunta_actual['ID'], 'acertada': True})
            else:
                self.quiz.falladas[self.pregunta_actual['ID']] = self.quiz.falladas.get(self.pregunta_actual['ID'], 0) + 1
            
            # Mostrar la siguiente pregunta
            self.mostrar_siguiente_pregunta()
        else:
            messagebox.showwarning("Advertencia", "Selecciona una opción antes de continuar.")


    def reiniciar(self):
    
        # Reiniciar el cuestionario
        if self.quiz:
            # Restaurar las preguntas a las iniciales y vaciar las listas
            self.quiz.por_preguntar = self.quiz.preguntas.copy()  # Restablecer las preguntas pendientes
            self.quiz.ya_preguntadas = []  # Vaciar las preguntas respondidas
            self.quiz.falladas = {}  # Vaciar las preguntas falladas
            self.mostrar_siguiente_pregunta()  # Mostrar la primera pregunta
            self.actualizar_indicadores()  # Actualizar los indicadores


    def ir_al_final(self):
        # Ir directamente a la última pregunta
        if self.quiz:
            # Seleccionamos la última pregunta y la mostramos
            ultima_pregunta = self.quiz.preguntas[-1]
            self.pregunta_actual = ultima_pregunta
            self.pregunta_label.config(text=ultima_pregunta['Pregunta'])
            self.opciones_var.set("")
            for widget in self.opciones_frame.winfo_children():
                widget.destroy()
            for key in ['A', 'B', 'C', 'D', 'E']:
                opcion_texto = ultima_pregunta['Opciones'].get(key, "Opción no disponible")
                tk.Radiobutton(
                    self.opciones_frame, text=opcion_texto, variable=self.opciones_var, value=key
                ).pack(anchor="w")

            self.actualizar_indicadores()

    def pasar_pregunta(self):
    
        # Pasar a la siguiente pregunta sin responder
        if self.quiz:
            if self.quiz.por_preguntar:
                pregunta_actual = self.quiz.por_preguntar[0]  # Obtener la primera pregunta pendiente
                self.quiz.por_preguntar.append(pregunta_actual)  # Volver a agregar la pregunta sin responder
                self.quiz.por_preguntar.pop(0)  # Eliminar la pregunta de la lista pendiente
                self.mostrar_siguiente_pregunta()


    def actualizar_indicadores(self):
     if self.quiz:
         total_preguntas = len(self.quiz.preguntas)
         restantes = len(self.quiz.por_preguntar)
         acertadas = len(self.quiz.ya_preguntadas)  # Respuestas correctas
         falladas = len([p for p in self.quiz.falladas if p in self.quiz.ya_preguntadas])  # Respuestas incorrectas
         nota_media = self.calcular_nota_media()
         pregunta_actual = self.quiz.pregunta_actual['ID'] if self.quiz.pregunta_actual else "0"

         self.lbl_total_preguntas.config(text=f"Total: {total_preguntas}")
         self.lbl_restantes.config(text=f"Restantes: {restantes}")
         self.lbl_acertadas.config(text=f"Acertadas: {acertadas}")
         self.lbl_falladas.config(text=f"Falladas: {falladas}")
         self.lbl_nota_media.config(text=f"Nota media: {nota_media:.2f}")
         self.lbl_pregunta_actual.config(text=f"Pregunta actual: {pregunta_actual}")

    def calcular_nota_media(self):
     total_preguntas = len(self.quiz.preguntas)
     acertadas = len(self.quiz.ya_preguntadas)  # Solo preguntas correctas
     if total_preguntas > 0:
         return (acertadas / total_preguntas) * 10
     return 0.0


def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
