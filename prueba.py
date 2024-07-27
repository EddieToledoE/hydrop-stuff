import serial
import sqlite3
import time

# Configuración del puerto serial (ajusta 'COM5' al puerto correcto en tu PC)
ser = serial.Serial('COM5', 115200)

# Configuración de la base de datos SQLite
conn = sqlite3.connect('sensor_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS data
             (timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, humidity REAL, temperature REAL)''')

def insert_data(humidity, temperature):
    c.execute("INSERT INTO data (humidity, temperature) VALUES (?, ?)", (humidity, temperature))
    conn.commit()

while True:
    try:
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        if "Humedad" in line and "Temperatura" in line:
            parts = line.split("\t")
            humidity = float(parts[0].split(": ")[1].replace(" %", ""))
            temperature = float(parts[1].split(": ")[1].replace(" *C", ""))
            insert_data(humidity, temperature)
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(1)
