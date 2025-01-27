import tkinter as tk
from tkinter import filedialog
from db_handler import cargar_preguntas

def cargar_bbdd():
    ruta = filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx")])
    preguntas = cargar_preguntas(ruta)
    if preguntas is not None:
        print("Preguntas cargadas correctamente.")
    else:
        print("Error al cargar las preguntas.")

def main():
    root = tk.Tk()
    root.title("Aplicación de Test")
    # Botón para cargar BBDD
    btn_cargar = tk.Button(root, text="Cargar BBDD", command=cargar_bbdd)
    btn_cargar.pack()
    # Ejecutar ventana
    root.mainloop()

if __name__ == "__main__":
    main()
