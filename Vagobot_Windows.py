# -*- coding: utf-8 -*-
import csv, os, subprocess
from prettytable import PrettyTable
from termcolor import colored
from flask import Flask, render_template, request

app = Flask(__name__)

# Define una función para mostrar el contenido de un archivo CSV en una tabla
def mostrar_contenido(header, content):
    table = PrettyTable(header) # Crea una nueva tabla con la cabecera especificada
    for row in content: # Itera sobre las filas de contenido
        if len(row) == len(header): # Si la fila tiene la misma cantidad de elementos que la cabecera
            table.add_row(row)
        else:
            print(f"La fila {row} no se agregará porque tiene un número incorrecto de valores.")
    print(table)

# Define una función para leer un archivo CSV y devolver su cabecera y contenido
def leer_archivo_csv(archivo):
    with open(os.path.join("Naps", archivo), "r") as f:
        reader = csv.reader(f)
        cabecera = next(reader)
        contenido = [linea for linea in reader]
    return cabecera, contenido

# Define una función para mostrar un archivo CSV seleccionado
def mostrar_archivo_seleccionado(archivo_seleccionado):
    subprocess.run(["python", "Analizador.py", archivo_seleccionado])

archivo_seleccionado = None

# Define una función para mostrar todos los archivos CSV disponibles en el directorio "Naps"
def mostrar_todos_los_naps():
    archivos = [f for f in os.listdir("Naps") if f.endswith(".csv")]
    print("\033c", end="") # Limpia la consola
    if not archivos:
        input("Directorio vacío, pulse Enter para volver al menú")
        main()
    else:
        print("Archivos disponibles:\n")
        for i, archivo in enumerate(archivos):
            nombre_sin_extension = archivo.split(".csv")[0]
            print(colored(f"{nombre_sin_extension}", "yellow"))
        print("")
        seleccion = input("Escriba el archivo que desea leer o 'V' para volver al menu: ")
        if seleccion == "V":
            return mostrar_menu_principal()
        archivo_seleccionado = seleccion + ".csv"
        if archivo_seleccionado in archivos:
            mostrar_archivo_seleccionado(archivo_seleccionado)
        else:
            print("El archivo seleccionado no está disponible.")

        while True:
            print("R para volver a cargar los NAPs o Q para volver al menu")
            opcion = input().upper()
            if opcion == 'R':
                mostrar_todos_los_naps()
                return
            elif opcion == 'Q':
                mostrar_menu_principal()
                return

# Esta función permite al usuario cargar un nuevo archivo de NAP.
#Se le solicita al usuario que ingrese el nombre del NAP, luego se define una lista header con las columnas necesarias y una lista content para almacenar las filas.
def cargar_nuevo_nap():
    print("\033c", end="")
    nap_name = input("Ingrese el nombre del NAP (ej: NAP 35): ")
    header = ["Nombre y Apellido", "Nro.Cliente" , "Nro. Telefono", "PPPoE" , "Vlan", "ONU", "Puerto" ,"NAP"]
    content = []
    print("Ingrese Nombre y Apellido;Nro.Cliente;Nro.Telefono;PPPoE;Vlan;ONU;Puerto (ctrl + c para terminar): ")
    completed = False
    while not completed:
        try:
            line = input()
            if not line:
                continue
            line = line.split(';')
            if len(line) != 7:
                print('Formato invalido, formato correcto: Nombre y Apellido;Nro.Cliente;Nro.Telefono;PPPoE;Vlan;ONU;Puerto.')
                continue
            line.append(nap_name) # agregar el NAP al final de la lista
            content.append(line)
        except KeyboardInterrupt:
            completed = True
    mostrar_contenido(header, content)
    confirm = input("¿Es correcta la información ingresada? (s/n): ")
    if confirm.lower() == "s":
        with open(os.path.join("Naps", f"{nap_name}.csv"), "w", newline='') as f:
            writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(header)
            writer.writerows(content)
        print("Archivo guardado exitosamente.")
        while True:
            next_step = input("¿Desea agregar otro NAP? (s/n): ")
            if next_step.lower() == "s":
                cargar_nuevo_nap()
                break
            elif next_step.lower() == "n":
                break
            else:
                print("Opción inválida, por favor ingrese 's' o 'n'.")
    else:
        print("Operación cancelada.")
        while True:
            next_step = input("¿Deseas ingresar nuevamente? (s/n): ")
            if next_step.lower() == "s":
                cargar_nuevo_nap()
                break
            elif next_step.lower() == "n":
                break
            else:
                print("Opción inválida, por favor ingrese 's' o 'n'.")

# Esta función permite al usuario cargar una lista de NAP desde un archivo CSV con nombre "NAP_X.csv" en el directorio actual.
def cargar_lista_nap():
    if os.path.exists("NAP_X.csv"):
        continuar = input("El CSV debe llamarse NAP_X.csv. ¿Continuar? (s/n)")
        if continuar.lower() == "s":
            subprocess.run(["python", "Separador.py"])
            print("")
            print("Presione Q para volver al menú anterior.")
            opcion = input().upper()
            if opcion == 'Q':
                mostrar_menu_principal()
                return
        else:
            return
    else:
        print("No se encuentra el archivo NAP_X.csv en el directorio actual.")
        while True:
            print("Presione Q para volver al menú anterior.")
            opcion = input().upper()
            if opcion == 'Q':
                mostrar_menu_principal()
                return

def mostrar_naps_masivos():
    try:
        # Ejecuta el archivo Masivo.py
        subprocess.run(['python', 'Masivo.py'])
        print("")
        # Muestra mensaje para volver a buscar o ir al menú principal.
        print("Presione R volver a buscar o Q para el menu princial.")
        opcion = input().upper()
        if opcion == 'R':
            mostrar_naps_masivos()
            return
        elif opcion == 'Q':
            mostrar_menu_principal()
            return
    except FileNotFoundError:
        # Si no encuentra el archivo, muestra un mensaje de error.
        print("El archivo Masivo.py no se encuentra en la ruta especificada.")

def mostrar_menu_principal():
    # Limpia la pantalla.
    os.system("powershell.exe Clear-Host")
    # Muestra el título del programa y un logo.
    print("\033[1;36m========== Sistema de NAPs Vagobot - Version Windows ==========\033[0m\n")
    print("\033[1;33m   _________  \033[0m")
    print("\033[1;33m  /    \\    \\ \033[0m")
    print("\033[1;33m /      \\    \\ \033[0m")
    print("\033[1;33m \\      /    // \033[0m")
    print("\033[1;33m  \\____/    //  \033[0m")
    print("\033[1;33m     WINDOWS   \033[0m\n")
    # Muestra las opciones del menú.
    print("\033[1;32m1.\033[0m Ver NAPs")
    print("\033[1;32m2.\033[0m Ver NAPs por VLAN")
    print("\033[1;32m3.\033[0m Cargar NAPs por lista")
    print("\033[1;32m4.\033[0m Cargar nuevo NAP a mano")
    print("\033[1;31m5.\033[0m Salir")
    print("\033[1;36m=============================================================\033[0m")

def main():
    while True:
        # Muestra el menú principal y espera que el usuario seleccione una opción.
        mostrar_menu_principal()
        opcion = input("Seleccione una opcion: ")
        if opcion == "1":
            mostrar_todos_los_naps()
        elif opcion == "2":
            mostrar_naps_masivos()
        elif opcion == "3":
            cargar_lista_nap()
        elif opcion == "4":
            cargar_nuevo_nap()
        elif opcion == "5":
            break
        else:
            print("Opcion invalida, seleccione nuevamente")

if __name__ == "__main__":
    main()
