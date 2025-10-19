import os
import time

print("🛫 Iniciando simulador PredictAir...\n")

# 1) Ejecuta el generador de datos (sensors.py)
print(" Generando datos de sensores...")
os.system("python sensors.py")

# 2) Pausa  para simular el tiempo de lectura
time.sleep(2)

# 3) Ejecuta el sistema de alertas
print("\n Analizando condiciones de la turbina...\n")
# Aquí agregamos otra pausa antes de ejecutar alerts.py
time.sleep(2)

os.system("python alerts.py")

# 4) Mensaje en pantalla
print("\n ¡Simulación completada con éxito!")
print("Los datos fueron guardados en 'data/sensors_data.csv'")
