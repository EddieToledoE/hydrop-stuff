import random
import paho.mqtt.client as mqtt
import serial
import json
import time

# Configuración del broker MQTT de CloudAMQP
broker_url = "toad.rmq.cloudamqp.com"
broker_port = 1883

# Credenciales MQTT
username = "jugilxxo:jugilxxo"
password = "aqvvDO1Y0hq2iW03wmz08TONcWdov1z0"

# Tema MQTT y mensaje
topic = "hydrop/668dee66cf7b5b0a30fb22a4/6699defcf167387f3335e144"

# Configuración del puerto serial (ajusta 'COM5' al puerto correcto en tu PC)
ser = serial.Serial('COM5', 115200)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado al broker MQTT!")
    else:
        print(f"Error de conexión, código de retorno: {rc}")

def on_publish(client, userdata, mid):
    print(f"Mensaje publicado con mid: {mid}")

def read_sensor_data():
    try:
        line = ser.readline().decode('utf-8').rstrip()
        print(f"Datos recibidos del sensor: {line}")
        if "Humedad" in line and "Temperatura" in line:
            parts = line.split("\t")
            humidity = float(parts[0].split(": ")[1].replace(" %", ""))
            temperature = float(parts[1].split(": ")[1].replace(" *C", ""))
            return {
                "humidity": humidity,
                "temperature": temperature
            }
    except Exception as e:
        print(f"Error al leer los datos del sensor: {e}")
    return None

def simulate_actuator_status():
    pump_status = random.choice(["on", "off"])
    nutrient_dispenser_status = random.choice(["on", "off"])
    return {
        "pump_status": pump_status,
        "nutrient_dispenser_status": nutrient_dispenser_status
    }

client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish
client.username_pw_set(username, password)
client.connect(broker_url, broker_port)
client.loop_start()

try:
    while True:
        sensor_data = read_sensor_data()
        if sensor_data:
            actuator_status = simulate_actuator_status()

            message = {
                "sensor_data": sensor_data,
                "actuator_status": actuator_status
            }

            json_message = json.dumps(message)  # Convertir el mensaje a JSON
            result = client.publish(topic, json_message)  # Enviar el mensaje como JSON
            result.wait_for_publish()

            print(f"Mensaje publicado: {json_message}")

        time.sleep(10)  # Espera de 10 segundos antes de enviar el siguiente mensaje
except KeyboardInterrupt:
    print("Interrupción del usuario. Desconectando...")

client.loop_stop()
client.disconnect()
