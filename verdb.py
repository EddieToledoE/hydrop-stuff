import sqlite3

# Conecta a la base de datos SQLite
conn = sqlite3.connect('sensor_data.db')
c = conn.cursor()

# Ejecuta una consulta para obtener todos los registros
c.execute("SELECT * FROM data")

# Recupera todos los registros de la consulta
rows = c.fetchall()

# Imprime los registros
for row in rows:
    print(row)

# Cierra la conexión
conn.close()
