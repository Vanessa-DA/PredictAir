import csv

# Definir rangos normales y límites de alerta
rangos = {
    "temperatura": {"bajo": 300, "alto": 950},
    "presion": {"bajo": 20, "alto": 60},
    "vibracion": {"bajo": 0.2, "alto": 1.2},
    "rpm": {"bajo": 2000, "alto": 10000}
}

# Función que determina el nivel de alerta de cada valor
def evaluar_alerta(sensor, valor):
    limites = rangos[sensor]
    if valor < limites["bajo"]:
        return "Alerta baja"
    elif valor > limites["alto"]:
        return "Alerta alta"
    else:
        return "🛫 Normal"

# Leer los datos del archivo CSV generado por sensors.py
archivo_csv = "data/sensors_data.csv"

print("\n📊 RESULTADOS DE MONITOREO DE TURBINA:\n")

with open(archivo_csv, newline="") as file:
    reader = csv.DictReader(file)
    for fila in reader:
        temp = float(fila["Temperatura (°C)"])
        pres = float(fila["Presión (psi)"])
        vib = float(fila["Vibración (mm/s)"])
        rpm = float(fila["RPM"])

        print(f"🕒 {fila['Fecha']}")
        print(f" Temperatura: {temp} °C → {evaluar_alerta('temperatura', temp)}")
        print(f" Presión: {pres} psi → {evaluar_alerta('presion', pres)}")
        print(f" Vibración: {vib} mm/s → {evaluar_alerta('vibracion', vib)}")
        print(f" RPM: {rpm} → {evaluar_alerta('rpm', rpm)}")
        print("-" * 50)
