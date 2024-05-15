import tkinter as tk

class MensajesApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Ejemplo de mensajes")

        self.frame = tk.Frame(self.master)
        self.frame.pack(padx=10, pady=10)

        self.btn_mensaje1 = tk.Button(self.frame, text="Mensaje 1", command=lambda: self.mostrar_mensaje("¡Hola! Soy el mensaje 1."))
        self.btn_mensaje1.pack(side=tk.LEFT)

        self.btn_mensaje2 = tk.Button(self.frame, text="Mensaje 2", command=lambda: self.mostrar_mensaje("¡Hola! Soy el mensaje 2."))
        self.btn_mensaje2.pack(side=tk.LEFT)

        self.label_mensaje = tk.Label(self.master, text="", font=("Arial", 14))
        self.label_mensaje.pack(pady=10)

    def mostrar_mensaje(self, mensaje):
        self.label_mensaje.config(text=mensaje)

def main():
    ventana = tk.Tk()
    app = MensajesApp(ventana)
    ventana.mainloop()

if __name__ == "__main__":
    main()
