import sqlite3
from sqlite3 import Error
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

engine = create_engine('sqlite:///hydrop_local.db', poolclass=QueuePool,pool_size=6,max_overflow=10,pool_timeout=30,pool_recycle=1800)

Session = sessionmaker(bind=engine)
session = Session()


# Función para crear las tablas en la base de datos
def create_tables():
    # Definir las consultas SQL como texto
    create_sensor_data_table = """
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ph REAL,
            ec REAL,
            humidity REAL,
            temperature REAL,
            water_temp REAL,
            water_level REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """

    create_pump_status_table = """
        CREATE TABLE IF NOT EXISTS pump_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pump_status TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """

    create_nutrient_dispenser_status_table = """
        CREATE TABLE IF NOT EXISTS nutrient_dispenser_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nutrient_dispenser_status TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """

    # Ejecutar las consultas utilizando engine.execute()
    with engine.connect() as conn:
        conn.execute(text(create_sensor_data_table))
        conn.execute(text(create_pump_status_table))
        conn.execute(text(create_nutrient_dispenser_status_table))
    print("Tablas creadas con éxito.")

# Función para guardar los datos del sensor
def save_sensor_data(ph,ec, humidity, temperature,water_temp, water_level):
    session = Session()
    try:
        query = text("""
            INSERT INTO sensor_data (ph,ec,humidity, temperature, water_temp, water_level)
            VALUES (:ph, :ec, :humidity, :temperature, :water_temp, :water_level)
        """)
        session.execute(query, {'ph': ph, 'ec': ec, 'humidity': humidity, 'temperature': temperature, 'water_temp': water_temp, 'water_level': water_level})
        session.commit()
    except Error as e:
        session.rollback() 
        print(f"Error al guardar los datos del sensor: {e}")
    finally:
        session.close()  # Cerramos la sesión
# Función para guardar el estado de los actuadores
def save_pump_status(pump_status):
    try:
        query = text("""
            INSERT INTO pump_status (pump_status)
            VALUES (:pump_status)
        """)
        session.execute(query, {'pump_status': pump_status})
        session.commit()
    except Error as e:
        session.rollback() 
        print(f"Error al guardar el estado del actuador: {e}")
    finally:
        session.close()

def save_nutrient_dispenser_status(nutrient_dispenser_status):
    session = Session()
    try:
        query = text("""
            INSERT INTO nutrient_dispenser_status (nutrient_dispenser_status)
            VALUES (:nutrient_dispenser_status)
        """)
        session.execute(query, {'nutrient_dispenser_status': nutrient_dispenser_status})
        session.commit()
    except Error as e:
        session.rollback()
        print(f"Error al guardar el estado del actuador: {e}")
    finally:
        session.close()

# Función para cerrar la conexión
def close_connection():
    if session:
        session.close()
        print("Conexión cerrada")
