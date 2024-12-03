# actuator.py
#import RPi.GPIO as GPIO

# Clase Observador que representa un actuador (bomba, dispensador)
class Actuator:
    def __init__(self, name, gpio_pin):
        self.name = name
        self.status = "off"
        self.gpio_pin = gpio_pin
        #GPIO.setmode(GPIO.BCM)  # Usar el modo BCM para los pines GPIO
        #GPIO.setup(self.gpio_pin, GPIO.OUT)  # Configurar el pin del actuador como salida

    def update(self, subject):
        """Actualizar el estado del actuador"""
        self.status = subject.status
        print(f"{self.name} actualizado a {self.status}")

        # Encender o apagar el actuador según el estado
        if self.status == "on":
            #GPIO.output(self.gpio_pin, GPIO.HIGH)
            print(f"{self.name} encendido")
        else:
            #GPIO.output(self.gpio_pin, GPIO.LOW)
            print(f"{self.name} apagado")




class Subject:
    def __init__(self):
        self._observers = []
        self.status = "off" 

    def attach(self, observer):
        """Registrar un nuevo observador"""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        """Eliminar un observador"""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self):
        """Notificar a todos los observadores sobre un cambio de estado"""
        for observer in self._observers:
            observer.update(self)

    def set_status(self, status):
        """Cambiar el estado y notificar a los observadores"""
        self.status = status
        self.notify()
