import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from db_handler import cargar_preguntas
from quiz_logic import Quiz

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Test de Preguntas")
        self.quiz = None

        # Botón para cargar la base de datos
        self.btn_cargar = tk.Button(root, text="Cargar BBDD", command=self.cargar_bbdd)
        self.btn_cargar.pack(pady=10)

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

    def cargar_bbdd(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx")])
        preguntas = cargar_preguntas(ruta)
        if preguntas:
            self.quiz = Quiz(preguntas)
            self.mostrar_siguiente_pregunta()
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
                for opcion in ['Opción A', 'Opción B', 'Opción C', 'Opción D', 'Opción E']:
                    tk.Radiobutton(
                        self.opciones_frame, text=pregunta[opcion], variable=self.opciones_var, value=opcion[-1]
                    ).pack(anchor="w")
            else:
                messagebox.showinfo("Fin", "Has respondido todas las preguntas.")

    def validar_respuesta(self):
        seleccion = self.opciones_var.get()
        if seleccion:
            correcta = seleccion == self.pregunta_actual['Correcta']
            self.quiz.registrar_respuesta(self.pregunta_actual['ID'], correcta)
            self.mostrar_siguiente_pregunta()
        else:
            messagebox.showwarning("Advertencia", "Selecciona una opción antes de continuar.")

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
