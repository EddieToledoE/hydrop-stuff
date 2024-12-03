import tkinter as tk
from tkinter import ttk
import sqlite3



conn = sqlite3.connect('hydrop_local.db')
c = conn.cursor()


# Función para obtener los datos de la tabla 'sensor_data'
def fetch_sensor_data(conn):
    c.execute("SELECT * FROM sensor_data")
    rows = c.fetchall()
    return rows

# Función para obtener los datos de la tabla 'pump_status'
def fetch_pump_status(conn):
    c.execute("SELECT * FROM pump_status")
    rows = c.fetchall()
    return rows

# Función para obtener los datos de la tabla 'nutrient_dispenser_status'
def fetch_nutrient_dispenser_status(conn):
    c.execute("SELECT * FROM nutrient_dispenser_status")
    rows = c.fetchall()
    return rows

# Crear la ventana de Tkinter
def create_ui():
    root = tk.Tk()
    root.title("Vista de la base de datos")

    # Crear la pestaña de sensores
    tab_control = ttk.Notebook(root)

    # Crear la tabla de sensores
    sensor_tab = ttk.Frame(tab_control)
    tab_control.add(sensor_tab, text="Datos del Sensor")

    tree_sensor = ttk.Treeview(sensor_tab, columns=("ID", "pH", "EC", "Humedad", "Temperatura", "Temp. Agua", "Nivel Agua", "Fecha"))
    tree_sensor.heading("#1", text="ID")
    tree_sensor.heading("#2", text="pH")
    tree_sensor.heading("#3", text="EC")
    tree_sensor.heading("#4", text="Humedad")
    tree_sensor.heading("#5", text="Temperatura")
    tree_sensor.heading("#6", text="Temp. Agua")
    tree_sensor.heading("#7", text="Nivel Agua")
    tree_sensor.heading("#8", text="Fecha")

    tree_sensor.column("#1", width=50)
    tree_sensor.column("#2", width=100)
    tree_sensor.column("#3", width=100)
    tree_sensor.column("#4", width=100)
    tree_sensor.column("#5", width=100)
    tree_sensor.column("#6", width=100)
    tree_sensor.column("#7", width=100)
    tree_sensor.column("#8", width=150)

    tree_sensor.pack(fill="both", expand=True)

    # Obtener los datos y mostrar en el Treeview
    conn = sqlite3.connect("mi_base_de_datos.db")
    sensor_data = fetch_sensor_data(conn)
    for row in sensor_data:
        tree_sensor.insert("", "end", values=row)

    # Crear la pestaña de estados de la bomba
    pump_tab = ttk.Frame(tab_control)
    tab_control.add(pump_tab, text="Estado de la Bomba")

    tree_pump = ttk.Treeview(pump_tab, columns=("ID", "Estado", "Fecha"))
    tree_pump.heading("#1", text="ID")
    tree_pump.heading("#2", text="Estado")
    tree_pump.heading("#3", text="Fecha")

    tree_pump.column("#1", width=50)
    tree_pump.column("#2", width=100)
    tree_pump.column("#3", width=150)

    tree_pump.pack(fill="both", expand=True)

    # Obtener los datos y mostrar en el Treeview
    pump_status_data = fetch_pump_status(conn)
    for row in pump_status_data:
        tree_pump.insert("", "end", values=row)

    # Crear la pestaña de dispensadores de nutrientes
    nutrient_tab = ttk.Frame(tab_control)
    tab_control.add(nutrient_tab, text="Estado del Dispensador de Nutrientes")

    tree_nutrient = ttk.Treeview(nutrient_tab, columns=("ID", "Estado", "Fecha"))
    tree_nutrient.heading("#1", text="ID")
    tree_nutrient.heading("#2", text="Estado")
    tree_nutrient.heading("#3", text="Fecha")

    tree_nutrient.column("#1", width=50)
    tree_nutrient.column("#2", width=100)
    tree_nutrient.column("#3", width=150)

    tree_nutrient.pack(fill="both", expand=True)

    # Obtener los datos y mostrar en el Treeview
    nutrient_status_data = fetch_nutrient_dispenser_status(conn)
    for row in nutrient_status_data:
        tree_nutrient.insert("", "end", values=row)

    tab_control.pack(expand=1, fill="both")

    root.mainloop()

if __name__ == "__main__":
    create_ui()
