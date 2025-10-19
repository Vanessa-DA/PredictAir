import requests  # Para enviar datos a Node-RED
import time

import random
import csv
from datetime import datetime

# Función para generar un dato aleatorio dentro del rango normal
def generar_dato(sensor):
    if sensor == "temperatura":
        return random.uniform(250, 1000)
    elif sensor == "presion":
        return random.uniform(15, 70)
    elif sensor == "vibracion":
        return random.uniform(0.1, 1.5)
    elif sensor == "rpm":
        return random.uniform(1500, 11000)

# Archivo CSV donde se guardan los datos
archivo_csv = "data/sensors_data.csv"

# Crear encabezados del archivo
with open(archivo_csv, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Fecha", "Temperatura (°C)", "Presión (psi)", "Vibración (mm/s)", "RPM"])

# Generar y guardar 20 muestras simuladas
for i in range(20):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    temperatura = round(generar_dato("temperatura"), 2)
    presion = round(generar_dato("presion"), 2)
    vibracion = round(generar_dato("vibracion"), 3)
    rpm = round(generar_dato("rpm"), 0)

    # Guardar en el archivo CSV
    with open(archivo_csv, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([fecha, temperatura, presion, vibracion, rpm])

    # Enviar a Node-RED
    datos = {
        "temperatura": temperatura,
        "presion": presion,
        "vibracion": vibracion,
        "rpm": rpm
    }

    try:
        respuesta = requests.post("http://127.0.0.1:1880/sensores", json=datos)
        if respuesta.status_code == 200:
            print(f"📡 Datos enviados: {datos}")
        else:
            print(f"Error al enviar datos: {respuesta.status_code}")
    except Exception as e:
        print(" No se pudo conectar a Node-RED:", e)

    # Esperar 3 segundos antes del siguiente envío
    time.sleep(3)

print("Envío de datos finalizado.")
