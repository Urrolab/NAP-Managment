import sys
import csv
import random
from prettytable import PrettyTable

def leer_archivo_csv(ruta_archivo):
    with open(ruta_archivo, "r") as archivo:
        lector = csv.reader(archivo)
        datos = list(lector)
        encabezados = datos[0]
        encabezados.append("Conexión")
        datos = datos[1:]
    return encabezados, datos

def generar_columna_conexion(datos):
    for fila in datos:
        fila.append(random.choice(["Conectado", "Desconectado"]))
    return datos

def crear_tabla(encabezados, datos):
    tabla = PrettyTable(encabezados)
    for fila in datos:
        tabla.add_row(fila)
    return tabla

def main(archivo_seleccionado):
    encabezados, datos = leer_archivo_csv("Naps/" + archivo_seleccionado)
    datos = generar_columna_conexion(datos)
    tabla = crear_tabla(encabezados, datos)
    print(tabla)

if __name__ == "__main__":
    archivo_seleccionado = sys.argv[1]
    main(archivo_seleccionado)