# -*- coding: utf-8 -*-
import csv, os, msvcrt
from prettytable import PrettyTable

def mostrar_contenido(header, content):
    table = PrettyTable(header)
    for row in content:
        if len(row) == len(header):
            table.add_row(row)
        else:
            print(f"La fila {row} no se agregara porque tiene un numero incorrecto de valores.")
    print(table)

def leer_archivo_csv(archivo):
    with open(os.path.join("Naps", archivo), "r", encoding='utf-8') as f:
        reader = csv.reader(f)
        cabecera = next(reader)
        contenido = [linea for linea in reader]
    return cabecera, contenido

def mostrar_archivo_seleccionado(archivo_seleccionado):
    cabecera, contenido = leer_archivo_csv(archivo_seleccionado)
    mostrar_contenido(cabecera, contenido)

def mostrar_todos_los_naps():
    archivos = [f for f in os.listdir("Naps") if f.endswith(".csv")]
    print("\033c", end="") # Limpia la consola
    if not archivos:
        print("Directorio vacio, pulse Enter para n al menu principal")
        key = msvcrt.getch()
        if key == b'\r':
            mostrar_todos_los_naps()
            return
        elif key == b'\x1b':
            mostrar_menu_principal()
            return
    else:
        print("Archivos disponibles:")
        for i, archivo in enumerate(archivos):
            nombre_sin_extension = archivo.split(".csv")[0]
            print(f"{nombre_sin_extension}")

        seleccion = input("Escriba el archivo que desea leer o 'V' para volver al menu: ")
        if seleccion == "V":
            return mostrar_menu_principal()
        archivo_seleccionado = seleccion + ".csv"
        if archivo_seleccionado in archivos:
            mostrar_archivo_seleccionado(archivo_seleccionado)
        else:
            print("El archivo seleccionado no esta disponible.")

        while True:
            print("Pulse Enter para volver a cargar los NAPs o Escape para volver al menu principal")
            key = msvcrt.getch()
            if key == b'\r':
                mostrar_todos_los_naps()
            elif key == b'\x1b':
                mostrar_menu_principal()
                return

def cargar_nuevo_nap():
    print("\033c", end="")
    nap_name = input("Ingrese el nombre del NAP (ej: NAP 35): ")
    header = ["Nombre y Apellido", "PPPoE", "Telefono", "Vlan", "ONU", "Puerto", "NAP"]
    content = []
    print("Ingrese Nombre y Apellido;PPPoE;Telefono;Vlan;ONU;Puerto (ctrl + z para terminar): ")
    while True:
        try:
            line = input()
            if not line:
                continue
            line = line.split(';')
            if len(line) != 6:
                print('Formato invalido, formato correcto: Nombre y Apellido;PPPoE;Telefono;Vlan;ONU;Puerto.')
                continue
            line.append(nap_name) # agregar el NAP al final de la lista
            content.append(line)
        except EOFError:
            break
    mostrar_contenido(header, content)
    confirm = input("¿Es correcta la informacion ingresada? (s/n): ")
    if confirm.lower() == "s":
        with open(os.path.join("Naps", f"{nap_name}.csv"), "w", newline='', encoding='utf-8') as f:
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
                print("Opcion inválida, por favor ingrese 's' o 'n'.")
    else:
        print("Operacion cancelada.")
        while True:
            next_step = input("¿Deseas ingresar nuevamente? (s/n): ")
            if next_step.lower() == "s":
                cargar_nuevo_nap()
                break
            elif next_step.lower() == "n":
                break
            else:
                print("Opción invalida, por favor ingrese 's' o 'n'.")

def mostrar_menu_principal():
    os.system("powershell.exe Clear-Host")
    print("\033[1;36m========== Sistema de NAPs Vagobot - Version Windows ==========\033[0m\n")
    print("\033[1;33m   _________  \033[0m")
    print("\033[1;33m  /    \\    \\ \033[0m")
    print("\033[1;33m /      \\    \\ \033[0m")
    print("\033[1;33m \\      /    // \033[0m")
    print("\033[1;33m  \\____/    //  \033[0m")
    print("\033[1;33m     WINDOWS   \033[0m\n")
    print("\033[1;32m1.\033[0m Ver NAPs")
    print("\033[1;32m2.\033[0m Cargar nuevo NAP a mano")
    print("\033[1;31m3.\033[0m Salir")
    print("\033[1;36m=============================================================\033[0m")

def main():
    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opcion: ")
        if opcion == "1":
            mostrar_todos_los_naps()
        elif opcion == "2":
            cargar_nuevo_nap()
        elif opcion == "3":
            break
        else:
            print("Opcion invalida, seleccione nuevamente")
if __name__ == "__main__":
    main()