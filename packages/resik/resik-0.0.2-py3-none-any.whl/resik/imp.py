
# the code is a example for a class and run not use terminal or command line



import time
class imprime:
    def __init__(self, mensaje):
        self.mensaje = mensaje

    def mostrar_mensaje(self):
        print(self.mensaje)


obj = imprime("¡Hola! Soy el mensaje 1.")
obj.mostrar_mensaje()
time.sleep(2)
