from tkinter import ttk

def aplicar_estilos():
    style = ttk.Style()
    
    # Configuración global de la ventana
    style.configure("TButton", font=("Segoe UI", 12), padding=10, relief="flat")
    style.configure("TLabel", font=("Segoe UI", 12), background="#2C2F33", foreground="white")
    
    # Botones
    style.configure("TButton", background="#7289DA", foreground="white")
    style.map("TButton", background=[('active', '#5B6EAE')])

    # Ajustar el fondo de la ventana
    style.configure("TFrame", background="#23272A")
    
    # Otros estilos que desees agregar
