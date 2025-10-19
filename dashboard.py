import pandas as pd
import matplotlib.pyplot as plt

# Leer el archivo CSV generado por sensors.py
data = pd.read_csv("data/sensors_data.csv")

# Mostrar las primeras filas en consola (opcional)
print("\n📊 Datos cargados desde sensors_data.csv:\n")
print(data.head())

# Crear una figura con subgráficos para cada variable
plt.figure(figsize=(12, 8))
plt.suptitle("Dashboard PredictAir - Monitoreo de Turbina Aeronáutica", fontsize=14, fontweight='bold')

# --- Temperatura ---
plt.subplot(2, 2, 1)
plt.plot(data["Fecha"], data["Temperatura (°C)"], color="red")
plt.title("Temperatura (°C)")
plt.xticks(rotation=45)
plt.tight_layout(pad=2)

# --- Presión ---
plt.subplot(2, 2, 2)
plt.plot(data["Fecha"], data["Presión (psi)"], color="blue")
plt.title("Presión (psi)")
plt.xticks(rotation=45)
plt.tight_layout(pad=2)

# --- Vibración ---
plt.subplot(2, 2, 3)
plt.plot(data["Fecha"], data["Vibración (mm/s)"], color="green")
plt.title("Vibración (mm/s)")
plt.xticks(rotation=45)
plt.tight_layout(pad=2)

# --- RPM ---
plt.subplot(2, 2, 4)
plt.plot(data["Fecha"], data["RPM"], color="orange")
plt.title("Velocidad de rotación (RPM)")
plt.xticks(rotation=45)
plt.tight_layout(pad=2)

# Mostrar las gráficas
plt.show()
