import requests  # Para enviar datos a Node-RED
import time
import random
import csv
from datetime import datetime

# Rangos para evaluación rápida
rangos = {
    "temperatura": {"bajo": 300, "alto": 950},
    "presion": {"bajo": 20, "alto": 60},
    "vibracion": {"bajo": 0.2, "alto": 1.2},
    "rpm": {"bajo": 2000, "alto": 10000}
}

# Estado para predicción 
ultimo = {
    "temperatura": None,
    "presion": None,
    "vibracion": None,
    "rpm": None
}

# Estado SES (último pronóstico) para Temperatura y Presión
ses_forecast_temp = None
ses_forecast_pres = None

# Hiperparámetros SES (ajustables 0<α<1)
SES_ALPHA_TEMP = 0.3
SES_ALPHA_PRES = 0.25

def estado_pred_texto(sensor, pred):
    lim = rangos[sensor]
    riesgo = (pred < lim["bajo"]) or (pred > lim["alto"])
    return ("Riesgo Preventivo", True) if riesgo else ("Normal", False)

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

# Generar y enviar 20 muestras simuladas
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

    # --------- PREDICCIONES ---------
    # Vibración (naive t+1)
    pred_vib = ultimo["vibracion"] if ultimo["vibracion"] is not None else vibracion
    estado_vib, riesgo_vib = estado_pred_texto("vibracion", pred_vib)
    texto_pred_vib = f"Predicción Vibración: {pred_vib:.3f} mm/s ({estado_vib})"

    # Temperatura (SES)
    if ses_forecast_temp is None:
        ses_forecast_temp = temperatura  # inicialización
    pred_tmp = round(ses_forecast_temp, 2)  # pronóstico t+1 (antes de actualizar)
    estado_tmp, riesgo_tmp = estado_pred_texto("temperatura", pred_tmp)
    texto_pred_tmp = f"Predicción Temperatura (SES α={SES_ALPHA_TEMP}): {pred_tmp:.2f} °C ({estado_tmp})"
    # actualización SES: ŷ_{t+1} = α y_t + (1-α) ŷ_t
    ses_forecast_temp = SES_ALPHA_TEMP * temperatura + (1 - SES_ALPHA_TEMP) * ses_forecast_temp

    # Presión (SES)
    if ses_forecast_pres is None:
        ses_forecast_pres = presion
    pred_pre = round(ses_forecast_pres, 2)
    estado_pre, riesgo_pre = estado_pred_texto("presion", pred_pre)
    texto_pred_pre = f"Predicción Presión (SES α={SES_ALPHA_PRES}): {pred_pre:.2f} psi ({estado_pre})"
    ses_forecast_pres = SES_ALPHA_PRES * presion + (1 - SES_ALPHA_PRES) * ses_forecast_pres

    # RPM (naive t+1)
    pred_rpm = ultimo["rpm"] if ultimo["rpm"] is not None else rpm
    estado_rpm, riesgo_rpm = estado_pred_texto("rpm", pred_rpm)
    texto_pred_rpm = f"Predicción RPM: {pred_rpm:.0f} rpm ({estado_rpm})"

    # Actualizar últimos observados
    ultimo["vibracion"] = vibracion
    ultimo["temperatura"] = temperatura
    ultimo["presion"] = presion
    ultimo["rpm"] = rpm
    # --------------------------------

    # Enviar a Node-RED 
    datos = {
        "temperatura": temperatura,
        "presion": presion,
        "vibracion": vibracion,
        "rpm": rpm,

        # Vibración (naive)
        "prediccion_vibracion_t1": pred_vib,
        "prediccion_vibracion_texto": texto_pred_vib,
        "prediccion_vibracion_riesgo": riesgo_vib,

        # Temperatura (SES)
        "prediccion_temperatura_t1": pred_tmp,
        "prediccion_temperatura_texto": texto_pred_tmp,
        "prediccion_temperatura_riesgo": riesgo_tmp,

        # Presión (SES)
        "prediccion_presion_t1": pred_pre,
        "prediccion_presion_texto": texto_pred_pre,
        "prediccion_presion_riesgo": riesgo_pre,

        # RPM (naive)
        "prediccion_rpm_t1": pred_rpm,
        "prediccion_rpm_texto": texto_pred_rpm,
        "prediccion_rpm_riesgo": riesgo_rpm,

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

    
    time.sleep(3)

print("Envío de datos finalizado.")
