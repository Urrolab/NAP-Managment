import sys
import csv
import random
from prettytable import PrettyTable
from termcolor import colored


class NAP:
    def __init__(self, archivo_seleccionado):
        self.ruta_archivo = "Naps/" + archivo_seleccionado
        self.encabezados, self.datos = self.leer_archivo_csv()

    def leer_archivo_csv(self):
        with open(self.ruta_archivo, "r") as archivo:
            lector = csv.reader(archivo)
            datos = list(lector)
            encabezados = datos[0]
            datos = datos[1:]
        return encabezados, datos

    def generar_columna_conexion(self):
        print("\033c", end="")
        conexiones = []
        columna_existe = "Conexión" in self.encabezados
        indice_columna = self.encabezados.index("Conexión") if columna_existe else len(self.encabezados)
        for fila in self.datos:
            estado = random.choice(["Conectado", "Desconectado"])
            conexiones.append(estado)
            if columna_existe:
                fila[indice_columna] = estado
            else:
                fila.append(estado)
        if not columna_existe:
            self.encabezados.append("Conexión")
        if sum(c == "Desconectado" for c in conexiones) > len(self.datos) / 2:
            print(colored("¡NAP INESTABLE!".center(90), "red"))
        elif sum(c == "Conectado" for c in conexiones) > len(self.datos) / 2:
            print(colored("¡NAP ESTABLE!".center(90), "green"))

    def crear_tabla(self):
        tabla = PrettyTable(self.encabezados)
        for fila in self.datos:
            fila_coloreada = [colored(c, "green" if c == "Conectado" else "red") if self.encabezados[i] == "Conexión" else c for i, c in enumerate(fila)]
            tabla.add_row(fila_coloreada)
        return tabla

    def guardar_archivo_csv(self):
        with open(self.ruta_archivo, "w", newline="") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(self.encabezados)
            escritor.writerows(self.datos)

    def procesar_archivo(self):
        self.generar_columna_conexion()
        tabla = self.crear_tabla()
        print(tabla)
        self.guardar_archivo_csv()


if __name__ == "__main__":
    archivo_seleccionado = sys.argv[1]
    nap = NAP(archivo_seleccionado)
    nap.procesar_archivo()
