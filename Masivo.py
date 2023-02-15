import csv
import os
import random

def obtener_csv_files():
    return [f for f in os.listdir("Naps") if f.endswith('.csv')]

def generar_columna_conexion(csv_reader):
    data = []
    for row in csv_reader:
        row['Conexión'] = 'Conectado' if random.randint(0, 1) == 1 else 'Desconectado'
        data.append(row)
    fieldnames = csv_reader.fieldnames + ['Conexión']
    return fieldnames, data

def actualizar_columna_conexion(csv_reader):
    data = []
    fieldnames = csv_reader.fieldnames
    for row in csv_reader:
        row['Conexión'] = 'Conectado' if random.randint(0, 1) == 1 else 'Desconectado'
        data.append(row)
    return fieldnames, data

def contar_filas_conexion(vlan, data):
    total_rows = 0
    connected_rows = 0
    disconnected_rows = 0
    for row in data:
        if row['Vlan'] == vlan:
            total_rows += 1
            if row['Conexión'] == 'Conectado':
                connected_rows += 1
            elif row['Conexión'] == 'Desconectado':
                disconnected_rows += 1
    return total_rows, connected_rows, disconnected_rows

def calcular_porcentaje_conexion(total_rows, connected_rows, disconnected_rows):
    connected_percent = connected_rows / total_rows * 100 if total_rows > 0 else 0
    disconnected_percent = disconnected_rows / total_rows * 100 if total_rows > 0 else 0
    return connected_percent, disconnected_percent

def imprimir_estado_csv(file, connected_percent, disconnected_percent):
    if connected_percent > 50:
        print(f"NAP: {file} Estado: Conectado")
    elif disconnected_percent > 50:
        print(f"NAP: {file} Estado: Desconectado")

# Obtener una lista de todos los archivos CSV en el directorio "Naps"
csv_files = obtener_csv_files()

# Solicitar al usuario que ingrese la VLAN
vlan = input("Ingrese la VLAN: ")

# Iterar sobre cada archivo CSV
for file in csv_files:
    with open(os.path.join("Naps", file), 'r') as f:
        csv_reader = csv.DictReader(f)
        has_conexion_column = 'Conexión' in csv_reader.fieldnames

        if not has_conexion_column:
            fieldnames, data = generar_columna_conexion(csv_reader)
        else:
            fieldnames, data = actualizar_columna_conexion(csv_reader)

        total_rows, connected_rows, disconnected_rows = contar_filas_conexion(vlan, data)
        connected_percent, disconnected_percent = calcular_porcentaje_conexion(total_rows, connected_rows, disconnected_rows)
        imprimir_estado_csv(file, connected_percent, disconnected_percent)
