import csv
import os

# Abrimos el archivo de entrada y lo leemos
with open('NAP_X.csv', 'r') as file:
    reader = csv.reader(file)
    headers = next(reader) # Guardamos los headers

    # Creamos un diccionario para agrupar los usuarios por NAP
    nap_dict = {}
    for row in reader:
        nap = row[4]
        if nap in nap_dict:
            nap_dict[nap].append(row)
        else:
            nap_dict[nap] = [row]

# Iteramos sobre el diccionario para escribir cada archivo
for nap, rows in nap_dict.items():
    filename = nap.replace("/", "_") + '.csv'
    filename = os.path.join("Naps", filename)

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers) # Escribimos los headers
        for row in rows:
            row = [field.strip('"') for field in row] # Eliminamos las comillas dobles
            writer.writerow(row)
