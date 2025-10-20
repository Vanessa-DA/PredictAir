import requests  # Para enviar datos a Node-RED
import time
import random
import csv
from datetime import datetime

# Rangos para evaluación rápida (coherentes con alerts.py)
rangos = {
    "temperatura": {"bajo": 300, "alto": 950},
    "presion": {"bajo": 20, "alto": 60},
    "vibracion": {"bajo": 0.2, "alto": 1.2},
    "rpm": {"bajo": 2000, "alto": 10000}
}

# Estado para predicción naive t+1 (solo vibración)
ultimo_vibracion = None

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

# Archivo CSV donde se guardan los datos (puedes ignorarlo si no lo usas)
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

    # --------- PREDICCIÓN NAIVE SOLO PARA VIBRACIÓN ---------
    # prediccion_t1 = último valor observado (si no hay último, usa el actual)
    pred_vib = ultimo_vibracion if ultimo_vibracion is not None else vibracion
    limites_vib = rangos["vibracion"]
    riesgo_preventivo_vib = (pred_vib < limites_vib["bajo"]) or (pred_vib > limites_vib["alto"])

    # Texto simple para widget ui_text en Node-RED
    # Ej: "Predicción Vibración: 0.84 mm/s (Normal)" o "… (Riesgo Preventivo)"
    estado_pred = "Riesgo Preventivo" if riesgo_preventivo_vib else "Normal"
    texto_prediccion_vibracion = f"Predicción Vibración: {pred_vib:.3f} mm/s ({estado_pred})"

    # Actualizar último valor
    ultimo_vibracion = vibracion
    # --------------------------------------------------------

    # Enviar a Node-RED (incluye el nuevo campo de texto para el widget)
    datos = {
        "temperatura": temperatura,
        "presion": presion,
        "vibracion": vibracion,
        "rpm": rpm,
        # Campos específicos para el widget de texto de Vibración
        "prediccion_vibracion_t1": pred_vib,
        "prediccion_vibracion_texto": texto_prediccion_vibracion,
        "prediccion_vibracion_riesgo": riesgo_preventivo_vib,
        "ts": fecha
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
