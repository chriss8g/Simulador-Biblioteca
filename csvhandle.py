import csv

# *************************************************************
# ******************** Agregar columnas ***********************
# *************************************************************

# Definir las columnas del archivo CSV
columnas = ['Distribution In', 'AVE', 'Distribution Out', 'AVE', 'MAX Queue Size', 'MIN Queue Size', 'AVE Queue Size']

# Nombre del archivo CSV
nombre_archivo = 'data.csv'

# Abrir el archivo CSV en modo de escritura
with open(nombre_archivo, 'w', newline='') as archivo_csv:
    writer = csv.writer(archivo_csv)
    
    # Escribir las columnas en el archivo CSV
    writer.writerow(columnas)

print("Columnas agregadas exitosamente.")

# *************************************************************
# ********************** Agregar datos ************************
# *************************************************************

import csv

# Datos que deseas agregar al archivo CSV
datos_nuevos = ['Nuevo', 'Dato', '1']

# Nombre del archivo CSV
nombre_archivo = 'mi_archivo.csv'

# Modo de apertura del archivo: 'w' para escritura, 'a' para anexar
modo_apertura = 'a'

# Abre el archivo CSV en el modo especificado
with open(nombre_archivo, mode=modo_apertura, newline='') as archivo_csv:
    writer = csv.writer(archivo_csv)
    
    # Agrega una nueva fila al final del archivo CSV
    writer.writerow(datos_nuevos)

print("Fila agregada exitosamente.")