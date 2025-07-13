import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from db_handler import cargar_preguntas
from quiz_logic import Quiz
from style import aplicar_estilos
import random
from PIL import Image, ImageTk # Para las imagenes 


class App:

    def __init__(self, root):  # Constructor
        self.root = root
        self.root.title("Test de Preguntas")

        # Cargar fondo y adaptar al tamaño de la ventana
        self.original_bg_image = Image.open("img/AutoQuickTest_carga.png")  # Cargar imagen de fondo
        self.bg_image = ImageTk.PhotoImage(self.original_bg_image.resize((1920, 1080)))  # tamaño inicial

        self.bg_label = tk.Label(self.root, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_label.lower()  # enviar al fondo

        self.root.bind("<Configure>", self.redimensionar_fondo)

        self.root.geometry("1280x720")
        self.root.update_idletasks()  # para que calcule todo bien

        # Centrar la ventana en pantalla
        ancho_ventana = 1280
        alto_ventana = 720
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()
        pos_x = (ancho_pantalla - ancho_ventana) // 2
        pos_y = (alto_pantalla - alto_ventana) // 2
        self.root.geometry(f"{ancho_ventana}x{alto_ventana}+{pos_x}+{pos_y}")

        self.frame_modos = tk.Frame(root)  # contenedor para centrar los botones de modo

        self.btn_modo_normal = tk.Button(self.frame_modos, text="Modo Normal",
                                        font=("Arial", 20), width=20, height=2,
                                        command=lambda: self.iniciar_modo(usar_random=False))
        self.btn_modo_aleatorio = tk.Button(self.frame_modos, text="Modo Aleatorio",
                                            font=("Arial", 20), width=20, height=2,
                                            command=lambda: self.iniciar_modo(usar_random=True))

        self.btn_modo_normal.pack(pady=20)
        self.btn_modo_aleatorio.pack(pady=20)

        # Aplicar estilos
        aplicar_estilos()

        self.quiz = None

        # Variables modo random y falladas
        self.modo_random = tk.BooleanVar(value=False)
        self.modo_falladas = tk.BooleanVar(value=False)

        # Botón cargar base de datos (visible al inicio)
        self.btn_cargar = tk.Button(root, text="Cargar BBDD", command=self.cargar_bbdd,
                                font=("Arial", 24),
                                width=20, height=3)
        self.btn_cargar.pack(expand=True)

        # Crear resto de widgets pero NO hacer pack todavía (no visibles)
        self.chk_falladas = tk.Checkbutton(root, text="Modo falladas", variable=self.modo_falladas)
        self.chk_modo = tk.Checkbutton(root, text="Modo aleatorio", variable=self.modo_random)

        self.btn_reiniciar = tk.Button(root, text="Reiniciar", command=self.reiniciar)
        self.btn_ir_final = tk.Button(root, text="Ir a la última", command=self.ir_al_final)
        self.btn_pasar = tk.Button(root, text="Pasar Pregunta", command=self.pasar_pregunta)

        self.pregunta_label = tk.Label(root, text="", wraplength=400)
        self.opciones_var = tk.StringVar()
        self.opciones_frame = tk.Frame(root)

        self.btn_responder = tk.Button(root, text="Responder", command=self.iniciar_fade_out)

        self.indicadores_frame = tk.Frame(root)
        self.lbl_total_preguntas = tk.Label(self.indicadores_frame, text="Total: 0")
        self.lbl_restantes = tk.Label(self.indicadores_frame, text="Restantes: 0")
        self.lbl_acertadas = tk.Label(self.indicadores_frame, text="Acertadas: 0")
        self.lbl_falladas = tk.Label(self.indicadores_frame, text="Falladas: 0")
        self.lbl_nota_media = tk.Label(self.indicadores_frame, text="Nota media: 0.0")
        self.lbl_pregunta_actual = tk.Label(self.indicadores_frame, text="Pregunta actual: 0")

        self.btn_cerrar = tk.Button(root, text="Cerrar", command=self.cerrar_aplicacion, bg="red", fg="white")

        # Configurar grid dentro de indicadores_frame
        self.lbl_total_preguntas.grid(row=0, column=0, padx=10)
        self.lbl_restantes.grid(row=0, column=1, padx=10)
        self.lbl_acertadas.grid(row=1, column=0, padx=10)
        self.lbl_falladas.grid(row=1, column=1, padx=10)
        self.lbl_nota_media.grid(row=2, column=0, columnspan=2, pady=5)
        self.lbl_pregunta_actual.grid(row=3, column=0, columnspan=2, pady=5)


    def redimensionar_fondo(self, event):
        if event.widget == self.root:
            nuevo_ancho = event.width
            nuevo_alto = event.height
            nueva_imagen = self.original_bg_image.resize((nuevo_ancho, nuevo_alto), Image.ANTIALIAS)
            self.bg_image = ImageTk.PhotoImage(nueva_imagen)
            self.bg_label.config(image=self.bg_image)


    def reset_interfaz(self):
        # Oculta todo lo visible menos el botón de cargar
        for widget in [self.frame_modos, self.chk_falladas, self.chk_modo,
                    self.btn_reiniciar, self.btn_ir_final, self.btn_pasar,
                    self.btn_responder, self.pregunta_label, self.opciones_frame,
                    self.indicadores_frame, self.btn_cerrar]:
            widget.pack_forget()

    def cargar_bbdd(self):
        self.reset_interfaz()
        ruta = filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx")])
        preguntas = cargar_preguntas(ruta)
        if preguntas:
            self.quiz = Quiz(preguntas)
            self.mostrar_siguiente_pregunta()
            self.actualizar_indicadores()

            # Iniciar fade out del botón cargar y mostrar controles luego
            self.fade_out_widget(self.btn_cargar)
        else:
            messagebox.showerror("Error", "No se pudo cargar el archivo.")


    def iniciar_fade_out(self):
        # Empieza el fade out, y al terminar valida la respuesta y hace fade in
        self.fade_out(step=0)

    def fade_out(self, step=0, steps=10, delay=50):
        # Ejemplo básico de fade out cambiando el color del botón responder (puedes adaptar a más widgets)
        start_bg = "#f0f0f0"  # Color actual (ajusta si usas otro)
        end_bg = "#2e2e2e"    # Color oscuro para fade out
        start_fg = "#000000"
        end_fg = "#2e2e2e"

        def hex_to_rgb(h):
            h = h.lstrip('#')
            return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

        def rgb_to_hex(rgb):
            return '#%02x%02x%02x' % rgb

        start_bg_rgb = hex_to_rgb(start_bg)
        end_bg_rgb = hex_to_rgb(end_bg)
        start_fg_rgb = hex_to_rgb(start_fg)
        end_fg_rgb = hex_to_rgb(end_fg)

        factor = step / steps
        new_bg = tuple(int(start_bg_rgb[i] + factor * (end_bg_rgb[i] - start_bg_rgb[i])) for i in range(3))
        new_fg = tuple(int(start_fg_rgb[i] + factor * (end_fg_rgb[i] - start_fg_rgb[i])) for i in range(3))

        self.btn_responder.config(bg=rgb_to_hex(new_bg), fg=rgb_to_hex(new_fg))

        if step < steps:
            self.root.after(delay, lambda: self.fade_out(step + 1, steps, delay))
        else:
            # Al terminar fade out, validar respuesta y comenzar fade in
            self.validar_respuesta()
            self.fade_in(step=0)

    def fade_in(self, step=0, steps=10, delay=50):
        # Fade in inverso del fade out para el botón responder
        start_bg = "#2e2e2e"
        end_bg = "#f0f0f0"
        start_fg = "#2e2e2e"
        end_fg = "#000000"

        def hex_to_rgb(h):
            h = h.lstrip('#')
            return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

        def rgb_to_hex(rgb):
            return '#%02x%02x%02x' % rgb

        start_bg_rgb = hex_to_rgb(start_bg)
        end_bg_rgb = hex_to_rgb(end_bg)
        start_fg_rgb = hex_to_rgb(start_fg)
        end_fg_rgb = hex_to_rgb(end_fg)

        factor = step / steps
        new_bg = tuple(int(start_bg_rgb[i] + factor * (end_bg_rgb[i] - start_bg_rgb[i])) for i in range(3))
        new_fg = tuple(int(start_fg_rgb[i] + factor * (end_fg_rgb[i] - start_fg_rgb[i])) for i in range(3))

        self.btn_responder.config(bg=rgb_to_hex(new_bg), fg=rgb_to_hex(new_fg))

        if step < steps:
            self.root.after(delay, lambda: self.fade_in(step + 1, steps, delay))


    def mostrar_selector_modo(self):
        self.frame_modos.pack(expand=True)
        self.chk_falladas.config(state='disabled')


    def iniciar_modo(self, usar_random=False):
        self.modo_random.set(usar_random)
        self.frame_modos.pack_forget()  # ocultar los botones de modo
        self.quiz.iniciar_modo(usar_random=usar_random)
        self.mostrar_siguiente_pregunta()
        self.actualizar_indicadores()
        self.mostrar_controles_post_carga()


    def fade_out_widget(self, widget, steps=10, delay=50):
        """
        Simula un fade out disminuyendo la intensidad del color de fondo y texto.
        Al terminar oculta el widget.
        """
        # Colores iniciales
        start_bg = "#0078D7"  # color original del botón cargar (puedes ajustarlo)
        start_fg = "white"

        # Convertir colores hex a RGB
        def hex_to_rgb(h):
            h = h.lstrip('#')
            return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

        def rgb_to_hex(rgb):
            return '#%02x%02x%02x' % rgb

        start_bg_rgb = hex_to_rgb(start_bg)
        start_fg_rgb = hex_to_rgb("#FFFFFF")

        def step_fade(i):
            if i > steps:
                widget.pack_forget()  # Ocultar al terminar
                # Mostrar los otros botones tras fade out
                # self.mostrar_controles_post_carga()
                self.mostrar_selector_modo()
                return
            
            factor = 1 - i/steps  # va de 1 a 0
            new_bg = tuple(int(c * factor + 46 * (1 - factor)) for c in start_bg_rgb)  # 46 es un gris oscuro de fondo
            new_fg = tuple(int(c * factor + 46 * (1 - factor)) for c in start_fg_rgb)

            widget.config(bg=rgb_to_hex(new_bg), fg=rgb_to_hex(new_fg))
            self.root.after(delay, lambda: step_fade(i+1))

        step_fade(0)


    def mostrar_controles_post_carga(self):
        self.chk_falladas.config(state='normal')
        self.chk_falladas.pack(pady=5)
        self.chk_modo.pack(pady=5)

        self.btn_reiniciar.pack(pady=5)
        self.btn_ir_final.pack(pady=5)
        self.btn_pasar.pack(pady=5)
        self.btn_responder.pack(pady=10)
        self.pregunta_label.pack(pady=10)
        self.opciones_frame.pack()
        self.indicadores_frame.pack(pady=10)
        self.btn_cerrar.pack(pady=10)

        # Empaqueta las etiquetas de indicadores con grid
        self.lbl_total_preguntas.grid(row=0, column=0, padx=10)
        self.lbl_restantes.grid(row=0, column=1, padx=10)
        self.lbl_acertadas.grid(row=1, column=0, padx=10)
        self.lbl_falladas.grid(row=1, column=1, padx=10)
        self.lbl_nota_media.grid(row=2, column=0, columnspan=2, pady=5)
        self.lbl_pregunta_actual.grid(row=3, column=0, columnspan=2, pady=5)


    def iniciar_carga(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx")])
        preguntas = cargar_preguntas(ruta)
        if preguntas:
            self.quiz = Quiz(preguntas)
            self.mostrar_siguiente_pregunta()
            self.actualizar_indicadores()

            # Iniciar fade out del botón cargar y mostrar controles luego
            self.fade_out_widget(self.btn_cargar)

        else:
            messagebox.showerror("Error", "No se pudo cargar el archivo.")

    #-------------------------------------  FADE OUT Y FADE IN -------------------------------------


    def validar_respuesta(self):
        seleccion = self.opciones_var.get()
        if seleccion:
            correcta = seleccion == self.pregunta_actual['Respuesta Correcta']
            
            # Registrar respuesta en el quiz
            self.quiz.registrar_respuesta(self.pregunta_actual['ID'], correcta)
            
            if correcta:
                if self.pregunta_actual['ID'] not in self.quiz.ya_preguntadas:
                    self.quiz.ya_preguntadas.append(self.pregunta_actual['ID'])

                if self.modo_random.get() and self.pregunta_actual in self.quiz.por_preguntar:
                    self.quiz.por_preguntar.remove(self.pregunta_actual)

                if self.modo_falladas.get():
                    # Eliminarla de falladas si ya estaba
                    if self.pregunta_actual['ID'] in self.quiz.falladas:
                        del self.quiz.falladas[self.pregunta_actual['ID']]
                
                self.mostrar_siguiente_pregunta()
            
            self.actualizar_indicadores()
        else:
            messagebox.showwarning("Advertencia", "Selecciona una opción antes de continuar.")

    def mostrar_siguiente_pregunta(self):
        if self.quiz:
            if self.modo_falladas.get():
                falladas_ids = list(self.quiz.falladas.keys())
                preguntas_falladas = [p for p in self.quiz.preguntas if p['ID'] in falladas_ids]

                if preguntas_falladas:
                    self.pregunta_actual = random.choice(preguntas_falladas)
                else:
                    messagebox.showinfo("Fin", "No hay preguntas falladas.")
                    return

            elif self.modo_random.get():
                if self.quiz.por_preguntar:
                    self.pregunta_actual = random.choice(self.quiz.por_preguntar)
                else:
                    messagebox.showinfo("Fin", "Has respondido todas las preguntas.")
                    return
            else:
                self.pregunta_actual = self.quiz.siguiente_pregunta()

            if self.pregunta_actual:
                self.pregunta_label.config(text=self.pregunta_actual['Pregunta'])
                self.opciones_var.set("")

                for widget in self.opciones_frame.winfo_children():
                    widget.destroy()

                for key in ['A', 'B', 'C', 'D', 'E']:
                    opcion_texto = self.pregunta_actual['Opciones'].get(key, "Opción no disponible")
                    tk.Radiobutton(
                        self.opciones_frame, text=opcion_texto, variable=self.opciones_var, value=key
                    ).pack(anchor="w")

                self.actualizar_indicadores()


    def reiniciar(self):
        if self.quiz:
            if self.modo_falladas.get():
                # No reseteamos las falladas, porque el modo depende de ellas
                pass
            else:
                self.quiz.por_preguntar = self.quiz.preguntas.copy()
                if self.modo_random.get():
                    random.shuffle(self.quiz.por_preguntar)
                self.quiz.ya_preguntadas = []
                self.quiz.falladas = {}

            self.mostrar_siguiente_pregunta()
            self.actualizar_indicadores()



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

    # Me quedado por aqui no va el modo, cuando se pone en random no va
    def pasar_pregunta_random(self):
        if self.quiz:
            if self.quiz.por_preguntar:
                random.shuffle(self.quiz.por_preguntar)
            self.mostrar_siguiente_pregunta()

    def actualizar_indicadores(self):
        if self.quiz:
            total_preguntas = len(self.quiz.preguntas)
            restantes = len(self.quiz.por_preguntar)
            acertadas = len(self.quiz.ya_preguntadas)
            fallos_totales = sum(self.quiz.falladas.values())
            preguntas_falladas = len(self.quiz.falladas)
            nota_media = self.calcular_nota_media()
            pregunta_actual = self.pregunta_actual['ID'] if hasattr(self, 'pregunta_actual') else "0"

            self.lbl_total_preguntas.config(text=f"Total: {total_preguntas}")
            self.lbl_restantes.config(text=f"Restantes: {restantes}")
            self.lbl_acertadas.config(text=f"Acertadas: {acertadas}")
            self.lbl_falladas.config(
                text=f"Falladas: {fallos_totales} ({preguntas_falladas} preguntas diferentes)"
            )
            self.lbl_nota_media.config(text=f"Nota media: {nota_media:.2f}")
            self.lbl_pregunta_actual.config(text=f"Pregunta actual: {pregunta_actual}")

    def calcular_nota_media(self):
        total_intentos = sum(self.quiz.falladas.values()) + len(self.quiz.ya_preguntadas)  # Total de intentos hechos
        acertadas = len(self.quiz.ya_preguntadas)  # Solo preguntas correctas

        if total_intentos > 0:
            return (acertadas / total_intentos) * 10  # Penaliza errores
        return 0.0
    
    def cerrar_aplicacion(self):
        self.root.destroy()  # Cierra la ventana y finaliza la ejecución del programa


def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
