# from tkinter import ttk

# def aplicar_estilos():
#     style = ttk.Style()
    
#     # Configuración global de la ventana
#     style.configure("TButton", font=("Segoe UI", 12), padding=10, relief="flat")
#     style.configure("TLabel", font=("Segoe UI", 12), background="#2C2F33", foreground="white")
    
#     # Botones
#     style.configure("TButton", background="#7289DA", foreground="white")
#     style.map("TButton", background=[('active', '#5B6EAE')])

#     # Ajustar el fondo de la ventana
#     style.configure("TFrame", background="#23272A")
    
#     # Otros estilos que desees agregar

from tkinter import ttk

def aplicar_estilos():
    style = ttk.Style()

    # Usar tema nativo o 'clam' para mejor personalización
    style.theme_use('clam')

    # Configuración global
    style.configure("TFrame", background="#1E1E2F")  # Fondo oscuro, elegante
    style.configure("TLabel", background="#1E1E2F", foreground="#E0E0E0", font=("Segoe UI", 13))
    
    # Botones principales
    style.configure("TButton",
                    background="#4A90E2",
                    foreground="white",
                    font=("Segoe UI Semibold", 12),
                    padding=8,
                    relief="flat",
                    borderwidth=0)
    style.map("TButton",
              background=[('active', '#357ABD'), ('pressed', '#2E5C9A')],
              foreground=[('disabled', '#AAAAAA')])

    # Radiobuttons
    style.configure("TRadiobutton",
                    background="#1E1E2F",
                    foreground="#CCCCCC",
                    font=("Segoe UI", 12))
    style.map("TRadiobutton",
              background=[('active', '#2A2A40')])

    # Entry (si usas)
    style.configure("TEntry",
                    fieldbackground="#2C2C44",
                    foreground="#E0E0E0",
                    bordercolor="#4A90E2",
                    padding=5)

    # Scrollbar (si usas)
    style.configure("Vertical.TScrollbar",
                    background="#2C2C44",
                    troughcolor="#1E1E2F",
                    bordercolor="#1E1E2F",
                    arrowcolor="#4A90E2")
