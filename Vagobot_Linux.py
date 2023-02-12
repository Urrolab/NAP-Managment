import csv, os, readline, subprocess
from prettytable import PrettyTable

def completer(text, state):
    options = [f.split(".csv")[0] for f in os.listdir("Naps") if f.endswith(".csv")]
    matches = [option for option in options if option.startswith(text)]
    try:
        return matches[state]
    except IndexError:
        return None

def mostrar_contenido(header, content):
    table = PrettyTable(header)
    for row in content:
        if len(row) == len(header):
            table.add_row(row)
        else:
            print(f"La fila {row} no se agregará porque tiene un número incorrecto de valores.")
    print(table)

def leer_archivo_csv(archivo):
    with open(os.path.join("Naps", archivo), "r") as f:
        reader = csv.reader(f)
        cabecera = next(reader)
        contenido = [linea for linea in reader]
    return cabecera, contenido

def mostrar_archivo_seleccionado(archivo_seleccionado):
    subprocess.run(["python", "Analizador.py", archivo_seleccionado])

archivo_seleccionado = None

def mostrar_todos_los_naps():
    readline.set_completer(completer)
    readline.parse_and_bind('tab: complete')
    archivos = [f for f in os.listdir("Naps") if f.endswith(".csv")]
    print("\033c", end="") # Limpia la consola
    if not archivos:
        input("Directorio vacío, pulse Enter para volver al menú")
        main()
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

def cargar_nuevo_nap():
    print("\033c", end="")
    nap_name = input("Ingrese el nombre del NAP (ej: NAP 35): ")
    header = ["Nombre y Apellido", "Nro.Cliente" , "Nro. Telefono", "PPPoE" , "Vlan", "ONU", "Puerto" ,"NAP"]
    content = []
    print("Ingrese Nombre y Apellido;Nro.Cliente;Nro.Telefono;PPPoE;Vlan;ONU;Puerto (ctrl + z para terminar): ")
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

def mostrar_menu_principal():
    print("\033c", end="") # Limpiar la pantalla
    print("\033[1;36m========== Sistema de NAPs Vagobot - Versión Linux ==========\033[0m\n")
    print("\033[1;33m    .--.    \033[0m")
    print("\033[1;33m   |o_o |   \033[0m")
    print("\033[1;33m   |:_/ |   \033[0m")
    print("\033[1;33m  //   \ \\  \033[0m")
    print("\033[1;33m (|     | ) \033[0m")
    print("\033[1;33m/'\\_   _/`\\\033[0m\n")
    print("\033[1;32m1.\033[0m Ver NAPs")
    print("\033[1;32m2.\033[0m Cargar nuevo NAP a mano")
    print("\033[1;31m3.\033[0m Salir")
    print("\033[1;36m=============================================================\033[0m")

def main():
    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            mostrar_todos_los_naps()
        elif opcion == "2":
            cargar_nuevo_nap()
        elif opcion == "3":
            break
        else:
            print("Opción inválida, seleccione nuevamente")

if __name__ == "__main__":
    main()