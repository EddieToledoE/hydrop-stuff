import paho.mqtt.client as mqtt
import tkinter as tk
import json

# Configuración del broker MQTT de CloudAMQP
broker_url = "toad.rmq.cloudamqp.com"
broker_port = 1883

# Credenciales MQTT
username = "jugilxxo:jugilxxo"
password = "aqvvDO1Y0hq2iW03wmz08TONcWdov1z0"

# Temas MQTT
pump_command_topic = "hydrop/668dee66cf7b5b0a30fb22a4/6699defcf167387f3335e144/pump/command"
nutrient_dispenser_command_topic = "hydrop/668dee66cf7b5b0a30fb22a4/6699defcf167387f3335e144/nutrient_dispenser/command"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado al broker MQTT!")
    else:
        print(f"Error de conexión, código de retorno: {rc}")

def on_publish(client, userdata, mid):
    print(f"Mensaje publicado con mid: {mid}")

def send_command(topic, command):
    message = json.dumps(command)
    result = client.publish(topic, message)
    result.wait_for_publish()
    print(f"Comando enviado en : {topic} {message}")

# Crear cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish
client.username_pw_set(username, password)
client.connect(broker_url, broker_port)
client.loop_start()

# Crear interfaz de Tkinter
root = tk.Tk()
root.title("Control de Actuadores")

# Botones para controlar la bomba
pump_label = tk.Label(root, text="Bomba de Agua")
pump_label.pack()

pump_on_button = tk.Button(root, text="Encender Bomba", command=lambda: send_command(pump_command_topic, {"pump_status": "on"}))
pump_on_button.pack()

pump_off_button = tk.Button(root, text="Apagar Bomba", command=lambda: send_command(pump_command_topic, {"pump_status": "off"}))
pump_off_button.pack()

# Botones para controlar el dispensador de nutrientes
nutrient_label = tk.Label(root, text="Dispensador de Nutrientes")
nutrient_label.pack()

nutrient_on_button = tk.Button(root, text="Encender Dispensador", command=lambda: send_command(nutrient_dispenser_command_topic, {"nutrient_dispenser_status": "on"}))
nutrient_on_button.pack()

nutrient_off_button = tk.Button(root, text="Apagar Dispensador", command=lambda: send_command(nutrient_dispenser_command_topic, {"nutrient_dispenser_status": "off"}))
nutrient_off_button.pack()

root.mainloop()

client.loop_stop()
client.disconnect()
