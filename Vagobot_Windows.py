import csv, os, subprocess
from prettytable import PrettyTable
from termcolor import colored

def mostrar_contenido(header, content):
    table = PrettyTable(header)
    table.add_rows([row for row in content if len(row) == len(header)])
    print(table)

def leer_archivo_csv(archivo):
    with open(os.path.join("Naps", archivo), "r") as f:
        reader = csv.reader(f)
        cabecera = next(reader)
        contenido = list(reader)
    return cabecera, contenido

def mostrar_archivo_seleccionado(archivo_seleccionado):
    subprocess.run(["python", "Analizador.py", archivo_seleccionado])

archivo_seleccionado = None

def mostrar_todos_los_naps():
    archivos = [f for f in os.listdir("Naps") if f.endswith(".csv")]
    print("\033c", end="")
    if not archivos:
        input("Directorio vacío, pulse Enter para volver al menú")
        main()
        return
    print("Archivos disponibles:\n")
    for i, archivo in enumerate(archivos):
        print(colored(f"{archivo.split('.')[0]}", "yellow"))
    print("")
    while True:
        seleccion = input("Escriba el archivo que desea leer o 'V' para volver al menú: ")
        if seleccion == "V":
            return mostrar_menu_principal()
        archivo_seleccionado = seleccion + ".csv"
        if archivo_seleccionado not in archivos:
            print("El archivo seleccionado no está disponible.")
            continue
        mostrar_archivo_seleccionado(archivo_seleccionado)
        while True:
            print("R para volver a cargar los NAPs o Q para volver al menú")
            opcion = input().upper()
            if opcion == 'R':
                return mostrar_todos_los_naps()
            elif opcion == 'Q':
                return mostrar_menu_principal()
            else:
                print("Opción no válida, intente de nuevo")

def cargar_nuevo_nap():
    header = ["Nombre y Apellido", "Nro.Cliente", "Nro. Telefono", "PPPoE", "Vlan", "ONU", "Puerto", "NAP"]
    content = []
    while True:
        nap_name = input("Ingrese el nombre del NAP (ej: NAP 35): ")
        print("Ingrese Nombre y Apellido;Nro.Cliente;Nro.Telefono;PPPoE;Vlan;ONU;Puerto (ctrl + c para terminar): ")
        try:
            for line in iter(input, ""):
                line = line.split(';')
                if len(line) != 7:
                    print('Formato invalido, formato correcto: Nombre y Apellido;Nro.Cliente;Nro.Telefono;PPPoE;Vlan;ONU;Puerto.')
                    continue
                line.append(nap_name) # agregar el NAP al final de la lista
                content.append(line)
        except KeyboardInterrupt:
            pass

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
                    content = []
                    break
                elif next_step.lower() == "n":
                    return
                else:
                    print("Opción inválida, por favor ingrese 's' o 'n'.")
        else:
            print("Operación cancelada.")
            while True:
                next_step = input("¿Deseas ingresar nuevamente? (s/n): ")
                if next_step.lower() == "s":
                    content = []
                    break
                elif next_step.lower() == "n":
                    return
                else:
                    print("Opción inválida, por favor ingrese 's' o 'n'.")

def cargar_lista_nap():
    if not os.path.exists("NAP_X.csv"):
        print("No se encuentra el archivo NAP_X.csv en el directorio actual.")
        while True:
            print("Presione Q para volver al menú anterior.")
            opcion = input().upper()
            if opcion == 'Q':
                mostrar_menu_principal()
                return
    else:
        continuar = input("El CSV debe llamarse NAP_X.csv. ¿Continuar? (s/n)")
        if continuar.lower() == "s":
            subprocess.run(["python", "Separador.py"])
            print("\nPresione Q para volver al menú anterior.")
            opcion = input().upper()
            if opcion == 'Q':
                mostrar_menu_principal()
                return
        else:
            return

def mostrar_naps_masivos():
    while True:
        try:
            subprocess.run(['python', 'Masivo.py'])
            print("")
            opcion = input("Presione R volver a buscar o Q para el menú principal: ").upper()
            if opcion == 'R':
                continue
            elif opcion == 'Q':
                mostrar_menu_principal()
                return
            else:
                print("Opción inválida, por favor ingrese 'R' o 'Q'.")
        except FileNotFoundError:
            print("El archivo Masivo.py no se encuentra en la ruta especificada.")
            return

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
    print("\033[1;32m2.\033[0m Ver NAPs por VLAN")
    print("\033[1;32m3.\033[0m Cargar NAPs por lista")
    print("\033[1;32m4.\033[0m Cargar nuevo NAP a mano")
    print("\033[1;31m5.\033[0m Salir")
    print("\033[1;36m=============================================================\033[0m")

def main():
    while True:
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
