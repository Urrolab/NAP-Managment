import sys
import csv
import random
from prettytable import PrettyTable
from termcolor import colored

def leer_archivo_csv(ruta_archivo):
    with open(ruta_archivo, "r") as archivo:
        lector = csv.reader(archivo)
        datos = list(lector)
        encabezados = datos[0]
        datos = datos[1:]
    return encabezados, datos

def generar_columna_conexion(datos, encabezados):
    print("\033c", end="")
    conexiones = []
    columna_existe = "Conexión" in encabezados
    indice_columna = encabezados.index("Conexión") if columna_existe else len(encabezados)
    for fila in datos:
        estado = random.choice(["Conectado", "Desconectado"])
        conexiones.append(estado)
        if columna_existe:
            fila[indice_columna] = estado
        else:
            fila.append(estado)
    if not columna_existe:
        encabezados.append("Conexión")
    if sum(c == "Desconectado" for c in conexiones) > len(datos) / 2:
        print(colored("¡NAP INESTABLE!".center(90), "red"))
    elif sum(c == "Conectado" for c in conexiones) > len(datos) / 2:
        print(colored("¡NAP ESTABLE!".center(90), "green"))
    return encabezados, datos

def crear_tabla(encabezados, datos):
    tabla = PrettyTable(encabezados)
    for fila in datos:
        fila_coloreada = [colored(c, "green" if c == "Conectado" else "red") if encabezados[i] == "Conexión" else c for i, c in enumerate(fila)]
        tabla.add_row(fila_coloreada)
    return tabla

def guardar_archivo_csv(ruta_archivo, encabezados, datos):
    with open(ruta_archivo, "w", newline="") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(encabezados)
        escritor.writerows(datos)

def main(archivo_seleccionado):
    ruta_archivo = "Naps/" + archivo_seleccionado
    encabezados, datos = leer_archivo_csv(ruta_archivo)
    encabezados, datos = generar_columna_conexion(datos, encabezados)
    tabla = crear_tabla(encabezados, datos)
    print(tabla)
    guardar_archivo_csv(ruta_archivo, encabezados, datos)

if __name__ == "__main__":
    archivo_seleccionado = sys.argv[1]
    main(archivo_seleccionado)