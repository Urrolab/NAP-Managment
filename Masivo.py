import csv, os, random
from termcolor import colored

print("\033c", end="")

def obtener_csv_files():
    return [f for f in os.listdir("Naps") if f.endswith('.csv')]

def generar_columna_conexion(csv_reader):
    data = [{**row, 'Conexión': 'Conectado' if random.randint(0, 1) == 1 else 'Desconectado'} for row in csv_reader]
    fieldnames = csv_reader.fieldnames + ['Conexión']
    return fieldnames, data

def actualizar_columna_conexion(csv_reader):
    data = [{**row, 'Conexión': 'Conectado' if random.randint(0, 1) == 1 else 'Desconectado'} for row in csv_reader]
    fieldnames = csv_reader.fieldnames
    return fieldnames, data

def contar_filas_conexion(vlan, data):
    total_rows = sum(1 for row in data if row['Vlan'] == vlan)
    connected_rows = sum(1 for row in data if row['Vlan'] == vlan and row['Conexión'] == 'Conectado')
    disconnected_rows = total_rows - connected_rows
    return total_rows, connected_rows, disconnected_rows

def calcular_porcentaje_conexion(total_rows, connected_rows, disconnected_rows):
    connected_percent, disconnected_percent = [(count / total_rows * 100) if total_rows > 0 else 0 for count in (connected_rows, disconnected_rows)]
    return connected_percent, disconnected_percent

def imprimir_estado_csv(file, connected_percent, disconnected_percent):
    if connected_percent >= 50:
        print(f"NAP: {colored(file, 'yellow')} Estado: {colored('Estable', 'green')} {connected_percent:.0f}% Usuarios Conectados")
    elif disconnected_percent >= 50:
        print(f"NAP: {colored(file, 'yellow')} Estado: {colored('Inestable', 'red')} {disconnected_percent:.0f}% Usuarios Desconectados")

# Obtener una lista de todos los archivos CSV en el directorio "Naps"
csv_files = obtener_csv_files()

def obtener_vlans():
    vlans = sorted(list({row['Vlan'] for file in os.listdir('Naps') if file.endswith('.csv') for row in csv.DictReader(open(os.path.join('Naps', file)))}))
    return vlans

def obtener_y_seleccionar_vlan():
    vlans = obtener_vlans()
    print("VLANs disponibles: \n")
    for vlan in vlans:
        print(colored(vlan , 'yellow'))
    print("")
    selected_vlan = input("Ingrese la VLAN: ")
    print("")
    return selected_vlan

def procesar_archivo_csv(csv_path):
    with open(csv_path, 'r') as f:
        csv_reader = csv.DictReader(f)
        has_conexion_column = 'Conexión' in csv_reader.fieldnames

        if not has_conexion_column:
            fieldnames, data = generar_columna_conexion(csv_reader)
        else:
            fieldnames, data = actualizar_columna_conexion(csv_reader)

        total_rows, connected_rows, disconnected_rows = contar_filas_conexion(selected_vlan, data)
        connected_percent, disconnected_percent = calcular_porcentaje_conexion(total_rows, connected_rows, disconnected_rows)
        imprimir_estado_csv(file, connected_percent, disconnected_percent)

# Obtener y seleccionar la VLAN
selected_vlan = obtener_y_seleccionar_vlan()

# Iterar sobre cada archivo CSV
for file in csv_files:
    csv_path = os.path.join("Naps", file)
    procesar_archivo_csv(csv_path)

